import json

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


class TestsPublicUsersApi:
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
    def test_error_user_exists(self, client):
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

    @pytest.mark.django_db
    def test_success_user_token_creation(self, client):
        response = client.post(CREATE_USER_URL, self.user_body)
        assert response.status_code == status.HTTP_201_CREATED
        response = client.post(TOKEN_URL, self.user_body)
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)['token'] is not None

    @pytest.mark.django_db
    def test_error_user_token_creation_bad_creds(self, client):
        response = client.post(CREATE_USER_URL, self.user_body)
        assert response.status_code == status.HTTP_201_CREATED
        body = {'email': 'test@opentext.com', 'password': 'wrong_pass'}
        response = client.post(CREATE_USER_URL, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in json.loads(response.content).keys()

    @pytest.mark.django_db
    def test_error_user_token_creation_user_not_exists(self, client):
        body = {'email': 'test@opentext.com', 'password': 'wrong_pass'}
        response = client.post(CREATE_USER_URL, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in json.loads(response.content).keys()

    @pytest.mark.django_db
    def test_error_user_token_creation_missing_password(self, client):
        body = {'email': 'test@opentext.com', 'password': 'wrong_pass'}
        response = client.post(CREATE_USER_URL, body)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in json.loads(response.content).keys()

    @pytest.mark.django_db
    def test_retrieve_user_unauthorized(self, client):
        response = client.get(ME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class PrivateUserApiTests:
    def test_retrieve_profile_success(self, client, create_default_user):
        user = create_default_user()
        client.force_login(user)
        response = client.get(ME_URL)
        response_json = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert response_json['name'] == user['name']
        assert response_json['email'] == user['email']

    def test_post_me_not_allowed(self, client, create_default_user):
        user = create_default_user()
        client.force_login(user)
        response = client.post(ME_URL, {})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_user_profile(self, client, create_default_user):
        user = create_default_user()
        client.force_login(user)
        payload = {'name': 'new name', 'password': 'newpassword123'}
        response = client.patch(ME_URL, payload)

        user.refresh_from_db()
        assert user['name'], payload['name']
        assert user.check_password(payload['password']) is True
        assert response.status_code == status.HTTP_200_OK
