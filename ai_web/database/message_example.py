# 这一块使用Mysql插入未使用线程池的方式，需要用全局锁来保证每个一个连接只能由一个线程执行，不加锁会导致A线程数据被B线程拿走

import pymysql
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_CHATSET, MYSQL_MESSAGE_TABLE, MYSQL_SESSION_TABLE
from datetime import datetime
import threading
from log.log_util import logger

# 全局锁
db_lock = threading.Lock()

connect = pymysql.connect(
    host = MYSQL_HOST,
    port = MYSQL_PORT,
    user = MYSQL_USER,
    password = MYSQL_PASS,
    database = MYSQL_DATABASE,
    charset = MYSQL_CHATSET
)

cursor = connect.cursor()


# 插入聊天数据
def insert_message(user_msg, ai_msg, session_id, username):

    insert_template = """
        insert into chat_message(username, role, message, create_time, session_id)
        values(%s, %s, %s, %s, %s)
    """
    with db_lock:
        try:
            # 存储human
            cursor.execute(
                insert_template,
                (username, "Human", user_msg, datetime.now(), session_id)
            )

            # 存储ai
            cursor.execute(
                insert_template,
                (username, "AI", ai_msg, datetime.now(), session_id)
            )
            
            connect.commit()
        except Exception as e:
            connect.rollback()
            logger.info("执行插入聊天记录操作错误：%s", e)
            raise e



