from django.core.exceptions import ValidationError

def validate_csv(value):
    splitted_values = [item for item in value.split(';') if item]
    if len(splitted_values) % 2 != 0:
        raise ValidationError(u'Not a valid CSV input')