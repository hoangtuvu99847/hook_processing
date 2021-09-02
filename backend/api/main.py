from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import mysql.connector


load_dotenv()

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _init_db():
    mydb = mysql.connector.connect(
        host="35.240.161.144",
        user="vunv",
        password="Vu@1479825",
        database="hook_processing"
    )
    return mydb


@app.get("/")
def list():
    try:
        db = _init_db()
        cursor = db.cursor(dictionary=True)

        sql = """
        SELECT * FROM server WHERE status = 1
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    except Exception as ex:
        print("get_list_server: ", ex)


@app.get("server/{id}")
def detail():
    pass


if __name__ == '__main__':
    uvicorn.run('main:app', port=int(PORT), reload=True, host=HOST)
