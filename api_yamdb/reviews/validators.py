from datetime import datetime

def my_year_validator(value):
    if value < 1900 or value > datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correcrt year!'),
            params={'value': value},
        )