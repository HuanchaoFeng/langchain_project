from dbutils.pooled_db import PooledDB
import pymysql
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_CHATSET, MYSQL_MESSAGE_TABLE, MYSQL_SESSION_TABLE

# 连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=10,      
    mincached=2,            
    maxcached=5,            
    blocking=True,          
    host = MYSQL_HOST,
    port = MYSQL_PORT,
    user = MYSQL_USER,
    password = MYSQL_PASS,
    database = MYSQL_DATABASE,
    charset = MYSQL_CHATSET
)
