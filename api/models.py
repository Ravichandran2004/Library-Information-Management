from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.db.models import Q

class Reader(models.Model):
    reference_id = models.CharField(max_length=200, unique=True)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=200)
    reader_address = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.reader_name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    price_5_days = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

def get_return_date():
    return datetime.now() + timedelta(days=5)

class BorrowRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="api_borrow_records"
    )  # Change related_name to avoid conflict
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=Q(is_returned=False),
                name='api_unique_active_borrow'  # Renamed to make it unique
            )
        ]

    def calculate_fee(self):
        """Calculate fee based on borrowed duration."""
        if not self.return_date:
            return 0  # No fee if not returned yet

        days_borrowed = (self.return_date.date() - self.borrowed_date.date()).days

        if days_borrowed <= 0:
            days_borrowed = 1  # Minimum charge of 1 day

        if days_borrowed <= 5:
            return self.book.price_5_days
        else:
            extra_days = days_borrowed - 5
            return self.book.price_5_days + (extra_days * self.book.daily_rate)

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'
