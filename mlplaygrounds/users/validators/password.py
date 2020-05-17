import re

from rest_framework.serializers import ValidationError

def validate_is_alpha(value):
    if not bool(re.search('[a-zA-Z]', value)):
        raise ValidationError('Password should have at least one letter.')

def validate_is_numeric(value):
    if not bool(re.search('[0-9]', value)):
        raise ValidationError('Password should have at least one number.')

def validate_not_short(value):
    if len(value) < 6:
        raise ValidationError('Password should have at least 6 characters.')
