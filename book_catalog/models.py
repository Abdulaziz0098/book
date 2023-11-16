from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

from account.models import User


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    publication_date = models.DateField()
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            return round(average_rating, 2)
        else:
            return 0.00


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
