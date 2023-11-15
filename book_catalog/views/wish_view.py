from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from book_catalog.models import Wishlist
from book_catalog.serializers import WishlistSerializer


@api_view(['GET'])
def wishlist_list(request):
    wishlists = Wishlist.objects.all()
    serializer = WishlistSerializer(wishlists, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_wishlist(request):
    serializer = WishlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_wishlist(request, pk):
    try:
        wishlist = Wishlist.objects.get(pk=pk)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    except Wishlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_wishlist(request, pk):
    try:
        wishlist = Wishlist.objects.get(pk=pk)
        serializer = WishlistSerializer(wishlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Wishlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_wishlist(request, pk):
    try:
        wishlist = Wishlist.objects.get(pk=pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
