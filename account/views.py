import jwt
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework import exceptions, status
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from book import settings
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
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user_data = serializer.validated_data
        services.create_user(user_data=user_data)

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    resp = Response()
    resp.set_cookie(key="jwt", value=token, httponly=True)

    return Response({'token': token})


@swagger_auto_schema(
    method='get',
    responses={
        200: UserSerializer()
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_api(request):
    user = request.user
    serializer = user_serializer.UserSerializer(user)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    responses={
        200: 'Logout successful. The session has been terminated.'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    resp = Response()
    resp.delete_cookie("jwt")
    resp.data = {"message": "logged out"}

    return resp


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = UserGetSerializers(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        email = payload['email']
        if email:
            user = get_user_model().objects.get(email=email)
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    except get_user_model().DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response({'message': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
