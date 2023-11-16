from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from book_catalog.models import Review
from book_catalog.serializers import ReviewSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: ReviewSerializer(many=True),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def review_list(request, pk):
    reviews = Review.objects.filter(book=pk)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=ReviewSerializer,
    responses={
        201: ReviewSerializer(),
        400: 'Bad Request',
    }
)
@api_view(['POST'])
def create_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: ReviewSerializer(),
        404: 'Not Found',
    }
)
@api_view(['GET'])
def get_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    request_body=ReviewSerializer,
    responses={
        200: ReviewSerializer(),
        400: 'Bad Request',
        404: 'Not Found',
    }
)
@api_view(['PUT'])
def update_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='delete',
    responses={
        204: 'No Content',
        404: 'Not Found',
    }
)
@api_view(['DELETE'])
def delete_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
