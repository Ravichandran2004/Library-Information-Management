from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from lims_app.models import Book, BorrowRecord
from django.utils import timezone
from datetime import timedelta

class BorrowRecordTestCase(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.user = User.objects.create(username="testuser")

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="123456789",
            price_5_days=25.00,
            daily_rate=10.00
        )

    def test_duplicate_borrow_not_allowed(self):
        """A user should not be able to borrow the same book twice before returning it."""
        BorrowRecord.objects.create(user=self.user, book=self.book, is_returned=False)

        with self.assertRaises(IntegrityError):
            BorrowRecord.objects.create(user=self.user, book=self.book, is_returned=False)

    def test_can_borrow_again_after_return(self):
        """A user should be able to borrow the same book again after returning it."""
        record = BorrowRecord.objects.create(user=self.user, book=self.book, is_returned=False)
        record.is_returned = True
        record.save()

        new_record = BorrowRecord.objects.create(user=self.user, book=self.book, is_returned=False)
        self.assertEqual(BorrowRecord.objects.filter(user=self.user, book=self.book).count(), 2)

    def test_fee_calculation(self):
        """Test that the fee calculation works correctly."""
        borrowed_date = timezone.now()
        return_date = borrowed_date + timedelta(days=6)  # Ensure borrowing is > 5 days

        borrow_record = BorrowRecord.objects.create(
            user=self.user,
            book=self.book,
            borrowed_date=borrowed_date,
            return_date=return_date,
            is_returned=True
        )

        expected_fee = self.book.price_5_days + (1 * self.book.daily_rate)  # 6 days fee

        print(f"Borrowed date: {borrow_record.borrowed_date}")
        print(f"Return date: {borrow_record.return_date}")
        print(f"Expected fee: {expected_fee}, Calculated fee: {borrow_record.calculate_fee()}")

        self.assertEqual(borrow_record.calculate_fee(), expected_fee)

    def test_fee_for_same_day_return(self):
        """Test fee calculation when the book is returned on the same day."""
        borrow_record = BorrowRecord.objects.create(
            user=self.user, book=self.book, borrowed_date=timezone.now(), return_date=timezone.now(), is_returned=True
        )
        expected_fee = self.book.price_5_days
        self.assertEqual(borrow_record.calculate_fee(), expected_fee)
