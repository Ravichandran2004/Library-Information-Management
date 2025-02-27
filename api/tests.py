from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    def test_create_book(self):
        book = Book.objects.create(
            title="Sample Book",
            author="John Doe",
            published_date="2024-01-01",
            isbn="1234567890123",
            price=29.99
        )
        self.assertEqual(str(book), "Sample Book")
