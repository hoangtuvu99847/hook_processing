from src.producer import Producer
import mysql.connector
from src import MySQLConf

HOST = MySQLConf.HOST
USER = MySQLConf.USER
PASSWORD = MySQLConf.PASSWORD
DATABASE = MySQLConf.DB


def init_db():
    db = None
    try:
        db = mysql.connector.connect(
            host=HOST,
            user=USER,
            database=DATABASE,
            password=PASSWORD,
        )
        return db
    except Exception as ex:
        Producer().logger(type='ERROR', payload=str(ex))
        raise


class Server:
    db = init_db()

    def __init__(self) -> None:
        self.cursor = self.db.cursor(dictionary=True)

    def save(self, hostname, ip_address):
        query = """
            INSERT INTO server(hostname, ip_address)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE ip_address = %s,
                                    last_login=NOW();
            """
        val = (hostname, ip_address, ip_address)
        self.cursor.execute(query, val)
        self.db.commit()

        # print(self.cursor.rowcount, "record inserted.")
        # == > Change to write log running
        return True
