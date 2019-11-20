from webapp import create_app
from webapp.news_python import python_news_func

app = create_app()
with app.app_context():
    python_news_func()