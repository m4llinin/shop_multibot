from dataclasses import dataclass

from database.schemas.Mail import Mail


@dataclass
class MyMail:
    mails: list[Mail]
    all_pages: int
    cur_page: int = 0
