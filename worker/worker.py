import httpx
from bs4 import BeautifulSoup


def get_url_metadata(url: str):
    try:
        response = httpx.get(url)
        status_code = response.status_code
        if status_code >= 300:
            return (status_code, None)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
    except Exception as e:
        print(f"Error: {e}")
    return (status_code, title)
