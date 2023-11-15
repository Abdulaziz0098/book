from django.urls import path

from book_catalog.views import author_view, genre_view, book_view, review_view, wish_view

urlpatterns = [
    path('authors/', author_view.author_list, name='author-list'),
    path('authors/create/', author_view.create_author, name='create-author'),
    path('authors/<int:pk>/', author_view.get_author, name='get-author'),
    path('authors/<int:pk>/update/', author_view.update_author, name='update-author'),
    path('authors/<int:pk>/delete/', author_view.delete_author, name='delete-author'),

    path('genres/', genre_view.genre_list, name='genre-list'),
    path('genres/create/', genre_view.create_genre, name='create-genre'),
    path('genres/<int:pk>/', genre_view.get_genre, name='get-genre'),
    path('genres/<int:pk>/update/', genre_view.update_genre, name='update-genre'),
    path('genres/<int:pk>/delete/', genre_view.delete_genre, name='delete-genre'),

    path('books/', book_view.book_list, name='book-list'),
    path('books/create/', book_view.create_book, name='create-book'),
    path('books/<int:pk>/', book_view.get_book, name='get-book'),
    path('books/<int:pk>/update/', book_view.update_book, name='update-book'),
    path('books/<int:pk>/delete/', book_view.delete_book, name='delete-book'),

    path('reviews/', review_view.review_list, name='review-list'),
    path('reviews/create/', review_view.create_review, name='create-review'),
    path('reviews/<int:pk>/', review_view.get_review, name='get-review'),
    path('reviews/<int:pk>/update/', review_view.update_review, name='update-review'),
    path('reviews/<int:pk>/delete/', review_view.delete_review, name='delete-review'),

    path('wishlists/', wish_view.wishlist_list, name='wishlist-list'),
    path('wishlists/create/', wish_view.create_wishlist, name='create-wishlist'),
    path('wishlists/<int:pk>/', wish_view.get_wishlist, name='get-wishlist'),
    path('wishlists/<int:pk>/update/', wish_view.update_wishlist, name='update-wishlist'),
    path('wishlists/<int:pk>/delete/', wish_view.delete_wishlist, name='delete-wishlist'),
]
