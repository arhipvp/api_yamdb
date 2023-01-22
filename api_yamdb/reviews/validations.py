from django.core.exceptions import ValidationError
import datetime

def ValidateYear(year):
    if year < 1990 or year > datetime.datetime.now.year:
        raise ValidationError(f'{year} - ошибка года')
