import psycopg2

conn = psycopg2.connect(
    user="revota", password="r3vot4", database="revota", host="localhost", port="5432"
)
cursor = conn.cursor()


# INSERT
# cursor.execute(
#     """
#     INSERT INTO accounts (id, username, email, password, created_on, last_login)
#     VALUES (NEXTVAL('id_sequence'), 'pinki', 'pinkidwinanta@gmail.com', 'dwinanta', CURRENT_DATE, CURRENT_DATE);
#     """
# )
# conn.commit()


# SELECT
# cursor.execute(
#     """
#     SELECT * FROM accounts;
#     """
# )
# result = cursor.fetchall()
# for a in result:
#     print(a)


# CREATE TABLE/SEQUENCE
# cursor.execute(
#     """
#     CREATE SEQUENCE id_sequence;
#     CREATE TABLE accounts (
#         id SERIAL PRIMARY KEY,
#         username VARCHAR(50) UNIQUE NOT NULL,
#         email VARCHAR(50) UNIQUE NOT NULL,
#         password VARCHAR(50) NOT NULL,
#         created_on TIMESTAMP NOT NULL,
#         last_login TIMESTAMP
#     );
#     """
# )
# conn.commit()
# conn.close()


# ALTER TABLE/SEQUENCE
# cursor.execute(
#     """
#     ALTER TABLE accounts ALTER COLUMN id SET DEFAULT NEXTVAL('id_sequence');
#     ALTER SEQUENCE id_sequence START WITH 2;
#     """
# )
# conn.commit()
# conn.close()


# DROP TABLE
# cursor.execute(
#     """
#     DROP TABLE accounts;
#     """
# )
# conn.commit()
# conn.close()