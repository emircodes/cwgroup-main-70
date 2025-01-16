from rest_framework import serializers
from .models import User, Hobby, FriendRequest
from rest_framework.validators import UniqueValidator
from django.contrib.auth import update_session_auth_hash

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'created_at', 'status']
        
        
        
class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'validators': [UniqueValidator(queryset=Hobby.objects.all())]}
        }
        
class UserSerializer(serializers.ModelSerializer):
    similarity_score = serializers.IntegerField(read_only=True) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'password', 'date_of_birth', 'hobbies', 'similarity_score', 'friends')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}  
        }

    def update(self, instance, validated_data):
        """Override update method to handle password and other fields."""
        # Update the basic fields
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
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
    def create(self, validated_data):        
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'] 
        user = User.objects.create_user(**validated_data)
        
 
        
        return user
    
    


