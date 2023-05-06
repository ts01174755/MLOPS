# This is MLOps project created by NS R&Ds.
- by 台灣梯度下降第一品牌

## Version-log
- 1.1.7:
  - 新增控制多個controller的架構
  - 微調微服務的架構
    - 新增log功能
  - CICD
    - 微調自動執行CI到container的方法
    - 微調自動執行CD container 的方法

# 環境安裝
## 啟動pyenv
1. 下載 pyenv, pyenv-virtualenv:

```brew install pyenv pyenv-virtualenv```

2. Clone 專案並指定虛擬環境

```git clone https://github.com/ts01174755/MLOPS.git [Your Project Path]```

3. pyenv 設定

```cd [Your Project Path]```

```python3 pyenv_setting.py```

```source ~/.zshrc```

## 版本控制
- 使用 python 3.8.16

```pyenv install 3.8.16```

- 為專案建立虛擬環境

```pyenv virtualenv 3.8.16 mlops_nsrd```

```cd [Your Project Path]```
    
```pyenv local mlops_nsrd```
    
## 建立環境(建議用pyenv)

- 進入env_config修改參數，有五個CONTAINER參數要做修改

```vim env_config.py```

    IMAGE_MONGODB_TAG = [YOUR MONGODB IMAGE TAG]
    CONTAINER_MONGODB_NAME = [YOUR MONGODB CONTAINER NAME]
    CONTAINER_MONGODB_PORT_LIST = [YOUR MONGODB PORT LIST]
    CONTAINER_MONGODB_ROOT = [YOUR MONGODB ROOT]
    CONTAINER_MONGODB_ROOT_MAP = [YOUR MONGODB ROOT MAP]
    CONTAINER_MONGO_POSTGRES_NET = [YOUR MONGODB POSTGRES NET]
    CONTAINER_MONGO_ENV_DICT = [CONTAINER_MONGO_ENV_DICT]

```python3 env_local_pkgInstall.py all```

```python3 env_docker_mongodb.py all```

```python3 env_docker_postgres.py all```

# MongoDB

### MongoDB - 建立資料庫

> $ mongo -u mongodb -p mongodb --authenticationDatabase admin
>
> ~ use originaldb
 
# Postgres

## Postgres - 建立資料庫
```$ docker inspect [YOUR POSTGRESDB NAME]```

1. 查看 container 資訊，找出Networks.bridge.IPAddress
2. 點擊 "Add Server"
3. Name: [YOUR POSTGRES NAME]
4. Host name/address: [Networks.bridge.IPAddress]
5. Port: [YOUR POSTGRES PORT]
6. Maintenance database: [YOUR POSTGRES DATABASE NAME]
7. Username: [YOUR POSTGRES USERNAME]
8. Password: [YOUR POSTGRES USERPASSWORD]