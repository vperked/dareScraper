import mysql.connector
import json
from main import Messages
class Json: ## Pretty much contains the same function pulling different data, im not gonna bother noting all of it.
    def pullDBIP():
        with open("config.json") as config:
            configFile = json.load(config)
            dataBaseIp = configFile["databaseIP"]
            return dataBaseIp
    def pullDBPort():
        with open ("config.json") as config:
            configFile = json.load(config)
            databasePort = configFile["databasePort"]
            return databasePort
    def pullDBUser():
        with open ("config.json") as config:
            configFile = json.load(config)
            databaseUser = configFile["databaseUser"]
            return databaseUser
    def getDBPassword():
        password = input("Please input your mySQL DB password:") # Grabs the user input 
        return password # Returns the password
 
 
class Database:
    def connectToDataBase():
        try:
            connection = mysql.connector.connect(
            host=Json.pullDBIP(),
            port=Json.pullDBPort(),
            user=Json.pullDBUser(),
            password=Json.getDBPassword()
    )
            cursor = connection.cursor()
        except Exception as e:
            Messages.Errors.errorMessage(e)
    def showDataBase(cursor):
       cmd = cursor.execute("SHOW DATABASES")
       for x in cursor:
           Messages.Errors.sucessMessage(cmd)
           Messages.Errors.sucessMessage(x)


