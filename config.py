import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

LANGUAGES = {
    'en': 'English',
    'sk': 'Slovensky'
}
