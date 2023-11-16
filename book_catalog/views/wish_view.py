from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from book_catalog.models import Wishlist
from book_catalog.serializers import WishlistSerializer, WishlistPostSerializer


@swagger_auto_schema(
    method='get',
    responses={
        200: WishlistSerializer(many=True),
        404: 'Not Found',
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_list(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(wishlists, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=WishlistPostSerializer,
    responses={
        201: WishlistSerializer(),
        400: 'Bad Request',
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_post_delete(request):
    book_id = request.data.get('book')

    existing_wishlist = Wishlist.objects.filter(user=request.user, book=book_id).first()

    if existing_wishlist:
        existing_wishlist.delete()
        return Response({"message": "Wishlist entry deleted"}, status=status.HTTP_200_OK)

    serializer = WishlistPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: WishlistSerializer(),
        404: 'Not Found',
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request, pk):
    try:
        wishlist = Wishlist.objects.get(pk=pk, user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    except Wishlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
