import mysql
from sellercreation.datamodel.db_connector import database_access
import logging
from sellercreation.configuration import log_config

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

class SPExecutor():
    def generateUniqueSellerCode(self):
        logger.addFilter(ClassNameFilter(self.__class__.__name__))
        connection = database_access()
        cursor = connection.cursor()
        try:
            # Call the stored procedure to generate a unique code
            logger.info("generating unique seller code")
            cursor.callproc("GenerateUniqueSellerCode")
            # Fetch the result (generated code) from the stored procedure
            result = None
            for result_cursor in cursor.stored_results():
                result = result_cursor.fetchone()
            if result:
                generated_code = result[0]
                logger.info("sp_GenerateUniqueSellerCode executed successfully !!")
                return generated_code
            else:
                print("No result returned from the stored procedure.")
            # Commit the changes (important)
            connection.commit()
        except mysql.connector.Error as err:
            logger.error(err)
        # Close the cursor and database connection
        cursor.close()
        connection.close()
