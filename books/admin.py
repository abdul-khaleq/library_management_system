from django.contrib import admin
from .models import BookModel,BorrowHistoryModel, ReviewModel
# Register your models here.
admin.site.register(BookModel)
admin.site.register(BorrowHistoryModel)
admin.site.register(ReviewModel)