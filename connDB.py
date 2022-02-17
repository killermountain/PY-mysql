
import mysql.connector

class MySQLDB():

    def __init__(self):
        self.__connectDB()
        self.cursor = self.conn.cursor()        

    def __connectDB(self):
        self.conn = mysql.connector.connect(
        
        host="remotemysql.com",
        user="dcRNtOADDk",
        passwd="ioc5W4pQPO",
        database="dcRNtOADDk"

#         host="localhost",
#         port= "3306",
#         user="root",
#         passwd="",
#         database="pdfdb"
        )

    def getDocInfo(self):
        # query = "SELECT MAX(id) FROM "+ table_name +";"
        query = "SELECT COUNT(`id`), MAX(`id`) FROM `documents`;"
        self.cursor.execute(query)

        for x in self.cursor:
            return (x[0], x[1])

    def getAllDocs(self):
        query = "SELECT `id`,`name`,`hospital_name`,`keywords` FROM `documents`;"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def disconnectDB(self):
            self.conn.close()

