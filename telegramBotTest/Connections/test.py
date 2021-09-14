import psycopg2

connection = psycopg2.connect(dbname = "telegrambotinfodb", user = "postgres", password = "qwerty", host = "127.0.0.1", port = "5432")
print(connection)
