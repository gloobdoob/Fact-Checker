from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from bs4.element import Tag
from mechanize import Browser

class GoogleScraper:
    def __init__(self, n_searches = 30):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s, options=self.options)

        self.br = Browser()
        self.n_searches = n_searches

    def get_results(self, query):

        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')]

        google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}" + "&num=" + f'{self.n_searches}'
        self.driver.get(google_url)
        time.sleep(3)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        result_div = soup.find_all('div', attrs={'class': 'g'})

        links = []
        titles = []
        descriptions = []
        titles_links = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href=True)
                title = None
                title = r.find('h3')

                if isinstance(title, Tag):
                    title = title.get_text()

                description = None
                description = r.find('span', attrs={'class': 'st'})

                if isinstance(description, Tag):
                    description = description.get_text()

                self.br.open(link['href'])
                title = self.br.title()

                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '':
                    links.append(link['href'])
                    self.br.open(link['href'])
                    titles.append(title)
                    descriptions.append(description)

            # Next loop if one element is not present
            except Exception as e:
                print(e)
                continue

        for title, link in zip(titles, links):
            if title != 'Images' and title != 'Description' and title != None:
                titles_links.append((title, link))

        return titles_links