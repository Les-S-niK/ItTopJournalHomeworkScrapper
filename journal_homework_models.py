
## Built-in modules: ##
from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Any

## Local modules: ##
from journal_requests import JournalHomeworkScrapper, UserInputData


@dataclass
class HomeworkModel:
    """Class for representing a model of homework."""
    status: int
    teacher_name: str
    subject_name: str
    file_url_path: str
    comment: str
    creation_time: datetime
    theme: str


class HomeworkAPI:
    """Class to interact with Journal API."""
    def __init__(self, login_data: dict[str, str] | UserInputData):
        """Initialize the Journal homeworks scrapper.

        Args:
            login_data (dict[str, str] | UserInputData): dict object with 4 fields:
            You can get all of it in the JournalAPI. 
            https://journal.top-academy.ru/ru/auth/login/index
            
            APPLICATION_KEY = YOUR_APP_KEY
            ID_CITY = YOUR_ID_CITY (sometimes it can be "null").
            PASSWORD = YOUR_PASSWORD
            USER_NAME = YOUR_USERNAME
        """
        self.journal_scrapper: JournalHomeworkScrapper = JournalHomeworkScrapper(login_data=login_data)

    def get_homeworks_page(
        self,
        page: int,
        status: int,
        group_id: int
    ) -> list[dict[str, Any]]:
        """Method to get all homeworks from the page.

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
            list[dict[str, Any]]: All homeworks from the page.
        """
        return self.journal_scrapper.get_homeworks_from_api(
            page=page,
            status=status,
            group_id=group_id
        )


class HomeworksPageModel:
    """Model for representing a page of homeworks."""
    def __init__(
        self,
        journal_homework_api: HomeworkAPI,
        page: int,
        status: int,
        group_id: int
    ) -> None:
        """Initialize a page model with the page and get all homeworks from the page by URL.

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
        """
        
        self.page: int = page
        self.status: int = status
        self.group_id: int = group_id
        self.homeworks: Generator[HomeworkModel, None, None] = self._get_homeworks_page(journal_homework_api=journal_homework_api)
    
    def _get_homeworks_page(self, journal_homework_api: HomeworkAPI) -> Generator[HomeworkModel, None, None]:
        """Send a GET request to the API and return a generator of homeworks from the page.

        Yields:
            Generator[HomeworkModel, None, None]: HomeworkModel with necessary attributes.
        """
        STATUS_KEY: str = "status"
        TEACHER_NAME_KEY: str = "fio_teach"
        SUBJECT_NAME_KEY: str = "name_spec"
        FILE_URL_PATH_KEY: str = "file_path"
        COMMENT_KEY: str = "comment"
        CREATION_TIME_KEY: str = "creation_time"
        THEME_KEY: str = "theme"
        
        for homework in journal_homework_api.get_homeworks_page(
            page=self.page,
            status=self.status,
            group_id=self.group_id
        ):
            yield HomeworkModel(
                status=homework.get(STATUS_KEY),
                teacher_name=homework.get(TEACHER_NAME_KEY),
                subject_name=homework.get(SUBJECT_NAME_KEY),
                file_url_path=homework.get(FILE_URL_PATH_KEY),
                comment=homework.get(COMMENT_KEY),
                creation_time=homework.get(CREATION_TIME_KEY),
                theme=homework.get(THEME_KEY)
            )
    
    def __iter__(self) -> Generator[HomeworkModel, None, None]:
        """Return a generator of homeworks from the page"""
        for homework in self.homeworks:
            yield homework


class HomeworksPageModelFactory:
    """Factory for creating a page model with the page of homeworks"""
    def __init__(
        self,
        login_data: dict[str, str] | UserInputData,
        page: int,
        status: int,
        group_id: int,
    ) -> None:
        journal_homework_api: HomeworkAPI = HomeworkAPI(login_data=login_data)
        self.homeworks_page_model: HomeworksPageModel = HomeworksPageModel(
            page=page,
            status=status,
            group_id=group_id,
            journal_homework_api=journal_homework_api
        )
    
    def __iter__(self) -> Generator[HomeworkModel, None, None]:
        """Return a generator of homeworks from the page"""
        for homework in self.homeworks_page_model:
            yield homework