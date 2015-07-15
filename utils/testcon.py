import psycopg2

connection = psycopg2.connect('dbname=tycho2 user=postgres password=chess')

cursor = connection.cursor()

cursor.execute('select count(1) from hip_main')
row = cursor.fetchone()
print row[0]
