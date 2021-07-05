from fastapi import FastAPI
import sqlite3

app = FastAPI()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _init():
    connection = sqlite3.connect('../hookprocessing.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    return cursor


@app.get("/")
def list():
    try:
        cursor = _init()
        sql = """SELECT * FROM server WHERE status = 1"""
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    except Exception as ex:
        print("get_list_server: ", ex)


@app.get("server/{id}")
def detail():
    pass
