from django.contrib.auth import get_user_model

import pytest


class TestsModels:
    mock_password = '123'
    mock_email = 'test@opentext.com'

    @pytest.mark.django_db
    def test_success_create_user_with_email(self):
        user = get_user_model().objects.create_user(self.mock_email, self.mock_password)

        assert user.email == self.mock_email
        assert user.check_password(self.mock_password) is True

    @pytest.mark.django_db
    def test_success_normalize_email(self):
        email = 'test@OPENTEXT.COM'
        user = get_user_model().objects.create_user(email, self.mock_password)

        assert user.email == email.lower()

    @pytest.mark.django_db
    def test_error_email_is_none(self):
        with pytest.raises(ValueError):
            get_user_model().objects.create_user(None, self.mock_password)

    @pytest.mark.django_db
    def test_success_create_superuser(self):
        user = get_user_model().objects.create_superuser(self.mock_email, self.mock_password)

        assert user.is_superuser is True
        assert user.is_staff is True
