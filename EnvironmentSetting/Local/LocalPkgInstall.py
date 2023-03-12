import subprocess

subprocess.run("pip install --upgrade pip", shell=True)
subprocess.run("pip install python-dotenv", shell=True)
subprocess.run('pip install psycopg2-binary', shell=True)
subprocess.run('pip install pymongo', shell=True)
subprocess.run('pip install fastapi', shell=True)
subprocess.run('pip install uvicorn', shell=True)
subprocess.run('pip install requests', shell=True)
subprocess.run('pip install beautifulsoup4', shell=True)

# 安裝 google form api 相關的套件
subprocess.run('pip install google-api-python-client', shell=True)
subprocess.run('pip install google-auth-httplib2', shell=True)
subprocess.run('pip install google-auth-oauthlib', shell=True)
subprocess.run('pip install oauth2client', shell=True)


