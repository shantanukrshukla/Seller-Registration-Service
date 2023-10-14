import logging
from sellercreation.configuration import log_config
import configparser
import os
from sellercreation.configuration.resource_encryption import FileDecrpytor

#init
current_directory = os.path.abspath(os.path.dirname(__file__))
logger = log_config.configure_logging()

# Create a custom filter to add the class name to the log record
class ClassNameFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__()
        self.class_name = name

    def filter(self, record):
        record.classname = self.class_name
        return True

class Main():
    def main(self):
        logger.addFilter(ClassNameFilter(self.__class__.__name__))
        config = configparser.ConfigParser()
        decrypt_instance = FileDecrpytor()
        conn = decrypt_instance.filedecrypt().decode('utf-8')
        config.read_string(conn)
        log_content = """
        K   K  U   U  BBBB  EEEE  RRRR   CCCC  A   RRRR   TTTTT
        K  K   U   U  B   B E     R   R C     A A  R   R    T  
        KK     U   U  BBBB  EEEE  RRRR  C     AAA  RRRR     T  
        K  K   U   U  B   B E     R  R  C     A  A R  R     T  
        K   K   UUU   BBBB  EEEE  R   R  CCCC A   A R   R    T  
        """
        version = config.get('version', 'version')
        logger.info(log_content)
        logger.info("starting seller creation service")
        logger.info("deployed version - {}".format(version))