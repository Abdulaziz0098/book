from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from book_catalog.models import Genre
from book_catalog.serializers import GenreSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: GenreSerializer(many=True),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=GenreSerializer,
    responses={
        201: GenreSerializer(),
        400: 'Bad Request',
    }
)
@api_view(['POST'])
def create_genre(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: GenreSerializer(),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def get_genre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    request_body=GenreSerializer,
    responses={
        200: GenreSerializer(),
        400: 'Bad Request',
        404: 'Not Found',
    }
)
@api_view(['PUT'])
def update_genre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='delete',
    responses={
        204: 'No Content',
        404: 'Not Found',
    }
)
@api_view(['DELETE'])
def delete_genre(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
