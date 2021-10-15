import mysql.connector
from src import MySQLConf

HOST = MySQLConf.HOST
USER = MySQLConf.USER
PASSWORD = MySQLConf.PASSWORD
DATABASE = MySQLConf.DB


class DB:
    """Init connection MYSQL db"""
    db = mysql.connector.connect(
        host=HOST,
        user=USER,
        database=DATABASE,
        password=PASSWORD,
    )

    def __init__(self) -> None:
        self.cursor = self.db.cursor(dictionary=True)


class Server(DB):
    def __init__(self) -> None:
        super().__init__()

    def save(self, hostname, ip_address):
        query = """
            INSERT INTO server(hostname, ip_address)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE ip_address = %s,
                                    last_login=NOW();
            """
        val = (hostname, ip_address, ip_address)
        self.cursor.execute(query, val)

        # == > Change to write log running
        return self.cursor.lastrowid


class CPU(DB):
    def __init__(self) -> None:
        super().__init__()

    def save(self, server_id, data):
        query = """
        INSERT INTO cpu(server_id, data)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE data = %s
        """
        val = (server_id, data, data)
        self.cursor.execute(query, val)
