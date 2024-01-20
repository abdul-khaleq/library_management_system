from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def add_category(request):
    if request.method == 'POST':
        brand_form = forms.CategoriesForm(request.POST)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('homepage')
    else:
        brand_form = forms.CategoriesForm()
    return render(request, 'add_category.html', {'form': brand_form})