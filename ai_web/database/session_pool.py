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

class session:
    def __init__(self):
        pass

    # 新增会话窗口
    def create_session(self, title, username):

        connect = pool.connection()
        cursor = connect.cursor()

        insert_template = """
            insert into session(username, title, session_id, create_time)
            values(%s, %s, %s, %s)
        """
        try:
            session_id = uuid.uuid4().hex 
            cursor.execute(
                insert_template,
                (username, title, session_id, datetime.now())
            )
            connect.commit()

            return session_id
        except Exception as e:
            connect.rollback()
            raise e
        finally:
            cursor.close()
            connect.close()
    
    # 修改会话title
    def update_title(self, session_id, title):
        
        connect = pool.connection()
        cursor = connect.cursor()

        update_template = """
            UPDATE session SET title = %s WHERE session_id = %s
        """

        try:
            cursor.execute(
                update_template,
                (title, session_id)
            )
            connect.commit()
            return "修改成功"
        
        except Exception as e:
            connect.rollback()
            raise e
        finally:
            cursor.close()
            connect.close()
    
    # 获取单个用户的所有会话
    def get_sessions(self, username):
        connect = pool.connection()
        cursor = connect.cursor()

        select_template = """
            SELECT *
            FROM session
            where username = %s
            ORDER BY id ASC;
        """

        try:
            cursor.execute(
                select_template,
                (username)
            )
            return cursor.fetchall()
        except Exception as e:
            logger.info("查询失败：%s", e)
            raise e
        finally:
            cursor.close()
            connect.close()
    
    # 删除会话
    def delete_session(self, session_id):

        delete_template = """
            DELETE FROM session WHERE session_id=%s
        """

        connect = pool.connection()
        cursor = connect.cursor()

        try:
            cursor.execute(
                delete_template, (session_id,)
            )
            connect.commit()
            return cursor.rowcount

        except Exception as e:
            connect.rollback()
            logger.error("删除会话失败：%s", e)
            raise e

        finally:
            cursor.close()
            connect.close()

if __name__ == "__main__":

    s = session()
    # print(s.create_session("新聊天记录", "lisi"))
    # print(s.delete_session("d277f9a22b0c4bc09d648c94e31475eb"))
    # print(s.update_title("c3dcb46d4c19471db1a4a08f1ce869dd", "update_title"))
