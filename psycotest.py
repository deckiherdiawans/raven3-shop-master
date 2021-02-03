import psycopg2

conn = psycopg2.connect(
    user="revota",
    password="r3vot4",
    database="revota",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()


# CREATE TABLE/SEQUENCE
cursor.execute(
    """
    --CREATE SEQUENCE id_sequence;
    CREATE TABLE profiles (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL,
        created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP
    );
    """
)
conn.commit()


# DROP TABLE
# cursor.execute(
#     """
#     DROP TABLE accounts;
#     """
# )
# conn.commit()


# ALTER TABLE/SEQUENCE
# cursor.execute(
#     """
#     --ALTER TABLE profiles ALTER COLUMN id SET DEFAULT NEXTVAL('id_sequence');
#     ALTER SEQUENCE id_sequence RESTART WITH 1;
#     """
# )
# conn.commit()


# INSERT
# cursor.execute(
#     """
#     INSERT INTO profiles (id, username, email, password, created_on, last_login)
#     VALUES (NEXTVAL('id_sequence'), 'deckiherdiawans', 'd.herdiawan.s@gmail.com', 'H3r@w4t!', CURRENT_DATE, CURRENT_DATE);
#     """
# )
# conn.commit()


# INSERT MULTIPLE DATA
# cursor.execute(
#     """INSERT INTO profiles (id, username, email, password, created_on, last_login) VALUES (NEXTVAL('id_sequence'),'Choerul','choerulsofyan@yahoo.com','yahooyahoo',CURRENT_DATE,NULL)"""
# )
# cursor.execute(
#     """INSERT INTO profiles (id, username, email, password, created_on, last_login) VALUES (NEXTVAL('id_sequence'),'tiodinar','tiodinar@gmail.com','tiodinar',CURRENT_DATE,NULL)"""
# )
# cursor.execute(
#     """INSERT INTO profiles (id, username, email, password, created_on, last_login) VALUES (NEXTVAL('id_sequence'),'jakapandu','jakapeer@gmail.com','jprjpr',CURRENT_DATE,NULL)"""
# )
# conn.commit()
# print(cursor.rowcount, "are inserted successfully.")


# DELETE DATA FROM TABLE
# cursor.execute(
#     """
#     DELETE FROM profiles WHERE id = 4;
#     """
# )
# conn.commit()


# SELECT
# cursor.execute(
#     """
#     SELECT * FROM profiles;
#     """
# )
# result = cursor.fetchall()
# for a in result:
#     print(a)