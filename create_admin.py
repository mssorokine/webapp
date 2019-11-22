from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)
    
    password_primary = getpass('Введите пароль: ')
    password_repeat = getpass('Повторите пароль: ')

    if not password_primary == password_repeat:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password_primary)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id {}'.format(new_user.id))
    
