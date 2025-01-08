import redis
import json
from main import Messages

class Json:  ## Contains functions to pull database-related data from the config file.
    @staticmethod
    def pullDBIP():
        # Retrieve the database IP address from config.json
        with open("config.json") as config:
            configFile = json.load(config)  # Load JSON data from config file
            dataBaseIp = configFile.get("databaseIP")
            if not dataBaseIp:
                Messages.Errors.invalidJson()
                return False
            else:
                return dataBaseIp  # Return the database IP
    @staticmethod
    def pullDBPort():
        # Retrieve the database port from config.json
        with open ("config.json") as config:
            configFile = json.load(config)
            databasePort = configFile.get("dataBasePort")
            if not databasePort:
                Messages.Errors.invalidJson()
                return False
            else:
                return databasePort  # Return the database port

    def pullDBUser():
        # Retrieve the database username from config.json
        with open ("config.json") as config:
            configFile = json.load(config)
            databaseUser = configFile.get("databaseUser")
            if not databaseUser:
                Messages.Errors.invalidJson()
                return False
            else:  
                return databaseUser  # Return the database username

    def getDBPassword():
        # Prompt user to input their database password
        password = input("Please input your DB password:")
        if not password:
            Messages.Errors.errorMessage("Please input a password!")
        else:
            return password  

class Database:
    def connectToDataBase():
        try:
            host = Json.pullDBIP()
            port = Json.pullDBPort()
            redisConnection = redis.Redis(
                host=host,  # Database IP
                port=port,  # Database port
            )

            redisConnection.get("testkey") # Create a cursor to interact with the database
            return True
        except Exception as e:
            Messages.Errors.errorMessage(e)  # Handle any errors that occur during the connection
            return False