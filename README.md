# api_yamdb

api_yamdb

## Описание

Проект YaMDb собирает отзывы пользователей на произведения

### Технологии

Python 3.7

#### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:arhipvp/api_yamdb.git
```

```bash
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python manage.py migrate
```

Загрузить тестовые данные
```bash
python manage.py load_csv
```

Запустить проект:

```bash
python manage.py runserver
```

Документация в формате Redoc:

```HTTP
http://127.0.0.1:8000/redoc/
```

##### Авторы

Архипов Владимир
Афанасьев Илья
Гринчар Николай
