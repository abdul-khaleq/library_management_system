from django import forms
from . models import BookModel, ReviewModel

class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        # fields = '__all__'
        exclude = ['available_review']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['review']