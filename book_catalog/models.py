from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

from account.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    publication_date = models.DateField()
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
