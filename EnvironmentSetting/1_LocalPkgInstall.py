from package.common.shellCmd import shellCmd
import os

shellcmd = shellCmd()
shellcmd.execute("pip install --upgrade pip", shell=True)
shellcmd.execute("pip install python-dotenv", shell=True)
shellcmd.execute('pip install psycopg2-binary', shell=True)
shellcmd.execute('pip install pymongo', shell=True)
shellcmd.execute('pip install fastapi', shell=True)
shellcmd.execute('pip install uvicorn', shell=True)
shellcmd.execute('pip install requests', shell=True)
shellcmd.execute('pip install beautifulsoup4', shell=True)
