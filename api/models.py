from lims_app.models import Book, Reader, BorrowRecord
from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta, datetime
from django.db.models import Q

class APIRequestLog(models.Model):
    """Logs API requests without affecting existing data"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()

    def __str__(self):
        return f'{self.method} {self.endpoint} - {self.status_code}'

