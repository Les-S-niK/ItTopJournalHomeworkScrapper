
from journal_homework_models import HomeworksPageModelFactory
from journal_requests import UserInputData
from homeworks_folder_manager import HomeworksFolderManager


APPLICATION_KEY: str = ""
PASSWORD: str = ""
USERNAME: str = ""

user_data: UserInputData = UserInputData(
    APPLICATION_KEY=APPLICATION_KEY,
    ID_CITY="null",
    PASSWORD=PASSWORD,
    USERNAME=USERNAME
)
factory: HomeworksPageModelFactory = HomeworksPageModelFactory(
    login_data=user_data,
    page=0,
    status=1,
    group_id=53
)

for homework in factory.homeworks_page_model:
    manager: HomeworksFolderManager = HomeworksFolderManager(
        homework_to_save=homework,
        login_data=user_data
    )
    manager.save_to_path()


