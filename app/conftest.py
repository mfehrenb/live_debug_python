from django.contrib.auth import get_user_model

import pytest


@pytest.fixture
def create_default_user():
    def _do_create():
        return get_user_model().objects.create_user(email='test@opentext.com', password='test123', name='Test User')
    return _do_create
