from rest_framework import serializers
from .models import User, Hobby

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}  
        }

     # Use email as username (reference: learnouts.com)
    def create(self, validated_data):
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'] 
        user = User.objects.create_user(**validated_data)
        return user

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']
