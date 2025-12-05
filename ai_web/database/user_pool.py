import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from database.pool import pool
from datetime import datetime
from log.log_util import logger


# 新增用户
def create_user(username, phone, password):
    create_time = datetime.now()
    insert_template = """
        insert into user(username, phone, password, create_time)
        values(%s, %s, %s, %s)
    """
    connection = pool.connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            insert_template,
            (username, phone, password, create_time)
        )
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

# 查询用户
def select_single_user(username):
    select_template = """
        select * from user where username = %s
    """
    connection = pool.connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            select_template,
            (username)
        )
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

# 查询所有用户，未分页操作,limit offset
def select_users():
    select_template = """
        select * from user
    """
    connection = pool.connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            select_template,
            ()
        )
        connection.commit()
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

# 修改,动态增加参数
def update_user(user_id, **kwargs):

    if not kwargs:
        return 0 

    set_clauses = []
    values = []
    for key, value in kwargs.items():
        set_clauses.append(f"{key} = %s")
        values.append(value)

    # 动态SQL
    sql = f"UPDATE user SET {', '.join(set_clauses)} WHERE id = %s"

    values.append(user_id)

    connection = pool.connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql, values)
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

# 删除用户
def delete_user(user_id):
    delete_template = """
        delete from user where id = %s
    """
    connection = pool.connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            delete_template,
            (user_id)
        )
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # result = select_single_user("zhangsan")
    # result = select_users()
    # result = create_user("test", "123456", "123456")
    # print(f"新增结果：{result}")
    result = delete_user(5)
    print(f"删除结果：{result}")



