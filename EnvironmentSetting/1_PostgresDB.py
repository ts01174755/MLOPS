import os

############################################## 建立postgresSQL ##############################################
# 安裝postgres
# >> https://medium.com/alberthg-docker-notes/docker%E7%AD%86%E8%A8%98-%E9%80%B2%E5%85%A5container-%E5%BB%BA%E7%AB%8B%E4%B8%A6%E6%93%8D%E4%BD%9C-postgresql-container-d221ba39aaec
# >> https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/AuroraUserGuide/babelfish-connect-PostgreSQL.html
# >> https://jimmyswebnote.com/postgresql-tutorial/
# >> https://juejin.cn/post/7132086527340871693

############################################## 拉postgres + PgAdmin4 映像檔 ##############################################
# 先 pull image
os.system("docker pull postgres")
os.system("docker pull dpage/pgadmin4") # 先 pull image
os.system('docker images') # 查看所有 image

############################################## 建立container ##############################################
# 建立 postgres container，設定 port 號，設定帳號與密碼
os.system(
    "docker create --name postgresdb \
    -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=postgres \
    postgres"
)
os.system("docker start postgresdb")

# 安裝 pgadmin4 UI
os.system(
    'docker run -p 5050:80 -e '
    '"PGADMIN_DEFAULT_EMAIL=pgadmin4@gmail.com" '
    '-e "PGADMIN_DEFAULT_PASSWORD=pgadmin4" '
    '-d dpage/pgadmin4'
) # 建立 container，設定 port 號，設定 pgadmin4 最高權限的登入密碼

############################################## 進入container ##############################################
os.system('docker exec -i postgresdb apt-get update') # 更新 apt-get
os.system('docker exec -i postgresdb apt-get install -y git') # 安裝 git
os.system('docker exec -i postgresdb bash -c "apt-get install make"') # 安裝 make
os.system('docker exec -i postgresdb bash -c "apt-get install gcc -y"') # 安裝 gcc
os.system('docker exec -i postgresdb bash -c "apt-get install postgresql-contrib -y"') # 安裝 postgresql-contrib
os.system('docker exec -i postgresdb bash -c "apt-get install postgresql-server-dev-15 -y"') # 安裝 postgresql-server-dev-15
os.system('docker exec -i postgresdb bash -c "cd usr/share/postgresql/15/contrib && git clone https://github.com/pgpartman/pg_partman.git"') # 下載 pg_partman, https://github.com/pgpartman/pg_partman
os.system('docker exec -i postgresdb bash -c "cd usr/share/postgresql/15/contrib/pg_partman && make install"') # 安裝 pg_partman, https://dbastreet.com/?p=1447
os.system('docker exec -i postgresdb bash -c "cd usr/share/postgresql/15/contrib/pg_partman && make installcheck"') # 測試 pg_partman

############################################## 建立DataBase & Table With Partition##############################################
os.system("docker exec -i postgresdb psql -U postgres -c \"create role postgresuser with login password 'postgresuser';\"") # 建立 postgresUser
os.system('docker exec -i postgresdb psql -U postgres -c "create database postgresdbuser owner postgresuser"') # 建立 postgresdb1
os.system('docker exec -i postgresdb psql -U postgres -d postgresdbuser -c "create schema userschema"')  # 建立 schema
os.system(
    'docker exec -i postgresdb psql -U postgres -d postgresdbuser -c "\
    create table userschema.userextract (\
        dt timestamp NOT NULL\
        , commondata1 char(50), commondata2 char(50), commondata3 char(50), commondata4 char(50), commondata5 char(50)\
        , commondata6 char(50), commondata7 char(50), commondata8 char(50), commondata9 char(50), commondata10 char(50)\
        , uniqueint1 int, uniqueint2 int, uniqueint3 int, uniqueint4 int, uniqueint5 int\
        , uniqueint6 int, uniqueint7 int, uniqueint8 int, uniqueint9 int, uniqueint10 int\
        , uniquefloat1 float, uniquefloat2 float, uniquefloat3 float, uniquefloat4 float, uniquefloat5 float\
        , uniquefloat6 float, uniquefloat7 float, uniquefloat8 float, uniquefloat9 float, uniquefloat10 float\
        , uniquestring1 text, uniquestring2 text, uniquestring3 text, uniquestring4 text, uniquestring5 text\
        , uniqueJSON json\
    )PARTITION BY RANGE(dt)"'
)  # 建立 Table, https://docs.postgresql.tw/the-sql-language/ddl/table-partitioning#5.11.5.-partitioning-and-constraint-exclusion

# 使用pg_partman建立分區表
os.system('docker exec -i postgresdb psql -U postgres -d postgresdbuser -c "create extension pg_partman"') # 建立 pg_partman, chrome-extension://noogafoofpebimajpfpamcfhoaifemoa/suspended.html#ttl=%E4%BD%BF%E7%94%A8%20pg_partman%20%E6%93%B4%E5%85%85%E5%8A%9F%E8%83%BD%E4%BE%86%E7%AE%A1%E7%90%86%20PostgreSQL%20%E5%88%86%E5%89%B2%E5%8D%80%20-%20Amazon%20Relational%20Database%20Service&pos=0&uri=https://docs.aws.amazon.com/zh_tw/AmazonRDS/latest/UserGuide/PostgreSQL_Partitions.html#PostgreSQL_Partitions.enable
os.system(
    'docker exec -i postgresdb psql -U postgres -d postgresdbuser -c \
    "select create_parent(\'userschema.userextract\', \'dt\', \'native\', \'daily\', p_start_partition := \'2021-01-01\')"\
    '
) # 建立分區表

############################################## PgAdmin4 Setting ##############################################
# 連postgresdb
os.system('docker inspect postgresdb') # 查看 container 資訊，找出Networks.bridge.IPAddress
os.system('open http://localhost:5050/')
# >> 點擊 "Add Server"
# >> Name: postgresdb
# >> Host name/address: {Networks.bridge.IPAddress}
# >> Port: 5432
# >> Maintenance database: postgres
# >> Username: postgres
# >> Password: postgres

# 下一步：建立DataBase    [V]
# 下一步：建立Table       [X]
# 下一步：建立Table欄位    [X]
# 下一步：建立Table欄位的資料型態 [X]
# 下一步：建立測試資料        [X]

############################################## PostgreSQL 指令 ##############################################
# 建立 postgres DataBase
# os.system('docker exec postgresdb psql --help') # 查看 psql 指令
# os.system('docker exec postgresdb psql -V') # 查看版本
# os.system('docker exec -i postgresdb psql -U postgres -c "\l"') # 查看所有資料庫
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "create table userextract (id int, name varchar(20))"')  # 建立 Table
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "alter table userextract add column age int"') # 建立 Table欄位
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "alter table userextract alter column age type varchar(20)"') # 修改 Table欄位的資料型態
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "insert into userextract values (1, \'test1\', \'20\')"') # 新增 Table欄位的資料
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "\d"') # 查看所有 Table
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "\d userextract"') # 查看 userextract 的所有欄位
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "select column_name, data_type from information_schema.columns where table_name = \'userextract\'"') # 查看 userextract 的所有欄位的資料型態
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "select * from userextract"') # 查看 userextract 的所有資料
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "alter table userextract drop column age"') # 刪除 Table欄位
# os.system('docker exec -i postgresdb psql -U postgres -d postgresdbtest -c "drop table userextract"') # 刪除 Table
# os.system('docker exec -i postgresdb psql -U postgres -c "drop database postgresdbtest"') # 刪除 DataBase



