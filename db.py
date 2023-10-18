import pymysql

dbHost = "localhost"
dbName = "asgr"
dbUsername = "python"
dbPass = "P^^th0n312"

conn = pymysql.connect(host=dbHost, user=dbUsername, password=dbPass, database=dbName, charset="utf8", autocommit=True)
c = conn.cursor()