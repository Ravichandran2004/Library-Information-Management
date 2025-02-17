from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
# Create your models here.
class Reader(models.Model): 
    def __str__(self):
        return self.reader_name
    reference_id=models.CharField(max_length=200) 
    reader_name=models.CharField(max_length=200) 
    reader_contact=models.CharField(max_length=200) 
    reader_address=models.TextField() 
    active=models.BooleanField(default=True)
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    price_5_days = models.DecimalField(max_digits=6, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

def get_return_date():
    return datetime.now() + timedelta(days=5)
class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(default=get_return_date)
    is_returned = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book', 'is_returned'], name='unique_borrow_record')
        ]
        
    def save(self, *args, **kwargs):
        if not self.pk and BorrowRecord.objects.filter(user=self.user, book=self.book, is_returned=self.is_returned).exists():
            raise ValidationError('Duplicate borrow record exists.')
        super().save(*args, **kwargs)
       
    def calculate_fee(self):
        """
        Calculates the return fee based on price_5_days and daily_rate.
        """
        print('40',self)
        days_borrowed = (datetime.now().date() - self.borrowed_date.date()).days  
        if days_borrowed <= 5:
            return self.book.price_5_days
        else:
            extra_days = days_borrowed - 5
            return self.book.price_5_days + (extra_days * self.book.daily_rate)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"