from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from book_catalog.models import Book
from book_catalog.serializers import BookSerializer, BookListSerializer, BookDetailSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: BookListSerializer(many=True),
        404: 'Not Found',
    },
    manual_parameters=[
        openapi.Parameter('genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING),
        openapi.Parameter('author', openapi.IN_QUERY, description="Filter by author", type=openapi.TYPE_STRING),
        openapi.Parameter('publication_date', openapi.IN_QUERY,
                          description="Filter by publication date (YYYY-MM-DD format)", type=openapi.TYPE_STRING),
    ]
)
@api_view(['GET'])
def book_list(request):
    genre = request.query_params.get('genre', None)
    author = request.query_params.get('author', None)
    publication_date = request.query_params.get('publication_date', None)

    books = Book.objects.all()

    if genre:
        books = books.filter(genre=genre)

    if author:
        books = books.filter(author=author)

    if publication_date:
        books = books.filter(publication_date=publication_date)

    serializer = BookListSerializer(books, many=True, context={'request': request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=BookSerializer,
    responses={
        201: BookSerializer(),
        400: 'Bad Request',
    }
)
@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: BookDetailSerializer(),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookDetailSerializer(book, context={'request': request})
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    request_body=BookSerializer,
    responses={
        200: BookSerializer(),
        400: 'Bad Request',
        404: 'Not Found',
    }
)
@api_view(['PUT'])
def update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='delete',
    responses={
        204: 'No Content',
        404: 'Not Found',
    }
)
@api_view(['DELETE'])
def delete_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
