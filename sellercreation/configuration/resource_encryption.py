from cryptography.fernet import Fernet
import logging
from sellercreation.configuration import log_config
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
#init
current_directory = os.path.abspath(os.path.dirname(__file__))
logger = log_config.configure_logging()
encryption_key = os.environ.get('MYAPP_ENCRYPTION_KEY')

class FileDecrpytor():
    def filedecrypt(self):
        key = os.getenv("MYAPP_ENCRYPTION_KEY")
        fernet = Fernet(key)
        sellercreation_directory = os.path.join(current_directory, '..', '..', 'sellercreation')
        # Specify the path to the config.ini file
        config_file_path = os.path.join(sellercreation_directory, "resource")
        # Decrypt the file when needed
        with open(f'{config_file_path}/config.ini.encrypted', "rb") as encrypted_file:
            print(current_directory)
            decrypted_data = fernet.decrypt(encrypted_file.read())
        return decrypted_data

# Create a custom filter to add the class name to the log record
class ClassNameFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__()
        self.class_name = name

    def filter(self, record):
        record.classname = self.class_name
        return True

class ResourceEncrypt():
    # Generate an encryption key and save it securely
    def generateKey(self):
        key = Fernet.generate_key()
        with open(f"{current_directory}/.env", "w") as key_file:
            key_file.write(f"MYAPP_ENCRYPTION_KEY={key.decode('utf-8')}")
        return key
    def resourceEncrypt(self):
        logger.addFilter(ClassNameFilter(self.__class__.__name__))
        sellercreation_directory = os.path.join(current_directory, '..', '..', 'sellercreation')
        # Specify the path to the config.ini file
        config_file_path = os.path.join(sellercreation_directory, "resource")
        key = self.generateKey()
        fernet = Fernet(key)
        with open(f'{config_file_path}/config.ini', "rb") as config_file:
            encrypted_data = fernet.encrypt(config_file.read())
        with open(f'{config_file_path}/config.ini.encrypted', "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
            os.remove(f'{config_file_path}/config.ini')

if __name__ == '__main__':
    instance = ResourceEncrypt()
    instance.resourceEncrypt()



