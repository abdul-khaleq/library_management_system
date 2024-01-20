from django.db import models
from categories.models import CategoriesModel
from django.contrib.auth.models import User

# Create your models here.
class BookModel(models.Model):
    title= models.CharField(max_length=55)
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads/')
    price =models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=10)
    def __str__(self):
        return f"Book name: {self.title}"

class BorrowHistoryModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    description = models.TextField()
    image = models.ImageField(upload_to='car/media/uploads/', blank=True, null=True)
    price = models.CharField(max_length=55)
    category = models.CharField(max_length=155)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    balance_after_borrowed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    return_book = models.BooleanField(default=False)

    def __str__(self):
        return f"name: {self.title}"

class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    review = models.TextField()
    cheated_on = models.DateTimeField(auto_now_add=True)
    # return_book = models.BooleanField(default=False)
    def __str__(self):
        return f"Reviewed by {self.user.first_name} {self.user.last_name}"
