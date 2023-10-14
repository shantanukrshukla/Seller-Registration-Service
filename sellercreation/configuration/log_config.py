import logging
import os

# Use a global variable to keep track of whether logging is already configured
logging_configured = False

current_directory = os.path.abspath(os.path.dirname(__file__))
sellercreation_directory = os.path.join(current_directory, '..', '..', 'sellercreation/logs')


def configure_logging():
    global logging_configured

    # Check if logging is already configured to avoid duplication
    if not logging_configured:
        # Ensure the log directory exists or create it if it doesn't
        os.makedirs(sellercreation_directory, exist_ok=True)

        # Create the logger only if it's not configured yet
        logger = logging.getLogger("kuberCart")
        logger.setLevel(logging.DEBUG)  # Set the logger level

        console_handler = logging.StreamHandler()
        log_file_path = os.path.join(sellercreation_directory, "sellercreation.log")
        file_handler = logging.FileHandler(log_file_path)

        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        # Create a custom log format that includes the class name
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - [%(classname)s] - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the custom formatter to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logging_configured = True

    return logging.getLogger("kuberCart")
