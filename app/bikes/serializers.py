from rest_framework import serializers

from bikes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)
