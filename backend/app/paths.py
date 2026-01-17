import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к ресурсам
BELBIN_TEST_PATH = os.path.join(BASE_DIR, os.getenv('BELBIN_TEST', 'data/belbin/belbin.json'))
DB_PATH = os.path.join(BASE_DIR, os.getenv('DB_PATH', 'sqlite:///data/innovate.db3'))
