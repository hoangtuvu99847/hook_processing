import mysql.connector


def init():
    db = None
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            database='hook_processing',
            password='',

        )
        return db
    except Exception as ex:
        print('DB: -> ', ex)


class Server:
    db = init()

    def __init__(self) -> None:
        self.cursor = self.db.cursor(dictionary=True)

    def all(self):
        query = """
        SELECT * FROM server
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        rows = [row for row in result]
        return rows

    def save(self, hostname, ip_address):
        try:
            query = """
            INSERT INTO server(hostname, ip_address)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE ip_address = %s,
                                    last_login=NOW();
            """
            val = (hostname, ip_address, ip_address)
            self.cursor.execute(query, val)
            self.db.commit()

            print(self.cursor.rowcount, "record inserted.")
            return True
        except Exception as ex:
            print('Server :: save --> ERROR: ', ex)


if __name__ == "__main__":
    Server().all()
