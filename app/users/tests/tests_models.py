from django.contrib.auth import get_user_model

import pytest


class TestsModels:
    @pytest.mark.django_db
    def test_success_create_user_with_email(self):
        email = "test@opentext.com"
        password = 'test_pass'
        user = get_user_model().objects.create_user(email=email, password=password)

        assert user.email == email
        assert user.check_password(password) is True