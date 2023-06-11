from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from blog.models import Post as PostModel


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post_detail')
    permission_classes = [IsAuthenticated]

    class Meta:
        model = PostModel
        fields = ('title', 'text', 'created_date', 'published_date', 'image', 'url')

    def create(self, validated_data):
        return PostModel.objects.create(**validated_data)
