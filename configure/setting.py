# ENV分为DEV（集成环境）、UAT（测试环境）、PROD（生产环境）
ENV = 'UAT'
user_uri = 'http://172.16.33.131:32000/#/login' if ENV == 'DEV' else 'http://172.16.33.131:30000/#/login' if ENV == 'UAT' else 'https://xxxxxxxx'
admin_uri = 'http://172.16.33.131:32001/#/login' if ENV == 'DEV' else 'http://172.16.33.131:30001/#/login' if ENV == 'UAT' else 'https://xxxxxxxx'

# one测试用户
users = [
    {"mobile": "18965125035","password": "qa123456!","message": "666888"},
    {"mobile": "18965816988","password": "qa123456!","message": "666888"},
    {"mobile": "15869164072","password": "qa123458!","message": "666888"}
]

adminUser = {"username": "admin","password":"1234567a"}

# oneBridge地址
bridgeURI = 'http://127.0.0.1:18080/one'

#数据库
host = '127.0.0.1'
username = 'root'
pwd = 'cpy123456!'
dbname = 'one'
port = 3306

#日志保留最近天数
days = 3

TASKCASES_PATH = r"C:\projects\oneCtl\taskCases.txt"
