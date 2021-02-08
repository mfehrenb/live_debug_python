import json

from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status
from bikes.models import Tag
from bikes.serializers import TagSerializer

TAGS_URL = reverse('bikes:tag-list')


class TestsPublicTagAPI:
    @pytest.mark.django_db
    def test_success_login_required(self, client):
        response = client.get(TAGS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestsPrivateTagAPI:
    @pytest.mark.django_db
    def test_success_retrieve_tags(self, client, create_default_user):
        user = create_default_user()
        response = client.login(email='test@opentext.com', password='')
        print(response)
        Tag.objects.create(user=user, name='Santa Cruz')
        Tag.objects.create(user=user, name='Norco')

        response = client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content) == serializer.data

    @pytest.mark.django_db
    def test_tags_limited_to_user(self, client, create_default_user):
        user = create_default_user()
        client.force_login(user)
        user2 = get_user_model().objects.create_user(
            'test2@opentext.com',
            'test123'
        )

        Tag.objects.create(user=user2, name='Specialized')
        tag = Tag.objects.create(user=user, name='Norco')

        response = client.get(TAGS_URL)
        response_json = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json['data'][0]['name'] == tag.name
