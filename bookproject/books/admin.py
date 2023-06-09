from django.contrib import admin
from .models import (
   StudentExtra, Book, IssuedBook, Carts, CartItems, BookReview, BookHistory
)

admin.site.register(
    [StudentExtra, Book, IssuedBook, Carts, CartItems, BookReview, BookHistory]
)