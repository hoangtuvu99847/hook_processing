from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import mysql.connector

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
        host="10.130.64.113",
        user="vunv79",
        password="Vu@1479825",
        database="hook_processing"
    )
    return mydb


@app.get("/")
def list_server():
    db = _init_db()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT * FROM server WHERE status = 1
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


@app.get("/server/cpu/{server_id}")
def get_cpu_info(server_id):
    db = _init_db()
    cursor = db.cursor(dictionary=True)
    sql = """
        SELECT *
        FROM cpu
                JOIN server s on s.id = cpu.server_id
        WHERE server_id = %s
    """
    val = (server_id,)
    cursor.execute(sql, val)
    cpu_server = cursor.fetchone()
    if cpu_server.get('data'):
        cpu_server['data'] = cpu_server['data'].split(',')
    return cpu_server


@app.get("/server/{_id}")
def detail(_id):
    db = _init_db()
    cursor = db.cursor(dictionary=True)
    sql = """
        SELECT * FROM server WHERE id = %s
    """
    val = (_id,)
    cursor.execute(sql, val)
    server = cursor.fetchone()
    return server


if __name__ == '__main__':
    uvicorn.run('main:app', port=int(PORT), reload=True, host=HOST)
