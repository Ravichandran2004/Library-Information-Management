from django.db import models

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
    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)  
    isbn = models.CharField(max_length=20, unique=True)
    genre = models.CharField(max_length=100)  
    description = models.TextField(blank=True, null=True)
    price_5_days = models.DecimalField(max_digits=6, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)