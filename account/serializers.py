from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone_number(self, phone_number):
        if not phone_number.isdigit():
            raise serializers.ValidationError({"phone_number": "Phone number is not valid!"}) 
        if phone_number[0:2] != "09" or len(phone_number) < 11:
            raise serializers.ValidationError({"phone_number": "Phone number is not valid!"}) 
        return phone_number

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return password

    def save(self):

        name = self.validated_data["name"]
        email = self.validated_data["email"]
        phone_number = self.validated_data["phone_number"]
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
       
        user = User(
            name=name,
            email=email,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save()
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password2 = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, current_password):
        if not self.context['request'].user.check_password(current_password):
            raise serializers.ValidationError({'current_password': 'Current password is not match'})
        return current_password    
    
    def validate_new_password(self, new_password):
        new_password2 = self.context["request"].data["new_password2"]
        if new_password != new_password2:
            raise serializers.ValidationError({'new_password': 'New password is not match'})
        return new_password
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone_number")

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError({"phone_number": "Phone number is not valid!"}) 
        if value[0:2] != "09" or len(value) < 11:
            raise serializers.ValidationError({"phone_number": "Phone number is not valid!"}) 
        return value
    