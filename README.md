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

```python
python -m venv venv
```

```bash
source venv/bin/activate
```

```python
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```python
python manage.py migrate
```

Запустить проект:

```python
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
