
## Pip modules: ##
from fake_useragent import UserAgent


def get_random_useragent() -> str:
    """Get the random useragent from fake_useragent library.

    Returns:
        str: String with the useragent.
    """
    return UserAgent().random


def get_headers_for_login() -> dict:
    """Get the headers for POST request to Journal API with the random user-agent.

    Returns:
        dict: Headers dictionary.
    """
    user_agent: str = get_random_useragent()
    
    login_headers: dict[str, str] = {
        "authority": "msapi.top-academy.ru",
        "method": "POST",
        "path": "/api/v2/auth/login",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru_RU, ru",
        "authorization": "Bearer null",
        "content-type": "application/json",
        "origin": "https://journal.top-academy.ru",
        "priority": "u=1, i",
        "referer": "https://journal.top-academy.ru/",
        "user-agent": user_agent
    }
    
    return login_headers


def get_headers_for_downloads() -> dict:
    """Get the headers for GET request to Journal API with the random user-agent for downloading files.

    Returns:
        dict: Headers dictionary.
    """
    user_agent: str = get_random_useragent()
    
    headers: dict[str, str] = {
        "User-Agent": user_agent
    }
    return headers


def get_headers_for_requests(
    token: str,
) -> dict:
    """Get the headers for any GET request to Journal API.
    Token needs to pass it in auth field.

    Args:
        token (str): Auth token. You can get it after logging in the Journal.

    Returns:
        dict: Headers dictionary.
    """
    user_agent: str = get_random_useragent()
    
    headers: dict[str, str] = {
        "Host": "msapi.top-academy.ru",
        "User-Agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru_RU, ru",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Authorization": f"Bearer {token}",
        "Origin": "https://journal.top-academy.ru",
        "Connection": "keep-alive",
        "Referer": "https://journal.top-academy.ru/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }
    return headers
