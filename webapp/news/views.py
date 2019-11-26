from flask import Blueprint, current_app, render_template

from webapp.news.models import News
from webapp.weather import get_city_weather

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def index():
    title = "Python news"
    weather = get_city_weather(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)