from .models import Account
from rest_framework import serializers
from django.contrib.auth import authenticate


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, request):
        email = request.get("email").lower()
        password = request.get("password")
        user = authenticate(email=email, password=password)
        if user:
            return user
        else:
            raise serializers.ValidationError("invalid credentials")


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self):
        account = Account.objects.create_user(**self.validated_data)
        return account