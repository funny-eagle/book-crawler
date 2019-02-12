import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def crawl_book_info(isbn):
    agent = UserAgent()
    headers = {'User-Agent': agent.random}
    url = 'http://search.dangdang.com/?act=input&key=' + isbn
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    ul = soup.find_all('ul', {'class': 'bigimg'})
    title = ''
    image = ''
    if len(ul) > 0:
        li = ul[0].find_all('li')
        if len(li) > 0:
            title = li[0].find('a').get('title')
            image = li[0].find('img').get('src')
    return title, isbn, image
