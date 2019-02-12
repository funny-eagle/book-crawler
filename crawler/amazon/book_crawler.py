import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def crawl_book_info(isbn):
    agent = UserAgent()
    headers = {'User-Agent': agent.random}
    url = 'https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=' + isbn
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    ul = soup.find_all('ul', {'id': 's-results-list-atf'})
    title = ''
    image = ''
    if len(ul) > 0:
        li = ul[0].find_all('li')
        if len(li) > 0:
            title = li[0].find('img').get('alt')
            image = li[0].find('img').get('src')
    return title, isbn, image
