import sys
import subprocess

## params
# RUN = ['init', 'base', 'google', 'OTHER', 'all']
RUN = 'all' if len(sys.argv) == 1 else sys.argv[1]


if __name__ == "__main__":
    if RUN == 'init' or RUN == 'all':
        subprocess.run("pip install --upgrade pip", shell=True)
        subprocess.run("brew install tree", shell=True)

    if RUN == 'pip' or RUN == 'all':
        PY_PKG_LIST = [
            'python-dotenv', 'psycopg2-binary', 'sqlalchemy', 'pymongo', 'fastapi', 'Jinja2==3.1.2',
            'uvicorn[standard]', 'aiofiles', 'requests', 'beautifulsoup4', 'pandas', 'black',
            'setuptools', 'build', 'pdfplumber', 'pypdf2', 'openpyxl',
            '--upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"', 'selenium'
        ]
        for pkg_ in PY_PKG_LIST:
            subprocess.run(f"pip install {pkg_}", shell=True)

    if RUN == 'google' or RUN == 'all':
        # 安裝 google form api 相關的套件
        GOOGLE_PKG_LIST = [
            'google-api-python-client', 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib',
            'oauth2client'
        ]
        for pkg_ in GOOGLE_PKG_LIST:
            subprocess.run(f"pip install {pkg_}", shell=True)

    if RUN == 'OTHER' or RUN == 'all':
        # 其他套件
        subprocess.run('brew install smartmontools', shell=True)