import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
class db_manager:
    def __init__(self) -> None:
        self.history=[]
    def getNewBucket(self):
        result= int(self.execute("SELECT increment_last_bucket();"))
        self.history.append(result)
        return result
    def execute(self,sql_command):
        with mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"), 
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQL_PORT")
            
            ) as mydb:
            with mydb.cursor(buffered=True) as cursor:
                cursor.execute(sql_command)
                result = cursor.fetchone()[0]

                mydb.commit()
        return result
db_manager()