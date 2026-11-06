"""Сериализаторы списка пользователей и регистрации с проверкой данных и пароля."""
from django.contrib.auth.templatetags.auth import render_password_as_hash
from rest_framework import serializers
from apps.users.models import User

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

import re


class UserListSerializer(serializers.ModelSerializer):
    """Представление контактных данных, должности и времени входа пользователя."""
    class Meta:
        """Модель пользователя и поля, включаемые в список пользователей."""
        model = User
        fields=('first_name',
                 'last_name',
                 'position',
                 'email',
                 'phone',
                 'last_login')


class RegisterUserSerializer(serializers.ModelSerializer):
    """Проверка регистрационных данных и создание пользователя с хешированным паролем."""
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        """Поля регистрации и запрет вывода пароля в ответе API."""
        model = User
        fields = ('username',
                 'first_name',
                 'last_name',
                 'email',
                 'position',
                 'password',
                 're_password',
)
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Проверить допустимые символы в именах, совпадение паролей и требования к паролю."""
        username=data.get('username')
        first_name=data.get('first_name')
        last_name=data.get('last_name')

        if not re.match('^[a-zA-Z0-9_]*$',username):
            raise serializers.ValidationError("Username must be alphanumeric")
        if not re.match('^[a-zA-Z]*$', first_name):
            raise serializers.ValidationError("First name must be alphanumeric")
        if not re.match('^[a-zA-Z]*$', last_name):
            raise serializers.ValidationError("Last name must be alphanumeric")

        password = data.get('password')
        re_password = data.get('re_password')

        if password != re_password:
            raise serializers.ValidationError({"password": "Passwords don't match"})

        try:
            validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})

        return data

    def create(self, validated_data):
        """Удалить подтверждение пароля и сохранить пользователя с хешированным паролем."""
        password = validated_data.pop('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

