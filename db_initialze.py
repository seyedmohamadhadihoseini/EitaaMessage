import db_manager
sql_command = "CREATE DATABASE mydatabase; USE mydatabase; CREATE TABLE mytable (id INT PRIMARY KEY);"
result =db_manager.db_manager.execute(sql_command)