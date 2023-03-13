from __future__ import print_function

import os.path
import io
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# 建立GoogleDrive類別，對GoogleDrive-api進行封裝
class GoogleDrive():

    # 初始化
    def __init__(self, TOKEN, CLIENT_SECRET_FILE, SCOPES):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        self.creds = None
        if os.path.exists(TOKEN):
            self.creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN, 'w') as token:
                token.write(self.creds.to_json())

        self.service = None

    # 取得google drive api服務
    def _get_service(self):
        if self.service is None:
            self.service = build('drive', 'v3', credentials=self.creds)
        return self.service

    # 建立資料夾
    def create_folder(self, folder_name, parent_folder_id):
        try:
            # create drive api client
            service = self._get_service()
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            file = service.files().create(body=file_metadata,
                                        fields='id').execute()
            print(F'Folder ID: {file.get("id")}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file

    # 查詢檔案
    def list_files(self, query="mimeType='image/jpeg'", print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name)',
                    pageToken=page_token
                ).execute()
                if print_file:
                    for file in response.get('files', []):
                        # Process change
                        print(F'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

        except HttpError as error:
            print(F'An error occurred: {error}')
            files = None

        return files

    # 上傳檔案
    def upload_file(self, file_name, mimetype='image/jpeg', folder_id=None):
        try:
            # create drive api client
            service = self._get_service()
            file_metadata = {'name': file_name}
            if folder_id is not None:
                file_metadata['parents'] = [folder_id]
            media = MediaFileUpload(file_name, mimetype=mimetype)
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(F'File ID: {file.get("id")}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

    # 下載檔案
    def download_file(self, file_id, file_name):
        try:
            # create drive api client
            service = self._get_service()
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F"Download {int(status.progress() * 100)}%.")
            with open(file_name, 'wb') as f:
                f.write(fh.getvalue())
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

    # 檔案搬移
    def move_file(self, file_id, folder_id):
        service = self._get_service()

        # Retrieve the existing parents to remove
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        # Move the file to the new folder
        file = service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

        print(F"File ID '{file.get('id')}' has been moved to folder ID '{folder_id}'.")
        return True

    # 刪除檔案
    def delete_file(self, file_id):
        try:
            # create drive api client
            service = self._get_service()
            service.files().delete(fileId=file_id).execute()
        except HttpError as error:
            print(F'An error occurred: {error}')
            return False
        return True

if __name__ == '__main__':
    googleDrive = GoogleDrive(
        TOKEN = 'MLOPS/env/googleDriveToken.json',
        CLIENT_SECRET_FILE='MLOPS/env/client_secret.json',
        SCOPES=['https://www.googleapis.com/auth/drive'], # 讀寫權限，刪除client_secret.json後，重新執行程式，會要求重新授權
        # SCOPES=['https://www.googleapis.com/auth/drive.metadata.readonly'] # 只有讀取權限，刪除client_secret.json後，重新執行程式，會要求重新授權
    )
    # files = googleDrive.list_files() # 查詢檔案
    # files = googleDrive.list_files(query="mimeType='image/jpeg'") # 查詢jpg
    # files = googleDrive.list_files(query="mimeType='video/mp4'") # 查詢mp4
    # files = googleDrive.list_files(query="mimeType='application/vnd.google-apps.folder'") # 查詢資料夾
    # files = googleDrive.list_files(query="'1zdcUj959fJ_YmjevBxRUqbE39ARj-rrs' in parents") # 查詢資料夾
    # print(files)

    # googleDrive.upload_file('MLOPS/env/testFile.txt', mimetype='application/json', folder_id='1zdcUj959fJ_YmjevBxRUqbE39ARj-rrs') # 上傳檔案

    # googleDrive.download_file('1xjTpMnKfaNKxJkMvUi2A8ldWjpOT0cPa', '/Users/peiyuwu/Downloads/testFile.txt') # 下載檔案

    # googleDrive.move_file('1xjTpMnKfaNKxJkMvUi2A8ldWjpOT0cPa', folder_id='1zdcUj959fJ_YmjevBxRUqbE39ARj-rrs') # 檔案搬移

    # 建立名為'newFolder'的資料夾
    # file_metadata = {
    #     'name': 'newFolder',
    #     'mimeType': 'application/vnd.google-apps.folder',
    #     'parents': ['1zdcUj959fJ_YmjevBxRUqbE39ARj-rrs']
    # }
    # file = googleDrive._get_service().files().create(body=file_metadata, fields='id').execute()
    # print(F"Folder ID: {file.get('id')}")

    googleDrive.delete_file('1xjTpMnKfaNKxJkMvUi2A8ldWjpOT0cPa') # 刪除檔案
