from dbutils.pooled_db import PooledDB
import pymysql
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from datetime import datetime
import threading
from log.log_util import logger
from pool import pool
import uuid

class chat_message:
    def __init__(self):
        pass

    # 插入聊天数据
    def insert_message(self, user_msg, ai_msg, session_id, username):

        connect = pool.connection()
        cursor = connect.cursor()

        insert_template = """
            insert into chat_message(username, role, message, create_time, session_id, pair_id)
            values(%s, %s, %s, %s, %s, %s)
        """
        try:
            #这块pair_id，加上，方便后续同时删掉问题和答案
            pair_id = uuid.uuid4().hex 
            # 存储human
            cursor.execute(
                insert_template,
                (username, "Human", user_msg, datetime.now(), session_id, pair_id)
            )

            # 存储ai
            cursor.execute(
                    insert_template,
                    (username, "AI", ai_msg, datetime.now(), session_id, pair_id)
            )
            connect.commit()
        except Exception as e:
            connect.rollback()
            raise e
        finally:
            cursor.close()
            connect.close()
    
    # 获取单个会话历史记录
    def get_session_message(session_id):
        connect = pool.connection()
        cursor = connect.cursor()

        # 根据id排，因为id是自增、且插入的时候是先插human再插ai，所以id是human的先
        select_template = """
            SELECT *
            FROM chat_message
            WHERE session_id = %s
            ORDER BY id ASC;
        """

        try:
            cursor.execute(
                select_template,
                (session_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            logger.info("查询失败：%s", e)
            raise e
        finally:
            cursor.close()
            connect.close()
    
    # 删除一对问答消息，只要点击删除其中一条，就直接按照pair，全删除掉
    def delete_message(pair_id):

        delete_template = """
            DELETE FROM chat_message WHERE pair_id=%s
        """

        connect = pool.connection()
        cursor = connect.cursor()

        try:
            cursor.execute(
                delete_template, (pair_id,)
            )
            connect.commit()
            return cursor.rowcount

        except Exception as e:
            connect.rollback()
            logger.error("删除对话对失败：%s", e)
            raise e

        finally:
            cursor.close()
            connect.close()




if __name__ == "__main__":

    chat = chat_message()
    chat.insert_message("user_msg", "ai_msg", "session_id", "username")