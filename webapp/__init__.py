from flask import Flask, render_template
from webapp.weather import get_city_weather
from webapp.news_python import python_news_func

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        title = "Новости Python"
        weather = get_city_weather(app.config['WEATHER_DEFAULT_CITY'])
        news_list = python_news_func()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)
    return app