import requests
from pydantic import BaseModel
import requests
import re
import unicodedata
import tempfile
import os


class CrawlWebsite(BaseModel):
    url : str
    js : bool = False
    depth : int = 1
    max_pages : int = 100
    max_time : int = 60

    def _crawl(self, url):
        response = requests.get(url)
        return response.text if response.status_code == 200 else None

    def process(self):
        content = self._crawl(self.url)
        ## Create a file
        file_name = f"{slugify(self.url)}.html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(content)
            ## Process the file

        return (temp_file_path, file_name) if content else None


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text