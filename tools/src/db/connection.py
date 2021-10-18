import mysql.connector
from src.config import MySQLConf

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
