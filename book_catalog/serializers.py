from rest_framework import serializers
from .models import Author, Genre, Book, Review, Wishlist


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['book']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    average_rating = serializers.FloatField(read_only=True)
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'average_rating', 'in_wishlist']

    def get_in_wishlist(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user, book=obj).exists()
        return False


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        extra_fields = ['author', 'genre', 'reviews', 'average_rating', 'in_wishlist']

    def get_in_wishlist(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user, book=obj).exists()
        return False
