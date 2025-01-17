from rest_framework import serializers
from .models import User, Hobby, FriendRequest
from rest_framework.validators import UniqueValidator
from django.contrib.auth import update_session_auth_hash
from datetime import date
from typing import Any, Dict, Optional, Type


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[FriendRequest] = FriendRequest
        fields: list[str] = [ 'status', 'sender', 'id', 'receiver']

            
class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[Hobby] = Hobby
        fields: list[str] = ['id', 'name']
        extra_kwargs: dict = {
            'name': {'validators': [UniqueValidator(queryset=Hobby.objects.all())]}
        }

# Read Serializer for User (Includes calculated_age and similarity_score)
class UserReadSerializer(serializers.ModelSerializer):
    similarity_score: serializers.IntegerField = serializers.IntegerField(read_only=True)
    calculated_age: serializers.SerializerMethodField = serializers.SerializerMethodField()  # Dynamically calculate age

    class Meta:
        model: Type[User] = User
        fields: tuple[str, ...] = (
            'id', 'username', 'email', 'name', 'date_of_birth', 'calculated_age', 'hobbies','friends', 'similarity_score'
        )

    def get_calculated_age(self, obj:User) -> Optional[int]:

        if obj.date_of_birth:
            today: date = date.today()
            return (
                today.year - obj.date_of_birth.year -
                ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            )
        return None  # Return None if `date_of_birth` is not set

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model: Type[User] = User
        fields: tuple[str, ...] = ('id', 'username', 'email', 'name', 'password', 'date_of_birth', 'hobbies', 'friends')
        extra_kwargs: dict = {
            'password': {'write_only': True},
            'username': {'required': False}  
        }

    def update(self, instance: User, validated_data: Dict[str,Any]) -> User:
        """Override update method to handle password and other fields."""
        # Update the basic fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
        friends_data = validated_data.get('friends', None)
        if friends_data is not None:
            # Assuming friends is a ManyToMany field, you can update it like this:
            instance.friends.set(friends_data)  # Update friends by setting new list
        
        # Handle hobbies update (Many-to-Many relationship)
        hobbies_data = validated_data.get('hobbies', None)
        if hobbies_data is not None:
            # Assuming hobbies is a ManyToMany field, you can update it like this:
            instance.hobbies.set(hobbies_data)  # Update hobbies by setting new list

        
        # Handle password update separately
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            update_session_auth_hash(self.context['request'], instance)
        instance.save()
        return instance
    
     # Use email as username (reference: learnouts.com)
    def create(self, validated_data: Dict[str, Any]) -> User:        
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'] 
        user: User = User.objects.create_user(**validated_data)
        return user
    
    


