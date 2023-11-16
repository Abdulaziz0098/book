from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, exceptions, permissions
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from . import serializer as user_serializer
from .serializer import *


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        200: UserSerializer(),
        400: 'Bad Request'
    }
)
@api_view(['POST'])
@csrf_protect
def register_api(request):
    serializer = user_serializer.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    serializer.instance = services.create_user(user_dc=data)

    return response.Response(data=serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={
        200: 'string',
        400: 'Bad Request',
        401: 'Unauthorized'
    }
)
@api_view(['POST'])
def login_api(request):
    email = request.data["email"]
    password = request.data["password"]

    user = services.user_email_selector(email=email)

    if user is None:
        raise exceptions.AuthenticationFailed("Invalid Credentials")

    if not user.check_password(raw_password=password):
        raise exceptions.AuthenticationFailed("Invalid Credentials")

    token = services.create_token(user_id=user.id)
    resp = response.Response()
    resp.set_cookie(key="jwt", value=token, httponly=True)

    return response.Response({'token': token})


@swagger_auto_schema(
    method='get',
    responses={
        200: UserSerializer()
    }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_api(request):
    user = request.user
    serializer = user_serializer.UserSerializer(user)
    return response.Response(serializer.data)


@swagger_auto_schema(
    method='post',
    responses={
        200: 'Logout successful. The session has been terminated.'
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    resp = response.Response()
    resp.delete_cookie("jwt")
    resp.data = {"message": "logged out"}

    return resp
