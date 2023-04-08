import subprocess

# 啟動Jenkins
# 操作方法：
# 1. brew services start jenkins-lts # 啟動
# 2. brew services stop jenkins-lts # 停止
# 3. brew services restart jenkins-lts # 重啟
subprocess.run("brew services start jenkins-lts", shell=True)
