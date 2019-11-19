import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False

def python_news_func():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for py_news in all_news:
            title = py_news.find('a').text
            url = py_news.find('a')['href']
            published = py_news.find('time').text
            result_news.append({
                "title": title,
                "url": url,
                "published": published
            })
        return result_news
    return False
