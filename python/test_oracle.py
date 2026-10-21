
import oracledb

username = "SYSTEM"
password = input("Enter your Oracle password: ")

connection = oracledb.connect(
    user=username,
    password=password,
    dsn="localhost:1522/freepdb1"
)

print("Oracle connected successfully!")

connection.close()
