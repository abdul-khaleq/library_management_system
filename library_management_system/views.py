from django.shortcuts import render
from books. models import BookModel
from categories.models import CategoriesModel

def home(request, id = None):
    books = BookModel.objects.all()
    if id is not None:
        category = CategoriesModel.objects.get(id=id)
        books =BookModel.objects.filter(category=category)
    categories = CategoriesModel.objects.all()
    return render(request, 'home.html', {'books':books, 'categories':categories})