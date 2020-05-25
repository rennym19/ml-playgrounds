from django.contrib.auth import get_user_model

from rest_framework.serializers import ValidationError

def validate_dataset_name_type(name):
    if not isinstance(name, str):
        raise ValidationError('name should be a string')
    return name

def validate_dataset_name_length(name):
    if len(name) > 255:
        raise ValidationError('name should be 255 characters long at most')
    return name

def validate_user_id(qs, user_id):
    if not qs.filter(username=user_id).exists():
        raise ValidationError('user_id should be a valid username')
    return user_id
