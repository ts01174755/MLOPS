import os

# 參考資料：
# >> https://blog.csdn.net/toopoo/article/details/104746623
# >> https://stackoverflow.com/questions/41129504/pycharm-with-pyenv
#
############################################################################################
os.system("brew install pyenv pyenv-virtualenv")
os.system("pyenv install 3.8.16")
os.system("pyenv virtualenv 3.8.16 [YourProjectName]")
os.system("pyenv local [YourProjectName]")
### >> 然後去 pycharm 控制台設定 Interpreter

############################################################################################
# os.system("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' > ~/.zshrc")  沒事別執行
# os.system("echo 'export PATH=\"$PYENV_ROOT/shims:$PATH\"' >> ~/.zshrc") 沒事別執行
# os.system("echo 'if which pyenv-virtualenv-init > /dev/null; then eval \"$(pyenv virtualenv-init -)\"; fi' >> ~/.zshrc") 沒事別執行
