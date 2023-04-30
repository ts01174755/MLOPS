import subprocess


if __name__ == "__main__":
    RUN = ['base', 'google', 'OTHER'][0]
    if RUN == 'base':
        subprocess.run("pip install --upgrade pip", shell=True)
        subprocess.run("brew install tree", shell=True)

    elif RUN == 'base':
        PY_PKG_LIST = [
            'python-dotenv', 'psycopg2-binary', 'sqlalchemy', 'pymongo', 'fastapi', 'Jinja2==3.1.2',
            'uvicorn[standard]', 'aiofiles', 'requests', 'beautifulsoup4', 'pandas', 'black',
            'setuptools', 'build'
        ]
        for pkg_ in PY_PKG_LIST:
            subprocess.run(f"pip install {pkg_}", shell=True)

    elif RUN == 'google':
        # 安裝 google form api 相關的套件
        GOOGLE_PKG_LIST = [
            'google-api-python-client', 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib',
            'oauth2client'
        ]
        for pkg_ in GOOGLE_PKG_LIST:
            subprocess.run(f"pip install {pkg_}", shell=True)


    elif RUN == 'OTHER':
        # 其他套件
        subprocess.run('brew install smartmontools', shell=True)