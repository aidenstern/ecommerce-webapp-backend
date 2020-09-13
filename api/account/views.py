import json
from datetime import timedelta

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from requests.exceptions import HTTPError
from rest_framework import generics, permissions, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from social_django.utils import load_backend, load_strategy

from .models import Account
from .serializers import AccountSerializer, LoginSerializer, SocialSerializer
from .utils import validate_email, validate_username


class AccountRegistration(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.create()
            token = Token.objects.create(user=account)
            response = Account.objects.filter(email=account.email).values().first()
            del response['password']
            response['access_token'] = token.key
            return Response(response, status=200)
        else:
            return Response(data=serializer.errors, status=400)


class AccountLogin(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data
            token, created = Token.objects.get_or_create(user=account)
            response = Account.objects.filter(email=account.email).values().first()
            del response['password']
            response['access_token'] = token.key
            return Response(response, status=200)
        else:
            return Response(data=serializer.errors, status=400)


class SocialLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(str(e), status=400)

        provider = request.data['provider']

        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy, name=provider, redirect_uri=None)

        token = serializer.validated_data['access_token']

        try:
            user = backend.do_auth(token)
        except Exception as e:
            return Response({"errors": str(e)}, status=400)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            response = Account.objects.filter(email=account.email).values().first()
            del response['password']
            response['access_token'] = token.key
            return Response(response, status=200)
        else:
            return Response({"errors": "Authentication failed"}, status=400)


class AccountLogout(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        Token.objects.get(key=request.data['access_token']).delete()
        return Response(status=status.HTTP_200_OK)
        
        
