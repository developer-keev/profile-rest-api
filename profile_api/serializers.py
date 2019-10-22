from rest_framework import serializers

from .models import UserProfile, ProfileFeedItem


class HelloSerializers(serializers.Serializer):
    """serializer a name field for testing our APIViews"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """serializer a user Profile objects"""
    # password = serializers.CharField(write_only=True, style={'input_type':'password'})

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

        def create(self, validated_data):
            """Create and return a new user"""
            user = UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
            )
            return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """serialize a Profile feed Item objects"""

    class Meta:
        model = ProfileFeedItem
        fields = (
            'id',
            'user_profile',
            'status_text',
            'created_on'
        )
        extra_kwargs={
            'user_profile':{'read_only': True}
        }
