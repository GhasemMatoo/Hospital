from rest_framework import serializers
from rest_framework_simplejwt.serializers import  TokenObtainPairSerializer
from accounts.models import User
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    Re_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'Re_password']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('Re_password'):
            raise serializers.ValidationError({'detail': 'Password doesnt match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('Re_password')
        return User.objects.create(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        validate_data['User_email'] = self.user.email
        validate_data['User_id'] = self.user.id
        return validate_data