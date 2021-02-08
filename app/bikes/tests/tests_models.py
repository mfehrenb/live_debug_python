import pytest
from bikes import models


class TestsModels:
    @pytest.mark.django_db
    def test_success_tag_str(self, create_default_user):
        user = create_default_user()
        tag = models.Tag.objects.create(user=user, name='Santa Cruz')

        assert str(tag) == tag.name


