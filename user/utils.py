from user.models import Client

from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, user=None, request=None):
    return {'token': token, 'user_id': user.id, 'username': user.name}
