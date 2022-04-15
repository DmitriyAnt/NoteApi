import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from pathlib import Path

base_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(__file__).parent

security_definitions = {
   "basicAuth": {
       "type": "basic"
   }
}

db_path = os.environ.get('DATABASE_URL')
if db_path is None:
    db_path = f'sqlite:///{BASE_DIR / "base.db"}'
else:
    db_path = db_path.replace("://", "ql://", 1)  # only for Heroku


class Config:
    SQLALCHEMY_DATABASE_URI = db_path
    TEST_DATABASE_URI = f'sqlite:///{BASE_DIR / "base.db"}'  # 'sqlite:///' + os.path.join(base_dir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    RESTFUL_JSON = {'ensure_ascii': False, }
    APISPEC_SPEC = APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions,
        security=[],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL = '/swagger'  # URI API Doc JSON
    APISPEC_SWAGGER_UI_URL = '/swagger-ui'  # URI UI of API Doc
    LANGUAGES = ['en', 'ru']
