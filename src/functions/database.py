import redis
import json
from main import Messages

# The Json class contains static methods to retrieve database configuration values from a JSON file.
class Json:
    @staticmethod
    def pullDBIP():
        # Retrieve the database IP address from config.json
        with open("config.json") as config:
            configFile = json.load(config)  # Load JSON data from config file
            dataBaseIp = configFile.get("databaseIP")  # Get the 'databaseIP' key value
            if not dataBaseIp:  # Check if the value is missing or None
                Messages.Errors.invalidJson()  # Log an error message for invalid JSON
                return False  # Return False indicating failure
            else:
                return dataBaseIp  # Return the database IP

    @staticmethod
    def pullDBPort():
        # Retrieve the database port from config.json
        with open("config.json") as config:
            configFile = json.load(config)  # Load JSON data from config file
            databasePort = configFile.get("dataBasePort")  # Get the 'dataBasePort' key value
            if not databasePort:  # Check if the value is missing or None
                Messages.Errors.invalidJson()  # Log an error message for invalid JSON
                return False  # Return False indicating failure
            else:
                return databasePort  # Return the database port

    def pullDBUser():
        # Retrieve the database username from config.json
        with open("config.json") as config:
            configFile = json.load(config)  # Load JSON data from config file
            databaseUser = configFile.get("databaseUser")  # Get the 'databaseUser' key value
            if not databaseUser:  # Check if the value is missing or None
                Messages.Errors.invalidJson()  # Log an error message for invalid JSON
                return False  # Return False indicating failure
            else:
                return databaseUser  # Return the database username

    def getDBPassword():
        # Prompt user to input their database password
        password = input("Please input your DB password:")  # Get password input from the user
        if not password:  # Check if the password is empty
            Messages.Errors.errorMessage("Please input a password!")  # Log an error message for empty password
        else:
            return password  # Return the user-provided password

# The Database class contains methods to connect to a Redis database and perform operations.
class Database:
    def connectToDataBase():
        # Establish a connection to the Redis database
        try:
            host = Json.pullDBIP()  # Retrieve the database IP
            port = Json.pullDBPort()  # Retrieve the database port
            redisConnection = redis.Redis(
                host=host,  # Specify the Redis host
                port=port,  # Specify the Redis port
            )

            redisConnection.get("testkey")  # Test the connection by retrieving a key
            return True  # Return True if the connection is successful
        except Exception as e:
            # Log any error that occurs during the connection attempt
            Messages.Errors.errorMessage(e)
            return False  # Return False indicating failure

    def addToDataBase(redisConnection, ip):
        # Add a key-value pair to the Redis database
        try:
            cmd = redisConnection.set("website", ip)  # Set the "website" key with the provided IP
        except Exception as e:
            # Log any error that occurs during the operation
            Messages.Errors.errorMessage(cmd)
