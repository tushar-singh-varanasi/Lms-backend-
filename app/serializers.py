# serializers.py

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Book,Transaction
User = get_user_model()

class UserRegistration(serializers.ModelSerializer):
    email = serializers.EmailField()
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirm password do not match")

        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove 'password2' from validated_data
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserRegistration, self).create(validated_data)
        return user
    
# for librarian crud
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

   
class Userloginserilaizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Check if a user with the provided username exists
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("A user with that username does not exist.")

        data['user'] = user
        return data
    
class UserprofileSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'        
    
    def update(self, instance, validated_data):
        instance.return_date = validated_data.get('return_date', instance.return_date)
        
        # Assuming your Book model has a 'status' field
        # Update the book status to 'AVAILABLE' when returning the book
        instance.book.status = 'AVAILABLE'
        instance.book.save()

        instance.save()
        return instance    