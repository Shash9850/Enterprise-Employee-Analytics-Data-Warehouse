from managers.db_manager import DatabaseConnection


db = DatabaseConnection()
connection = db.connect()

print("Database connected:", connection.is_connected())
print("Database:", connection.database)

db.close()