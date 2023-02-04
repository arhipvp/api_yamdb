import datetime
import sqlite3

import pandas as pd
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command to load from static/data'

    def handle(self, *args, **options):
        # создаем соединение
        cnx = sqlite3.connect('db.sqlite3')

        # таблица users
        # очищаем данные
        cnx.execute("DELETE FROM reviews_user")
        # ищем путь к файлу
        path = finders.find('data/users.csv')
        # считываем csv при помощи pandas и создаем dataframe
        df = pd.read_csv(path)
        # удаляем дубликаты в стобце id
        df.drop_duplicates(subset=['id'], inplace=True)
        # удаляем строки с незаполненными id
        df.dropna(subset=['id'], inplace=True)
        # заполняем столбцы, которых нет в csv
        df["password"] = "test"
        df["is_superuser"] = 0
        df["is_staff"] = 0
        df["is_active"] = 1
        df["date_joined"] = datetime.datetime.now()
        df["first_name"] = "test_firstname"
        df["last_name"] = "test_lastname"
        df["bio"] = "test_bio"
        # заливаем dataframe в таблицу
        df.to_sql(
            name='reviews_user',
            if_exists='append',
            index=False,
            con=cnx,
        )

        # таблица categories
        cnx.execute("DELETE FROM reviews_categories")
        path = finders.find('data/category.csv')
        df = pd.read_csv(path)
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_categories', if_exists='append', index=False,
                  con=cnx)

        # таблица titles
        cnx.execute("DELETE FROM reviews_title")
        path = finders.find('data/titles.csv')
        df = pd.read_csv(path)
        # переименовываем столбец
        df.rename(columns={"category": "category_id"}, inplace=True)
        df["description"] = "test_description"
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_title', if_exists='append', index=False,
                  con=cnx)

        # таблица genre
        cnx.execute("DELETE FROM reviews_genre")
        path = finders.find('data/genre.csv')
        df = pd.read_csv(path)
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_genre', if_exists='append', index=False,
                  con=cnx)

        # таблица genre_title
        cnx.execute("DELETE FROM reviews_title_genre")
        path = finders.find('data/genre_title.csv')
        df = pd.read_csv(path)
        df.rename(columns={"genre_id": "genre_id"}, inplace=True)
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_title_genre', if_exists='append', index=False,
                  con=cnx)

        # таблица review
        cnx.execute("DELETE FROM reviews_review")
        path = finders.find('data/review.csv')
        df = pd.read_csv(path)
        df.rename(columns={"author": "author_id"}, inplace=True)
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_review', if_exists='append', index=False,
                  con=cnx)

        # таблица comments
        cnx.execute("DELETE FROM reviews_comment")
        path = finders.find('data/comments.csv')
        df = pd.read_csv(path)
        df.rename(columns={"author": "author_id"}, inplace=True)
        df.drop_duplicates(subset=['id'], inplace=True)
        df.dropna(subset=['id'], inplace=True)
        df.to_sql(name='reviews_comment', if_exists='append', index=False,
                  con=cnx)

        return "OK"
