import json

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

CREATE_USER_URL = reverse('users:create')


class TestsUsersApi:
    user_body = {'email': 'test@opentext.com', 'password': '123456', 'name': 'Test User'}

    @pytest.mark.django_db
    def test_success_create_user(self, client):
        response = client.post(CREATE_USER_URL, self.user_body)
        assert response.status_code == status.HTTP_201_CREATED
        json_content = json.loads(response.content)
        user = get_user_model().objects.get(email=json_content['email'])
        assert user.check_password(self.user_body['password']) is True
        assert 'password' not in json_content.keys()

    @pytest.mark.django_db
    def test_success_user_exists(self, client):
        response = client.post(CREATE_USER_URL, self.user_body)
        assert response.status_code == status.HTTP_201_CREATED
        response = client.post(CREATE_USER_URL, self.user_body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_success_password_limit(self, client):
        body = {'email': 'test@opentext.com', 'password': '1'}
        response = client.post(CREATE_USER_URL, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = get_user_model().objects.filter(email=body['email']).exists()
        assert user_exists is False
