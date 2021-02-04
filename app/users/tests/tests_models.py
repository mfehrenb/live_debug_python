from django.contrib.auth import get_user_model

import pytest
from pytest_django.plugin import django_db_blocker


class TestsModels:
    @pytest.mark.django_db
    def test_success_create_user_with_email(self):
        email = "test@opentext.com"
        password = 'test_pass'
        user = get_user_model().objects.create_user(email, password)

        assert user.email == email
        assert user.check_password(password) is True

    @pytest.mark.django_db
    def test_success_normalize_email(self):
        email = "test@OPENTEXT.COM"
        user = get_user_model().objects.create_user(email, '123')

        assert user.email == email.lower()
