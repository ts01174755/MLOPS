import subprocess


if __name__ == "__main__":
    RUN = ['base', 'google', 'OTHER'][0]

    if RUN == 'base':
        subprocess.run("pip install --upgrade pip", shell=True)
        subprocess.run("pip install python-dotenv", shell=True)
        subprocess.run("pip install psycopg2-binary", shell=True)
        subprocess.run("pip install sqlalchemy", shell=True)
        subprocess.run("pip install pymongo", shell=True)
        subprocess.run("pip install fastapi", shell=True)
        subprocess.run("pip install Jinja2==3.1.2", shell=True)
        subprocess.run("pip install uvicorn[standard]", shell=True)
        subprocess.run("pip install aiofiles", shell=True)
        subprocess.run("pip install requests", shell=True)
        subprocess.run("pip install beautifulsoup4", shell=True)
        subprocess.run("pip install pandas", shell=True)
        subprocess.run("pip install black", shell=True)
        subprocess.run("pip install --upgrade setuptools", shell=True)
        subprocess.run("python -m pip install --upgrade build", shell=True)
        subprocess.run("brew install tree", shell=True)

    elif RUN == 'google':
        # 安裝 google form api 相關的套件
        subprocess.run("pip install google-api-python-client", shell=True)
        subprocess.run("pip install google-auth", shell=True)
        subprocess.run("pip install google-auth-httplib2", shell=True)
        subprocess.run("pip install google-auth-oauthlib", shell=True)
        subprocess.run("pip install oauth2client", shell=True)

    elif RUN == 'OTHER':
        # 其他套件
        subprocess.run('brew install smartmontools', shell=True)