
## Built-in modules: ##
from dataclasses import dataclass
from typing import Any

## Pip modules: ##
from requests import Response, RequestException
from requests import get, post

## Local modules: ##
from journal_headers import get_headers_for_login, get_headers_for_requests
from journal_loggers import request_logger
from journal_headers import get_headers_for_downloads
from config import JOURNAL_LOGIN_URL


@dataclass
class UserInputData(object):
    """Dataclass to hold user authorization data"""
    APPLICATION_KEY: str
    ID_CITY: str 
    PASSWORD: str
    USERNAME: str

    def to_dict(self) -> dict[str, str]:
        return {
            "application_key": self.APPLICATION_KEY,
            "id_city": self.ID_CITY,
            "password": self.PASSWORD,
            "username": self.USERNAME,
        }


class JournalLoginTokenParser(object):
    """Parses access token from the public ItTopJournal API. Uses journal user accout data to 
    take the token"""
    def __init__(
        self,
        login_data: dict[str, str] | UserInputData,
    ) -> None:
        """Journal Parser initialization for parsing the data from the ItTopJournal API
        There will be a new self. attrs with parsed information from API. You can check all of them with self.parsed_attr_names.

        Args:
            login_data (dict[str, str] | UserInputData): dict object with 4 fields:
            You can get all of it in the JournalAPI. 
            https://journal.top-academy.ru/ru/auth/login/index
            
            APPLICATION_KEY = YOUR_APP_KEY
            ID_CITY = YOUR_ID_CITY (sometimes it can be "null").
            PASSWORD = YOUR_PASSWORD
            USER_NAME = YOUR_USERNAME
        """
        
        self.access_token: str = self._login_in_journal_api(login_data=login_data)
        self.headers: dict[str, str] = get_headers_for_requests(token=self.access_token) 

    @staticmethod
    def check_response_status(response: Response) -> None:
        """Check the response status. If the status is not in 200-299, it raises an exception.
        
        Args:
            response (Response): response object. You can get it after request to api.
        
        Raises: 
            RequestException: if response.status_code is not in range 200-299.
        """
        if not response.ok:
            raise RequestException(f"Failed to login in the JournalApi. Status code: {response.status_code}")

    @request_logger
    def _login_in_journal_api(self, login_data: dict) -> str:
        """Logging in the JournalApi with json data and get the token after login.

        Args:
            session (Session): requests.Session object.
            
        Returns:
            str: API token.
        """
        if isinstance(login_data, UserInputData):
            login_data: dict[str, str] = login_data.to_dict()
        
        login_headers: dict = get_headers_for_login()
        
        response: Response = post(
            url=JOURNAL_LOGIN_URL,
            headers=login_headers,
            json=login_data
        )
        self.check_response_status(response=response)
        
        ## Get the token from API response: ##
        TOKEN_DICT_KEY: str = "access_token"
        access_token: str = response.json().get(TOKEN_DICT_KEY)
        
        return access_token


class JournalHomeworkScrapper(object):
    """Scrapps all groups homework from the public ItTopJournal API."""
    def __init__(
        self,
        login_data: dict[str, str] | UserInputData,
    ) -> None:
        """Initialize the scrapper, getting access token from the ItTopJournal API.

        Args:
            login_data (dict[str, str] | UserInputData): dict object with 4 fields:
                You can get all of it in the JournalAPI. 
                https://journal.top-academy.ru/ru/auth/login/index
                
                APPLICATION_KEY = YOUR_APP_KEY
                ID_CITY = YOUR_ID_CITY (sometimes it can be "null").
                PASSWORD = YOUR_PASSWORD
                USER_NAME = YOUR_USERNAME
        """
        self._login_api_parser: JournalLoginTokenParser = JournalLoginTokenParser(
            login_data=login_data
        )
    
    @staticmethod
    def generate_homework_api_url(
        page: int,
        status: int,
        group_id: int
    ) -> str:
        """Generate the URL for requests to homework in the Journal API.

        Args:
            page (int): Homework page.
            status (int): Homework status (
                0-(unknown, probably practical works)
                1-completed,
                2-on the checking,
                3-uncompleted
                5-expired
            )
            group_id (int): homework group id.

        Returns:
            str: Generated url.
        """
        return f"https://msapi.top-academy.ru/api/v2/homework/operations/list?page={page}&status={status}&type=0&group_id={group_id}"

    def download_homework_file(self, file_url_path: str) -> tuple[str, bytes]:
        """Download a homework file from the Journal homework API.

        Args:
            file_url_path (str): path to the homework file.

        Returns:
            tuple[str, bytes]: file ext and bytes of downloaded file.
        """
        downloaded_file_response: Response = get(
            url=file_url_path,
            headers=get_headers_for_downloads()
        )
        self._login_api_parser.check_response_status(response=downloaded_file_response)
        
        CONTENT_DISPOSITION_TAG: str = "Content-Disposition"
        content_disposition: str = downloaded_file_response.headers.get(CONTENT_DISPOSITION_TAG)
        ## Get file extension from the content disposition in request. ## 
        file_ext: str = content_disposition.split("\"")[1].split(".")[-1]
        
        return (file_ext, downloaded_file_response.content)

    @request_logger
    def get_homeworks_from_api(
        self,
        page: int,
        status: int,
        group_id: int
    ) -> list[dict[str, Any]]:
        """Send a get request to the homework Journal API with parameters in the URL.

        Args:
            page (int): Homework page.
            status (int): Homework status (
                0-(unknown, probably practical works)
                1-completed,
                2-on the checking,
                3-uncompleted
                5-expired
            )
            group_id (int): homework group id.

        Returns:
            list[dict[str, Any]]: Json object with the homework.
        """
        url: str = self.generate_homework_api_url(
            page=page,
            status=status,
            group_id=group_id
        )
        response: Response = get(
            url=url,
            headers=self._login_api_parser.headers,
        )
        self._login_api_parser.check_response_status(response=response)
        
        return response.json()


