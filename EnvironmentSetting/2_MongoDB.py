import os

############################################## 拉MongoDB + MongoExpress 映像檔 ##############################################
# 安裝MonogoDB
# >> https://www.runoob.com/docker/docker-install-mongodb.html # docker mongo 普通方法（但有bug 請見下一個除bug連結
# >> https://www.cnblogs.com/Can-daydayup/p/16796034.html # mongo 指令找不到的出錯解法
# >> https://www.minglunwu.com/notes/2021/mongodb_plus_express.html # mongo-express + MongoDB教學

# 先 pull image
# os.system("docker pull mongo:latest")
# os.system('docker pull mongo-express:latest')
# os.system('docker images') # 查看所有 image

# 建立網路
# os.system('docker network rm mongo-net')
# os.system('docker network create -d bridge mongo-net')
# os.system('docker network ls')

############################################## 建立container ##############################################
# 建立 mongodb container，設定 port 號
# os.system('rm -r /Users/wupeiyu/DataBase')
# os.system('mkdir /Users/wupeiyu/DataBase')
# os.system('mkdir /Users/wupeiyu/DataBase/MongoDB')
# os.system(
#     'docker create --name mongodb \
#     -e MONGO_INITDB_ROOT_USERNAME=mongoAdmin \
#     -e MONGO_INITDB_ROOT_PASSWORD=mongoPassword \
#     -p 27017:27017 \
#     --network mongo-net \
#     -v /Users/wupeiyu/DataBase:/data/db \
#     mongo'
# )
# os.system("docker start mongodb") # 啟動 mongodb
# os.system('docker exec -i mongodb mongosh admin -c "db.auth("mongoAdmin", "mongoPassword")"') # 登入mongoDB

# 建立 mongo-express container，設定 port 號
# os.system(
#     'docker create --name mongo_express \
#     --network mongo-net \
#     -e ME_CONFIG_MONGODB_SERVER=mongodb \
#     -e ME_CONFIG_MONGODB_ADMINUSERNAME=mongoAdmin \
#     -e ME_CONFIG_MONGODB_ADMINPASSWORD=mongoPassword \
#     -e ME_CONFIG_BASICAUTH_USERNAME=mongoUser \
#     -e ME_CONFIG_BASICAUTH_PASSWORD=mongoUserPassword \
#     -p 8081:8081 \
#     mongo-express'
# )
# os.system("docker start mongo_express") # 啟動 mongo_express
# os.system('docker ps -a') # 查看所r有 container

# 打開MongoDB-GUI
# os.system('open http://localhost:8081/')
