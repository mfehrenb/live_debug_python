from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest


@pytest.fixture
def test_user():
    mock_email = 'test@opentext.com'
    mock_password = '123'
    return get_user_model().objects.create_user(mock_email, mock_password,
                                                name='Test user name')


class TestsAdmin:
    @pytest.mark.django_db
    def test_users_listed(self, admin_client, test_user):
        url = reverse('admin:users_user_changelist')
        response = admin_client.get(url)
        repsonse_content_as_string = response.content.decode("utf-8")
        assert test_user.name in repsonse_content_as_string
        assert test_user.email in repsonse_content_as_string

    @pytest.mark.django_db
    def test_user_change_page(self, admin_client, test_user):
        url = reverse('admin:users_user_change', args=[test_user.id])
        response = admin_client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_create_page(self, admin_client, test_user):
        url = reverse('admin:users_user_add')
        response = admin_client.get(url)

        assert response.status_code == 200
