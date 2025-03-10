
## Built-in modules: ##
from os.path import dirname
from os import PathLike


current_dir_path: PathLike = dirname(__file__)
JOURNAL_LOGIN_URL: str = "https://msapi.top-academy.ru/api/v2/auth/login"