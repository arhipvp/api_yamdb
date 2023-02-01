from django.utils import timezone

from django.core.exceptions import ValidationError


def YearValidator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
