import psycopg2

mydb = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "rasputin",
    database = "postgres"
)
            
mydb.autocommit = True
myCursor = mydb.cursor()

try:
    myCursor.execute("SELECT datname FROM pg_database")
    for x in myCursor:
        print(x)
except Exception as e:
    print(f'Error: {e}')

myCursor.close()
mydb.close()