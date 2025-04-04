from rest_framework import serializers
#from core.models import Tweet  # or 
from tweet.models import Tweet
from django.contrib.auth.models import User

class TweetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id','text', 'photo','user_id']

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo:
            # Return full URL if photo exists
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return "no image uploaded"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'Password']