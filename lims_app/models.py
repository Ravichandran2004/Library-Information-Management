from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
# from django.core.exceptions import ValidationError
from django.db.models import Q
# from django.utils import timezone
from datetime import timezone as dt_timezone
# from .models import Book

class Reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id = models.CharField(max_length=200)
    reader_name = models.CharField(max_length=200)
    reader_contact = models.CharField(max_length=200)
    reader_address = models.TextField()
    active = models.BooleanField(default=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    price_5_days = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0.00)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

def get_return_date():
    return datetime.now() + timedelta(days=5)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=Q(is_returned=False),
                name='unique_active_borrow'
            )
        ]

    def calculate_fee(self):
        """Calculate fee based on borrowed duration."""
        if not self.return_date:
            return 0  # No fee if not returned yet

        # Convert both dates to UTC
        borrowed_date = self.borrowed_date.astimezone(dt_timezone.utc)
        return_date = self.return_date.astimezone(dt_timezone.utc)

        days_borrowed = (return_date.date() - borrowed_date.date()).days

        # Ensure at least 1-day fee is charged
        if days_borrowed <= 0:
            days_borrowed = 1

        if days_borrowed <= 5:
            return self.book.price_5_days
        else:
            extra_days = days_borrowed - 5
            return self.book.price_5_days + (extra_days * self.book.daily_rate)

class APIRequestLog(models.Model):
    """Logs API requests without affecting existing data"""
    user = models.CharField(max_length=255, null=True, blank=True)
    path = models.TextField()
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    user_agent = models.TextField(null=True, blank=True)  # ✅ Added missing fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # ✅ Added missing fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code}"

def log_api_request(request, status_code):
    """Logs API requests automatically"""
    from django.utils.timezone import now
    APIRequestLog.objects.create(
        user=request.user.username if request.user.is_authenticated else None,  # ✅ Fixed user reference
        path=request.path,  # ✅ Fixed field name
        method=request.method,
        status_code=status_code,
        created_at=now(),  # ✅ Fixed field name
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        ip_address=request.META.get("REMOTE_ADDR"),
    )


# class APIRequestLog(models.Model):
#     """Logs API requests without affecting existing data"""
#     user = models.CharField(max_length=255, null=True, blank=True)
#     path = models.TextField()
#     method = models.CharField(max_length=10)
#     status_code = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.method} {self.path} - {self.status_code}"
#
# def log_api_request(request, status_code):
#     """Logs API requests automatically"""
#     from django.utils.timezone import now
#     APIRequestLog.objects.create(
#         user=request.user if request.user.is_authenticated else None,
#         endpoint=request.path,
#         method=request.method,
#         status_code=status_code,
#         timestamp=now(),
#         user_agent=request.META.get("HTTP_USER_AGENT", ""),
#         ip_address=request.META.get("REMOTE_ADDR"),
#     )
#
#

