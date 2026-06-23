import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Page:
    load_time: float
    content: str

class UI:
    def __init__(self, pages: Dict[str, Page]):
        self.pages = pages

    def get_page(self, page_name: str) -> Page:
        return self.pages.get(page_name)

    def is_responsive(self, page_name: str) -> bool:
        page = self.get_page(page_name)
        if page:
            return page.load_time < 2
        return False

    def is_clean(self, page_name: str) -> bool:
        page = self.get_page(page_name)
        if page:
            return len(page.content) > 0
        return False
