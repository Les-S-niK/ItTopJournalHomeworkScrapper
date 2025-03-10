
## Built-in modules: ##
from typing import Callable
from functools import wraps
from time import time
from os import PathLike

## Pip modules: ##
from loguru import logger

## Local modules: ##
from config import current_dir_path


LOGGER_PATH: PathLike = f"{current_dir_path}/LOGS.log"

logger.add(
    sink=LOGGER_PATH,
    colorize=True,
    level="DEBUG",
    compression="zip",
    rotation="1 MB"
)
logger.info(f"Logger was initialized. Logs path: {LOGGER_PATH}")


def folder_manager_logger(function: Callable) -> Callable:
    """Folder manager logger to logging files creation.

    Args:
        function (Callable): folder manager method.

    Returns:
        Callable: Wrapper function.
    """
    @wraps(function)
    def wrapper(*args, **kwargs) -> None:
        """Folder manager method wrapper."""
        start_time: float = time()
        logger.debug(f"\n>>> Running FolderManager method {function.__name__}... <<<")
        
        try:
            function(*args, **kwargs)
            end_time: float = time() - start_time
            logger.debug(f"""\n>>> Succesful file creation from {function.__name__}. 
                Took time: {round(end_time, 2)} sec. <<<
            """)
        
        except Exception as error:
            logger.error(f">>>\n An error was occured in FolderManager method {function.__name__}. \n Error: {error}. <<<")
            raise Exception(error)
    
    return wrapper


def request_logger(function: Callable) -> Callable:
    """Request logger for logging the requests to Journal API.

    Args:
        function (Callable): request method.

    Returns:
        Callable: Wrapper function.
    """
    @wraps(function)
    def wrapper(*args, **kwargs) -> dict:
        """Request method wrapper, logging the request and returns the response.

        Returns:
            dict: response.json object.
        """
        start_time: float = time()
        logger.debug(f"\n>>> Running request {function.__name__}... <<<")
        try:
            json_response: dict = function(*args, **kwargs)
            end_time: float = time() - start_time
            logger.debug(f"""\n>>> Succesful response from {function.__name__}. 
                Took time: {round(end_time, 2)} sec. <<<
            """)
            
            return json_response
        
        except Exception as error:
            logger.critical(f">>>\n An error was occured in {function.__name__} request. \n Error: {error}. <<<")
            raise Exception(error)
    
    return wrapper