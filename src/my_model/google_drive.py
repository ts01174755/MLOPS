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
import shlex


class GoogleDriveBase:
    # 取得google drive api服務
    def _get_service(self):
        if self.service is None:
            self.service = build("drive", "v3", credentials=self.creds)
        return self.service

    # 建立資料夾
    def create_folder(self, folder_name, parent_folder_id, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_folder_id],
            }
            file = service.files().create(body=file_metadata, fields="id").execute()
            if print_file:
                print(f'Folder ID: {file.get("id")}')
        except HttpError as error:
            print(f"An error occurred: {error}")
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
                response = (
                    service.files()
                    .list(
                        q=query,
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                if print_file:
                    for file in response.get("files", []):
                        # Process change
                        print(f'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        return files

    # 上傳檔案
    def upload_file(
        self,
        target_file,
        file_name,
        mimetype="image/jpeg",
        folder_id=None,
        print_file=False,
    ):
        try:
            # create drive api client
            service = self._get_service()
            file_metadata = {"name": file_name}
            if folder_id is not None:
                file_metadata["parents"] = [folder_id]
            media = MediaFileUpload(target_file, mimetype=mimetype, resumable=True)
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            if print_file:
                print(f'File ID: {file.get("id")}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 下載檔案
    def download_file(self, file_id, file_name, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                if print_file:
                    print(f"Download {int(status.progress() * 100)}%.")
            with open(file_name, "wb") as f:
                f.write(fh.getvalue())
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 檔案搬移，使用 addParents 和 removeParents
    def move_file(self, file_id, folder_id, file_name, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            file = service.files().get(fileId=file_id, fields="parents").execute()
            previous_parents = ",".join(file.get("parents"))
            file = (
                service.files()
                .update(
                    fileId=file_id,
                    addParents=folder_id,
                    removeParents=previous_parents,
                    fields="id, parents",
                )
                .execute()
            )
            # 更改檔名
            file_metadata = {"name": file_name}
            file = (
                service.files()
                .update(fileId=file_id, body=file_metadata, fields="id")
                .execute()
            )
            if print_file:
                print(f'File ID: {file.get("id")}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 檔案複製
    def copy_file(self, file_id, folder_id, file_name=None, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            file_metadata = {"name": file_name}
            if folder_id is not None:
                file_metadata["parents"] = [folder_id]
            file = (
                service.files()
                .copy(fileId=file_id, body=file_metadata, fields="id")
                .execute()
            )
            if print_file:
                print(f'File ID: {file.get("id")}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 刪除檔案
    def delete_file(self, file_id, file_name, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            service.files().delete(fileId=file_id).execute()
            if print_file:
                print(f"File {file_name} has been deleted.")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 刪除資料夾
    def delete_folder(self, folder_id, folder_name, print_file=False):
        try:
            # create drive api client
            service = self._get_service()
            service.files().delete(fileId=folder_id).execute()
            if print_file:
                print(f"Folder {folder_name} has been deleted.")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 取得檔案資訊
    def get_file_info(self, file_id):
        try:
            # create drive api client
            service = self._get_service()
            file = service.files().get(fileId=file_id).execute()
            print(f'File ID: {file.get("id")}')
            print(f'File Name: {file.get("name")}')
            print(f'File Size: {file.get("size")}')
            print(f'File MimeType: {file.get("mimeType")}')
            print(f'File CreatedTime: {file.get("createdTime")}')
            print(f'File ModifiedTime: {file.get("modifiedTime")}')
            print(f'File WebContentLink: {file.get("webContentLink")}')
            print(f'File WebViewLink: {file.get("webViewLink")}')
            print(f'File IconLink: {file.get("iconLink")}')
            print(f'File ThumbnailLink: {file.get("thumbnailLink")}')
            print(f'File Parents: {file.get("parents")}')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
        return True

    # 取得檔案下載連結
    def get_file_download_link(self, file_id):
        try:
            # create drive api client
            service = self._get_service()
            file = service.files().get(fileId=file_id).execute()
            return file.get("webContentLink")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


# 建立GoogleDrive類別，對GoogleDrive-api進行封裝
class GoogleDrive(GoogleDriveBase):
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
                    CLIENT_SECRET_FILE, SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN, "w") as token:
                token.write(self.creds.to_json())

        self.service = None
        self.folderIdTree = {}
        self.folderNameIdMap = {}
        self.currentFolderId = "root"

    # 解析execute_shell_command的指令
    def _parse_command(self, cmd_str):
        return shlex.split(cmd_str)

    # 用Google Drive API實作ls指令，並把結果存在self.folderTree中
    # 模擬 ls /Users/xxx/Downloads
    def _ls_cmd(self, targetFolder, print_file=True):
        cmdResult = []
        if len(targetFolder) == 0:
            files = self.list_files(
                query="mimeType='application/vnd.google-apps.folder' and 'root' in parents"
            )
            for file in files:
                if print_file:
                    print(f'{file.get("name")}/')
                cmdResult.append(f'{file.get("name")}/')
        else:
            # 取得資料夾ID
            folderId = "root"
            for folder_ind_ in range(len(targetFolder)):
                if folderId not in self.folderIdTree:
                    self.folderIdTree[folderId] = {}

                # 取得資料夾ID
                folder = targetFolder[folder_ind_]
                if folder not in self.folderIdTree[folderId]:
                    files = self.list_files(
                        query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                    )
                    for file in files:
                        if file.get("name") == folder:
                            self.folderIdTree[folderId][folder] = file.get("id")
                            break
                if folder in self.folderIdTree[folderId]:
                    folderId = self.folderIdTree[folderId][folder]
                else:
                    print(f"找不到資料夾 {'/' + '/'.join(targetFolder[:folder_ind_+1])}")
                    return cmdResult

            # 取得資料夾內容
            files = self.list_files(query=f"'{folderId}' in parents")
            for file in files:
                if print_file:
                    print(f'{file.get("name")}')
                cmdResult.append(f'{file.get("name")}')
        return cmdResult

    # 用Google Drive API實作cd指令，並把結果存在self.folderTree中
    # 模擬 cd /Users/xxx/Downloads
    def _cd_cmd(self, targetFolder):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(targetFolder)):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = targetFolder[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(targetFolder[:folder_ind_+1])}")
                return None

        self.currentFolderId = folderId
        return self.currentFolderId

    # 用Google Drive API實作mkdir指令，並把結果存在self.folderTree中
    # 模擬 mkdir /Users/xxx/Downloads
    def _mkdir_cmd(self, targetFolder):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(targetFolder)):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = targetFolder[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                # 建立資料夾
                file = self.create_folder(
                    folder_name=folder, parent_folder_id=folderId, print_file=False
                )
                self.folderIdTree[folderId][folder] = file.get("id")
                folderId = file.get("id")
        return "success"

    # 用Google Drive API實作upload指令，並把結果存在self.folderTree中
    # 模擬 upload /Users/xxx/Downloads/xxx.txt /Users/xxx/Downloads/xxx.txt
    def _upload_cmd(
        self, uploadFile, fileName, targetFolder, mimetype=None, print_file=True
    ):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(targetFolder)):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = targetFolder[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                # 建立資料夾
                file = self.create_folder(
                    folder_name=folder, parent_folder_id=folderId, print_file=False
                )
                self.folderIdTree[folderId][folder] = file.get("id")
                folderId = file.get("id")

        # 上傳檔案
        self.upload_file(
            target_file=uploadFile,
            file_name=fileName,
            mimetype=mimetype,
            folder_id=folderId,
            print_file=print_file,
        )
        return "success"

    # 用Google Drive API實作download指令，並把結果存在self.folderTree中
    # 模擬 download /Users/xxx/Downloads/xxx.txt /Users/xxx/Downloads/xxx.txt
    def _download_cmd(self, sourceFile, fileName, print_file=True):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(sourceFile) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = sourceFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(sourceFile[:folder_ind_+1])}")
                return None

        # 取得檔案ID
        fileId = None
        files = self.list_files(query=f"'{folderId}' in parents")
        for file in files:
            if file.get("name") == sourceFile[-1]:
                fileId = file.get("id")
                break
        if fileId is None:
            print(f"找不到檔案 {'/' + '/'.join(sourceFile)}")
            return None

        # 下載檔案
        self.download_file(file_id=fileId, file_name=fileName, print_file=print_file)
        return "success"

    # 用Google Drive API實作mv指令，並把結果存在self.folderTree中
    # 模擬 mv /Users/xxx/Downloads/xxx.txt /Users/xxx/Downloads/xxx.txt
    def _mv_cmd(self, sourceFile, targetFolder, print_file=True):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(sourceFile) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = sourceFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(sourceFile[:folder_ind_+1])}")
                return '找不到資料夾'

        # 取得檔案ID
        fileName = sourceFile[-1]
        sourceFileId = None
        files = self.list_files(
            query=f"mimeType!='application/vnd.google-apps.folder' and '{folderId}' in parents"
        )
        for file in files:
            if file.get("name") == fileName:
                sourceFileId = file.get("id")
                break
        if sourceFileId is None:
            print(f"找不到檔案 {'/' + '/'.join(sourceFile)}")
            return '找不到檔案'

        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(targetFolder) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = targetFolder[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                # 建立資料夾
                file = self.create_folder(
                    folder_name=folder, parent_folder_id=folderId, print_file=False
                )
                self.folderIdTree[folderId][folder] = file.get("id")
                folderId = file.get("id")

        # 取得檔案ID
        fileName = targetFolder[-1]
        fileId = None
        files = self.list_files(
            query=f"mimeType!='application/vnd.google-apps.folder' and '{folderId}' in parents"
        )
        for file in files:
            if file.get("name") == fileName:
                fileId = file.get("id")
                break
        if fileId is not None:
            print(f"檔案已存在 {'/' + '/'.join(targetFolder)}")
            return "檔案已存在"

        # 移動檔案
        self.move_file(
            file_id=sourceFileId,
            folder_id=folderId,
            file_name=fileName,
            print_file=print_file,
        )
        return "success"

    # 用Google Drive API實作rmdir指令，並把結果存在self.folderTree中
    # 模擬 rmdir /Users/xxx/Downloads/xxx.txt
    def _rmdir_cmd(self, sourceFile, print_file=True):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(sourceFile)):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = sourceFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(sourceFile[:folder_ind_+1])}")
                return None

        # 刪除資料夾
        self.delete_folder(
            folder_id=folderId, folder_name=sourceFile[-1], print_file=print_file
        )
        return "success"

    # 用Google Drive API實作rm指令，並把結果存在self.folderTree中
    # 模擬 rm /Users/xxx/Downloads/xxx.txt
    def _rm_cmd(self, sourceFile, recursive=False, print_file=True):
        if recursive:
            return self._rmdir_cmd(sourceFile, print_file=print_file)
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(sourceFile) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = sourceFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(sourceFile[:folder_ind_+1])}")
                return None
        else:
            # 取得檔案ID
            fileName = sourceFile[-1]
            fileId = None
            files = self.list_files(
                query=f"mimeType!='application/vnd.google-apps.folder' and '{folderId}' in parents"
            )
            for file in files:
                if file.get("name") == fileName:
                    fileId = file.get("id")
                    break
            if fileId is None:
                print(f"找不到檔案 {'/' + '/'.join(sourceFile)}")
                return None

            # 刪除檔案
            self.delete_file(file_id=fileId, file_name=fileName, print_file=print_file)
            return "success"

    # 用Google Drive API實作cp指令，並把結果存在self.folderTree中
    # 模擬 cp /Users/xxx/Downloads/xxx.txt /Users/xxx/Downloads/xxx2.txt
    def _cp_cmd(self, sourceFile, targetFile, print_file=True):
        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(sourceFile) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = sourceFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(sourceFile[:folder_ind_+1])}")
                return "找不到資料夾"
        # 取得檔案ID
        fileName = sourceFile[-1]
        sourceFileId = None
        files = self.list_files(
            query=f"mimeType!='application/vnd.google-apps.folder' and '{folderId}' in parents"
        )
        for file in files:
            if file.get("name") == fileName:
                sourceFileId = file.get("id")
                break
        if sourceFileId is None:
            print(f"找不到檔案 {'/' + '/'.join(sourceFile)}")
            return "找不到檔案"

        # 取得資料夾ID
        folderId = "root"
        for folder_ind_ in range(len(targetFile) - 1):
            if folderId not in self.folderIdTree:
                self.folderIdTree[folderId] = {}

            # 取得資料夾ID
            folder = targetFile[folder_ind_]
            if folder not in self.folderIdTree[folderId]:
                files = self.list_files(
                    query=f"mimeType='application/vnd.google-apps.folder' and '{folderId}' in parents"
                )
                for file in files:
                    if file.get("name") == folder:
                        self.folderIdTree[folderId][folder] = file.get("id")
                        break
            if folder in self.folderIdTree[folderId]:
                folderId = self.folderIdTree[folderId][folder]
            else:
                print(f"找不到資料夾 {'/' + '/'.join(targetFile[:folder_ind_+1])}")
                return "找不到資料夾"
        # 取得檔案ID
        fileName = targetFile[-1]
        fileId = None
        files = self.list_files(
            query=f"mimeType!='application/vnd.google-apps.folder' and '{folderId}' in parents"
        )
        for file in files:
            if file.get("name") == fileName:
                fileId = file.get("id")
                break
        if fileId is not None:
            print(f"檔案已存在 {'/' + '/'.join(targetFile)}")
            return "檔案已存在"

        # 複製檔案
        self.copy_file(
            file_id=sourceFileId,
            file_name=fileName,
            folder_id=folderId,
            print_file=print_file,
        )

        return "success"

    # 模擬Shell指令
    def execute_shell_command(self, command, print_file=True):
        cmdList = self._parse_command(command)
        print(" ".join(cmdList))
        if cmdList[0] == "ls":
            if len(cmdList) == 1:
                return self._ls_cmd(targetFolder=[], print_file=print_file)
            elif len(cmdList) == 2:
                targetFolder = cmdList[1].split("/")
                if targetFolder[0] == "":
                    targetFolder = targetFolder[1:]
                if targetFolder == [""]:
                    targetFolder = []
                return self._ls_cmd(targetFolder=targetFolder, print_file=print_file)
            else:
                print("ls指令參數錯誤")
                return []
        elif cmdList[0] == "cd":
            if len(cmdList) == 1:
                self.currentFolderId = "root"
            elif len(cmdList) == 2:
                targetFolder = cmdList[1].split("/")
                if targetFolder[0] == "":
                    targetFolder = targetFolder[1:]
                self.currentFolderId = self._cd_cmd(targetFolder)
            else:
                print("cd指令參數錯誤")
            return self.currentFolderId
        elif cmdList[0] == "mkdir":
            if len(cmdList) == 2:
                targetFolder = cmdList[1].split("/")
                if targetFolder[0] == "":
                    targetFolder = targetFolder[1:]
                return self._mkdir_cmd(targetFolder=targetFolder)
            else:
                print("mkdir指令參數錯誤")
        elif cmdList[0] == "upload":
            uploadFile = cmdList[1]
            fileName = cmdList[2].split("/")[-1]
            targetFolder = cmdList[2].split("/")[:-1]
            if targetFolder[0] == "":
                targetFolder = targetFolder[1:]
            if len(cmdList) == 3:
                return self._upload_cmd(
                    uploadFile=uploadFile,
                    fileName=fileName,
                    targetFolder=targetFolder,
                    print_file=print_file,
                )
            elif len(cmdList) == 4:
                mimetype = None
                if cmdList[3].split("=")[0] == "--mimetype":
                    mimetype = cmdList[3].split("=")[1]
                return self._upload_cmd(
                    uploadFile=uploadFile,
                    fileName=fileName,
                    targetFolder=targetFolder,
                    mimetype=mimetype,
                    print_file=print_file,
                )
            else:
                print("upload指令參數錯誤")
        elif cmdList[0] == "download":
            if len(cmdList) == 3:
                sourceFile = cmdList[1].split("/")
                if sourceFile[0] == "":
                    sourceFile = sourceFile[1:]
                targetFile = cmdList[2]
                return self._download_cmd(
                    sourceFile=sourceFile, fileName=targetFile, print_file=print_file
                )
            else:
                print("download指令參數錯誤")
        elif cmdList[0] == "mv":
            if len(cmdList) == 3:
                source = cmdList[1].split("/")
                target = cmdList[2].split("/")
                if source[0] == "":
                    source = source[1:]
                if target[0] == "":
                    target = target[1:]
                return self._mv_cmd(sourceFile=source, targetFolder=target)
            else:
                print("mv指令參數錯誤")
        elif cmdList[0] == "rm":
            if len(cmdList) == 2:
                sourceFile = cmdList[1].split("/")
                if sourceFile[0] == "":
                    sourceFile = sourceFile[1:]
                return self._rm_cmd(sourceFile=sourceFile, print_file=print_file)
            elif len(cmdList) == 3:
                if cmdList[1] == "-r":
                    sourceFile = cmdList[2].split("/")
                    if sourceFile[0] == "":
                        sourceFile = sourceFile[1:]
                    return self._rm_cmd(
                        sourceFile=sourceFile, recursive=True, print_file=print_file
                    )
                else:
                    print("rm指令參數錯誤")
        elif cmdList[0] == "cp":
            if len(cmdList) == 3:
                sourceFile = cmdList[1].split("/")
                targetFile = cmdList[2].split("/")
                if sourceFile[0] == "":
                    sourceFile = sourceFile[1:]
                if targetFile[0] == "":
                    targetFile = targetFile[1:]
                return self._cp_cmd(
                    sourceFile=sourceFile, targetFile=targetFile, print_file=print_file
                )
            else:
                print("cp指令參數錯誤")


if __name__ == "__main__":
    # token 教學
    # https://xenby.com/b/180-%E6%95%99%E5%AD%B8-%E5%A6%82%E4%BD%95%E7%94%B3%E8%AB%8B%E4%B8%A6%E4%BD%BF%E7%94%A8token%E5%AD%98%E5%8F%96google-drive-rest-api-%E4%B8%8D%E9%9C%80%E4%BD%BF%E7%94%A8%E8%80%85%E4%BB%8B%E9%9D%A2

    import pprint
    import time

    googleDrive = GoogleDrive(
        TOKEN="MLOPS/env/googleDriveToken_stpeteamshare.json",
        CLIENT_SECRET_FILE="MLOPS/env/client_secret_stpeteamshare.json",
        SCOPES=[
            "https://www.googleapis.com/auth/drive"
        ],  # 讀寫權限，刪除client_secret.json後，重新執行程式，會要求重新授權
        # SCOPES=['https://www.googleapis.com/auth/drive.metadata.readonly'] # 只有讀取權限，刪除client_secret.json後，重新執行程式，會要求重新授權
    )
    # # 查詢根目錄下所有檔案
    # files = googleDrive.list_files(query='root in parents')
    # files = googleDrive.list_files(query="mimeType='image/jpeg'") # 查詢jpg
    # files = googleDrive.list_files(query="mimeType='video/mp4'") # 查詢mp4
    # files = googleDrive.list_files(query="mimeType='application/vnd.google-apps.folder'") # 查詢資料夾
    # files = googleDrive.list_files(query="'1zdcUj959fJ_YmjevBxRUqbE39ARj-rrs' in parents") # 查詢資料夾
    # files = googleDrive.list_files(query="mimeType='application/vnd.google-apps.folder' and 'root' in parents") # 查詢根目錄下所有資料夾
    # files = googleDrive.list_files(query="mimeType='application/vnd.google-apps.folder' and name='newFolder'") # 查詢特定名字的資料夾

    # 路徑建議使用絕對路徑，相對路徑會有問題
    # # ls 測試－只能查詢資料夾
    # # files = googleDrive.execute_shell_command(f'ls /', print_file=False) # 查詢根目錄下所有檔案
    # files = googleDrive.execute_shell_command(f'ls /testFolder/newFolder', print_file=False) # 查詢根目錄下所有檔案
    #
    # # cd 測試－只能取得資料夾ＩＤ
    # files = googleDrive.execute_shell_command(f'cd /testFolder/newFolder', print_file=True) # 切換資料夾
    #
    # # mkdir 測試
    # timeStr = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    # files = googleDrive.execute_shell_command(f'mkdir /testFolder/newFolder{timeStr}', print_file=False) # 建立資料夾
    # files = googleDrive.execute_shell_command(f'mkdir /testFolder/newFolder{timeStr}_2', print_file=False) # 建立資料夾
    #
    # # upload 測試
    # files = googleDrive.execute_shell_command(f'upload /Users/peiyuwu/Desktop/testFile.txt /testFolder/newFolder{timeStr}/testFile.txt', print_file=False) # 上傳檔案
    #
    # # cp 測試
    # files = googleDrive.execute_shell_command(f'cp /testFolder/newFolder{timeStr}/testFile.txt /testFolder/newFolder{timeStr}_2/testFile_copy.txt', print_file=False) # 複製檔案
    # files = googleDrive.execute_shell_command(f'cp /testFolder/newFolder{timeStr}/testFile.txt /testFolder/newFolder{timeStr}_2/testFile_copy2.txt', print_file=False) # 複製檔案
    #
    # # download 測試
    # files = googleDrive.execute_shell_command(f'download /testFolder/newFolder{timeStr}_2/testFile_copy.txt /Users/peiyuwu/Desktop/testFile_copy.txt', print_file=False) # 下載檔案
    #
    # # mv 測試
    # files = googleDrive.execute_shell_command(f'mv /testFolder/newFolder{timeStr}_2/testFile_copy.txt /testFolder/newFolder{timeStr}/testFile_copy_mv.txt', print_file=False) # 移動檔案
    #
    # # rm 測試
    # files = googleDrive.execute_shell_command(f'rm /testFolder/newFolder{timeStr}_2/testFile_copy2.txt', print_file=False) # 刪除檔案
    # files = googleDrive.execute_shell_command(f'rm -r /testFolder/newFolder{timeStr}_2', print_file=False) # 刪除資料夾
    #
