from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from customers.models import Customer

class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    published_year = models.IntegerField()
    book_type = models.PositiveSmallIntegerField(choices=[(1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')])  
    isActive = models.BooleanField(default=True)  
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')

    def clean(self):
        if self.published_year > 2025:  
            raise ValidationError('Published year cannot be in the future.')

    def __str__(self):
        return self.title
    
class Loan(models.Model):
    cust_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="loans")
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)  
    loan_date = models.DateField(auto_now_add=True)                              
    due_date =  models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)      
    is_active = models.BooleanField(default=True)              

    def __str__(self):
        return f"Loan: {self.cust_id} - {self.book_id}"    