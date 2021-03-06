import sqlite3

# conn  = sqlite3.connect('db.sqlite')
# cure = conn.cursor()


# query = """
# CREATE TABLE answrs (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     msg TEXT,
#     answ TEXT
# )
# """
# cure.execute(query)
# conn.commit()

# query = """
# INSERT INTO answrs (msg, answ) VALUES
# ("/help", "Команды: \n
#     /say - возврат вашего сообщения \n
#     /relax - Спасибо, если выберите это \n
#     /wake up - не спасибо, если выберите это после relax"),
# ( "/say", "msg[5:]")
# """

# cure.execute(query)
# conn.commit()

def get(table_name, cols = "*"):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    "".format()

    query = """
        SELECT {1} FROM {0}
    """.format(table_name,  cols if cols=="*" else "({0})".format(",".join(cols)) )

    cur.execute(query)
    colNames = list(map(lambda x: x[0], cur.description))

    result = []

    for i in cur.fetchall():
        result.append(dict(zip(colNames, i)))
    db.close()

    return result

def insert(table_name, cols, data):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = """
        INSERT INTO {0}({1})
        VALUES('{2}');
    """.format(table_name, ",".join(cols), "','".join(data))

    cur.execute(query)

    db.commit()
    db.close()


# query="""
# SELECT * FROM answrs
# """
# cure.execute(query)
# conn.commit()
# print(cure.fetchall())
# conn.close()

db = sqlite3.connect('db.sqlite')
cur = db.cursor()

# query="""
# CREATE TABLE groups (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupName TEXT
# )
# """
# cur.execute(query)
# db.commit()

# query="""
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     groupid INTEGER,
#     FOREIGN KEY (groupid) REFERENCE groups (id) 
# )
# """
# cur.execute(query)
# db.commit()

# insert("groups", ["groupName"], ["Админы"])
# insert("groups", ["groupName"], ["Модеры"])
# insert("groups", ["groupName"], ["Холопы"])
print(get("groups"))
db.close()