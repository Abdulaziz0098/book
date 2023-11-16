from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from book_catalog.models import Author
from book_catalog.serializers import AuthorSerializer


@swagger_auto_schema(
    method='GET',
    responses={
        200: AuthorSerializer(many=True),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def author_list(request):
    """
    Get a list of authors.
    """
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='POST',
    request_body=AuthorSerializer,
    responses={
        201: AuthorSerializer(),
        400: 'Bad Request',
    }
)
@api_view(['POST'])
def create_author(request):
    """
    Create a new author.
    """
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
    responses={
        200: AuthorSerializer(),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def get_author(request, pk):
    """
    Get details of a specific author.
    """
    try:
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='PUT',
    request_body=AuthorSerializer,
    responses={
        200: AuthorSerializer(),
        400: 'Bad Request',
        404: 'Not Found',
    }
)
@api_view(['PUT'])
def update_author(request, pk):
    """
    Update details of a specific author.
    """
    try:
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='DELETE',
    responses={
        204: 'No Content',
        404: 'Not Found',
    }
)
@api_view(['DELETE'])
def delete_author(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
