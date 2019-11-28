from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import locale
import platform

from webapp.db import db
from webapp.news.parsers.utils import get_html, save_news
from webapp.news.models import News

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()

def habr_news_func():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_habr_news = soup.find('ul', class_='content-list_posts').findAll('li', class_='content-list__item_post')
        result_news = []
        for habr_news in all_habr_news:
            title = habr_news.find('a', class_='post__title_link').text
            url = habr_news.find('a', class_='post__title_link')['href']
            published = habr_news.find('span', class_='post__time').text
            published = parse_habr_date(published)
            save_news(title, url, published)

def habr_news_content():
    news_empty_text = News.query.filter(News.text.is_(None))
    for news in news_empty_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_body = soup.find('div', class_='post__text-html').decode_contents()
            if news_body:
                news.text = news_body
                db.session.add(news)
                db.session.commit()
