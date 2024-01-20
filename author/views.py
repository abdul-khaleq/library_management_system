from typing import Any
from django.shortcuts import render, redirect, HttpResponseRedirect
from .import forms
from .import models
from author.models import UserModel
from books.models import BookModel
from books.models import BorrowHistoryModel
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import  LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from books.models import BorrowHistoryModel

from django.conf import settings
from django.core.mail import send_mail

class UserSignUpView(CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('user_login')
    form_class = forms.SignUpForm
    success_message = "account created successfully"

class UserLoginView(LoginView):
    template_name = 'signup.html'
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in info incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

class LogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('user_login')

@login_required
def profile(request):
    user = request.user
    books = BorrowHistoryModel.objects.filter(user=user)
    return render(request, 'profile.html', {'borrowedbooks': books})

def deposit(request):
    if request.method == 'POST':
        user = models.UserModel.objects.get(user=request.user)
        form = forms.DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user.balance += amount
            user.save()
            messages.success(request, f'Deposited ${amount} Successfully')
            subject = 'welcome to Library Management System'
            message = f'Hi {request.user.username}, You deposited ${amount} to your account.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return redirect('homepage')
            
    else:
        form = forms.DepositForm()
    return render(request,'deposit.html',{'form':form})

def return_book(request, id):
    returnBook = BorrowHistoryModel.objects.get(pk=id)
    User = UserModel.objects.get(user=request.user)
    book = BookModel.objects.get(title=returnBook.title)

    User.balance += int(float(returnBook.price))
    book.quantity += 1
    book.save()
    User.save()
    messages.success(request, f'Book return Successfully and ${returnBook.price} added to your account')
    returnBook.delete()
    return redirect('homepage')

