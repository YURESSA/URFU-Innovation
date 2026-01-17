from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import Base, engine
from .routes import register_routes


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=Config.ALLOWED_ORIGINS)

    # Создание таблиц
    Base.metadata.create_all(bind=engine)

    # Регистрация маршрутов
    register_routes(app)

    return app
