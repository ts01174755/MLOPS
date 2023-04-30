# This is MLOps project created by NS R&Ds.
- by 台灣梯度下降第一品牌

# 環境安裝
## 版本控制
- 下載 pyenv, pyenv-virtualenv:

```brew install pyenv pyenv-virtualenv```

- 使用 python 3.8.16

```pyenv install 3.8.16```

- 為專案建立虛擬環境

```pyenv virtualenv 3.8.16 MLOPS```

- Clone 專案並指定虛擬環境

```git clone https://github.com/ts01174755/MLOPS.git MLOPS```

```cd MLOPS```
    
```pyenv local MLOPS```
    
    

env和 EnvironmentSetting不知道有什麼差異
名稱：不要用駝峰式的方式
1. config不是拿來執行用的，他是拿來放「環境參數」
2. 設置一個run.py的執行ㄎ檔案，可以透過名稱快速豊皆要執行的過程，run裡面放的是「執行參數」
3. 「執行參數」與「環境參數」：
   1. 環境參數：放在config裡，決定run.py檔案的背景參數 
   2. 執行參數：放在run.py裡，決定直寄執行所必要的參數

透過run獲取env_config，把步驟參數與環境參數打進controller裏面，讓controller可以在不同的環境下執行不同的不走參數
run.py要放在跟目錄下
controller下import的model請用src.model.package或是[project].model.package

目標是我拿到一哥可執行的資料夾，我直接copy paste到指定的contorller or model之後，稍微改依蝦參數？（還境或者是不揍餐數）
env_config也放在最外面