
## Built-in modules: ##
from os import mkdir, listdir
from os import PathLike
from os.path import join, exists
from typing import Optional

## Local modules: ##
from journal_homework_models import HomeworkModel
from journal_requests import JournalHomeworkScrapper, UserInputData
from journal_loggers import folder_manager_logger
from config import current_dir_path


class HomeworksFolderManager:
    """Class to save homeworks from the API to the disk."""
    HOMEWORK_PAGE_NAME: str = "homeworks"
    
    def __init__(
        self,
        homework_to_save: HomeworkModel,
        login_data: dict[str, str] | UserInputData
    ) -> None:
        """Get HomeworkModel with login data and save it in file from the model in the disk.

        Args:
            homework_to_save (HomeworkModel): Homework model to save.
            login_data (dict[str, str] | UserInputData): dict object with 4 fields:
                You can get all of it in the JournalAPI. 
                https://journal.top-academy.ru/ru/auth/login/index
                
                APPLICATION_KEY = YOUR_APP_KEY
                ID_CITY = YOUR_ID_CITY (sometimes it can be "null").
                PASSWORD = YOUR_PASSWORD
                USER_NAME = YOUR_USERNAME
        """
        self.homework_to_save = homework_to_save
        self.homework_subject_name: str = homework_to_save.subject_name
        self.homework_theme: str = homework_to_save.theme
        self.file_url_path: str = homework_to_save.file_url_path
        self.login_data: dict[str, str] | UserInputData = login_data
        
        if not exists(self.HOMEWORK_PAGE_NAME):
            mkdir(self.HOMEWORK_PAGE_NAME)
        
    @folder_manager_logger
    def save_to_path(self, dir_path: Optional[PathLike] = current_dir_path) -> None:
        """Save the homework to the disk.

        Args:
            dir_path (PathLike, optional): path to homeworks folder. Defaults to current_dir_path.
                (homeworks folder in the current workspace)
        """
        
        subject_folder_name: str = self.homework_subject_name
        homework_folder_path: PathLike = join(dir_path, self.HOMEWORK_PAGE_NAME, subject_folder_name)
        
        if not exists(homework_folder_path):
            mkdir(homework_folder_path)
        
        homework_filename: str = self.homework_theme
        homeworks_scrapper: JournalHomeworkScrapper = JournalHomeworkScrapper(login_data=self.login_data)
        homework_file: bytes = homeworks_scrapper.download_homework_file(self.file_url_path)
        homework_file_ext: str = homework_file[0]
        COPY_POSTFIX: str = "_copy"
        
        if f"{homework_filename}.{homework_file_ext}" in listdir(homework_folder_path):
            homework_filename: str = f"{homework_filename}{COPY_POSTFIX}"
        homework_full_filename: str = f"{homework_filename}.{homework_file_ext}"

        
        with open(
            file=join(homework_folder_path, homework_full_filename),
            mode="wb"
        ) as file:
            file.write(homework_file[1])