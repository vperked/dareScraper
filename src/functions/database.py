import mysql.connector
import json
from main import Messages

class Json:  ## Contains functions to pull database-related data from the config file.
    def pullDBIP():
        # Retrieve the database IP address from config.json
        with open("config.json") as config:
            configFile = json.load(config)  # Load JSON data from config file
            dataBaseIp = configFile["databaseIP"]
            return dataBaseIp  # Return the database IP

    def pullDBPort():
        # Retrieve the database port from config.json
        with open ("config.json") as config:
            configFile = json.load(config)
            databasePort = configFile["databasePort"]
            return databasePort  # Return the database port

    def pullDBUser():
        # Retrieve the database username from config.json
        with open ("config.json") as config:
            configFile = json.load(config)
            databaseUser = configFile["databaseUser"]
            return databaseUser  # Return the database username

    def getDBPassword():
        # Prompt user to input their MySQL database password
        password = input("Please input your mySQL DB password:")
        return password  # Return the entered password

class Database:
    def connectToDataBase():
        try:
            # Establish a connection to the MySQL database using credentials from the Json class
            connection = mysql.connector.connect(
                host=Json.pullDBIP(),  # Database IP
                port=Json.pullDBPort(),  # Database port
                user=Json.pullDBUser(),  # Database user
                password=Json.getDBPassword()  # Database password
            )
            cursor = connection.cursor()  # Create a cursor to interact with the database
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle any errors that occur during the connection

    def showDataBase(cursor):
        # Show a list of all databases on the MySQL server
        cmd = cursor.execute("SHOW DATABASES")
        for x in cursor:  # Iterate through the result set
            Messages.Errors.sucessMessage(cmd)  # Print the command executed (if needed for debugging)
            Messages.Errors.sucessMessage(x)  # Print each database name
