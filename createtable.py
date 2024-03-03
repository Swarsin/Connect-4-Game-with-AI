import sqlite3 as sql

connect = sql.connect("test.db")

cursor = connect.cursor()

# cursor.execute("""
#     CREATE TABLE user (
#                username TEXT PRIMARY KEY,
#                wins INTEGER
#     )
#             """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("randomguy", 8)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("randomguy2", 82)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("swaraj singh", 2)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("who am i", 23)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("sdiofj", 86)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("ftyjk", 282)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("e12e21", 34)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("nfowmo", 125)
               """)
cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("ocwenweo", 234)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("vmwop", 25)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("odneqmfiopwe", 14)
               """)

cursor.execute("""
INSERT INTO user (username, wins)
VALUES ("cmpiwe", 24)
               """)

cursor.execute("""
               SELECT username, wins 
               FROM user
               """)

rows = cursor.fetchall()

list = [(row[0], row[1]) for row in rows]

connect.close()

print(list)