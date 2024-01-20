from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from author.models import UserModel
from books import models
from books.models import BookModel,BorrowHistoryModel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.views.generic import DetailView
from .models import BookModel, ReviewModel
from .forms import ReviewForm

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
@method_decorator(login_required, name='dispatch')
class AddBookCreateView(CreateView):
    model = BookModel
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'Book added Successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_valid(form)

class BookDetailView(DetailView):
    model = BookModel
    template_name = 'book_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = ReviewModel.objects.filter(book=book)
        try:
            context['review_book'] = BorrowHistoryModel.objects.get(user=self.request.user, book=book)
        except BorrowHistoryModel.DoesNotExist:
            context['review_book'] = None
        context['form'] = ReviewForm()
        return context
    
    def post(self, request, pk):
        book = BookModel.objects.get(pk=pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            
            review = form.cleaned_data['review']
            user = request.user
            if BorrowHistoryModel.objects.filter(user=user, title=book.title).exists():
                if ReviewModel.objects.filter(user=user, book=book).exists():
                    messages.warning(request, 'You have already reviewed this book.')
                else:
                    review = ReviewModel.objects.create(user=user, book=book, review=review)
                    review.save()
                    messages.success(request, 'Review added successfully.')
            else:
                messages.warning(request, 'You can only review books you have borrowed.')

        return redirect('book_details', pk=pk)

    
def borrowHistory(request, id):
    book = BookModel.objects.get(pk=id)
    user = UserModel.objects.get(user=request.user)
    if request.user:
        order_history =BorrowHistoryModel(
            book = book,
            title=book.title,
            description=book.description,
            price=book.price,
            balance_after_borrowed = user.balance - book.price,
            category=book.category,
            image=book.image,
            user=request.user,
            return_book =True,

        )
        if book.quantity >0:
            if user.balance >= book.price:
                user.balance -= book.price
                book.quantity -=1
                user.save()
                order_history.save()
                book.save()
                messages.success(request, 'Book borrowed Successfully')
                subject = 'welcome to Library Management System'
                message = f'Hi {request.user.username}, You borrowed Book Title {book.title} & Price {book.price} & Total balance {request.user.user.balance}. Go to profile to see your borrowed list.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                send_mail( subject, message, email_from, recipient_list )
            else:
                messages.success(request, 'You do not have enough money in your account')

    return redirect('homepage')