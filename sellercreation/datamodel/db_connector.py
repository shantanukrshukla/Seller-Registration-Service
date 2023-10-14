import mysql.connector
import configparser
from sellercreation.configuration.resource_encryption import FileDecrpytor

# Get the path to the directory where this scripts is located
#current_directory = os.path.abspath(os.path.dirname(__file__))
#datasync_directory = os.path.join(current_directory, '..', '..', 'sellercreation')
# Specify the path to the config.ini file
#config_file_path = os.path.join(datasync_directory, "resource/config.ini")

# Create a ConfigParser instance and read the config.ini file
config = configparser.ConfigParser()
#config.read(config_file_path)
decrypt_instance = FileDecrpytor()
conn = decrypt_instance.filedecrypt().decode('utf-8')
config.read_string(conn)

# Get database credentials from the config.ini file
db_host = config.get('database', 'db_host')
db_port = config.get('database', 'db_port')  # New line
db_user = config.get('database', 'db_user')
db_password = config.get('database', 'db_password')
db_name = config.get('database', 'db_name')

def database_access():
    mydb = mysql.connector.connect(
        host=db_host,
        port=db_port,  # Updated line
        user=db_user,
        password=db_password,
        database=db_name
    )
    return mydb