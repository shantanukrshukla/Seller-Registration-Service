import configparser
import threading
from flask_restful import Resource, reqparse
import os
import logging
from sellercreation.configuration.resource_encryption import FileDecrpytor
from sellercreation.configuration import log_config
from sellercreation.datamodel.db_connector import database_access
from sellercreation.sp_executor.sp_executor import SPExecutor
#from app.mail_alert import welcome_mail


# Create a ConfigParser instance and read the config.ini file
config = configparser.ConfigParser()

#config.read(config_file_path)
decrypt_instance = FileDecrpytor()
conn = decrypt_instance.filedecrypt().decode('utf-8')
config.read_string(conn)
db_table_name = config.get('database', 'db_table_name')

# Logging initialization
logger = log_config.configure_logging()

# Create a custom filter to add the class name to the log record
class ClassNameFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__()
        self.class_name = name
    def filter(self, record):
        record.classname = self.class_name
        return True

class SellerValidation():
    current_directory = os.path.abspath(os.path.dirname(__file__))
    sellercreation_directory = os.path.join(current_directory, '..', '..', 'sellercreation')
    sellerValidation = os.path.join(sellercreation_directory, "scripts/sellerValidation.sql")
    sellerCreation = os.path.join(sellercreation_directory, "scripts/sellerCreation.sql")
    TABLE_NAME = db_table_name
    def __init__(self, username):
        self.username = username

    @classmethod
    def find_by_email_and_phone(cls, email, phone):
        logger.addFilter(ClassNameFilter(__class__.__name__))
        logger.info("Making a connection to the database")
        connection = database_access()
        cursor = connection.cursor()
        with open(SellerValidation.sellerValidation, 'r') as sql_file:
            query = sql_file.read()
            logger.info("Checking if a seller with the given email and phone number exists in our database")
            query = query.format(table=cls.TABLE_NAME)
            logger.info("query = {}".format(query))
            cursor.execute(query, (email, phone,))
            row = cursor.fetchone()
            if row:
                logger.info("Seller found, returning info")
                user = row
            else:
                user = None
        connection.close()
        return user

    @classmethod
    def find_by_username(cls, username):
        logger.addFilter(ClassNameFilter(__class__.__name__))
        logger.info("making connection with database")
        connection = database_access()
        cursor = connection.cursor()
        with open(SellerValidation.sellerValidation, 'r') as sql_file:
            query = sql_file.read()
            logger.info("checking if seller is present in our database or not !!")
            query = query.format(table=cls.TABLE_NAME)
            logger.info(query)
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                logger.info("user found, returning info")
                user = row
            else:
                user = None
        connection.close()
        return user


class SellerRegistration(Resource):
    TABLE_NAME = db_table_name
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('firstName', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('lastName', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('phone', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('address', type=str, required=True, help="This field cannot be left blank!")
    # Create a logger for the thread
    def post(self):
        logger.addFilter(ClassNameFilter(__class__.__name__))
        logger.info(f"Thread {threading.current_thread().name}: Registering seller")
        data = SellerRegistration.parser.parse_args()
        if SellerValidation.find_by_email_and_phone(data['email'],data['phone']):
            logger.error("User with that username already exists")
            return {"message": "User with that username already exists."}, 400
        # Perform seller registration in a separate thread
        registration_thread = threading.Thread(target=self.register_seller, args=(seller_id, data))
        registration_thread.start()
        return {"message": "Seller's account creation process started."}, 201

    def register_seller(self, data):
        connection = database_access()
        cursor = connection.cursor()
        generateUniqueSellerCode = SPExecutor()
        seller_id = generateUniqueSellerCode.generateUniqueSellerCode()
        with open(SellerValidation.sellerCreation, 'r') as sql_file:
            logger.info("Inserting a new seller account into our database")
            query = sql_file.read()
            query = query.format(table=self.TABLE_NAME)
            cursor.execute(query, (seller_id, data['username'], data['password'], data['email'], data['phone'], data['address'], data['firstName'], data['lastName']))
            connection.commit()
        connection.close()
        logger.info("Seller's account has been created successfully")