from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddBookCreateView.as_view(), name='add_book'),
    path('borrow/<int:id>', views.borrowHistory, name='borrow'),
    path('detail/<int:pk>', views.BookDetailView.as_view(), name='book_details'),
]