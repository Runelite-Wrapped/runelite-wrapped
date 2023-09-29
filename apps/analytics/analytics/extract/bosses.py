from typing import List
from requests import get
from bs4 import BeautifulSoup


_url = "https://secure.runescape.com/m=hiscore_oldschool/overall"


def get_boss_list(url: str = None) -> List[str]:
    url = url or _url

    resp = get(_url)
    content = resp.text

    soup = BeautifulSoup(content, "html.parser")

    # get all "a" elements with the class activity-link
    # this is the list of bosses
    bosses = soup.find_all("a", class_="activity-link")

    # get the inner text of each element
    return [boss.text for boss in bosses]
