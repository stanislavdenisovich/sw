import os
import sys

# Укажите путь к вашему проекту и виртуальному окружению
project_path = '/var/www/School_websiteV19'
venv_path = '/var/www/School_websiteV19/myenv'

# Добавляем проект в sys.path
sys.path.insert(0, project_path)

# Устанавливаем виртуальное окружение
activate_env = os.path.join(venv_path, 'bin', 'activate_this.py')

# Проверка на существование файла
if os.path.exists(activate_env):
    exec(open(activate_env).read(), dict(__file__=activate_env))

# Импорт приложения
from app import app as application
