import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Reader, Book, BorrowRecord
from datetime import datetime, timedelta


class ReaderType(DjangoObjectType):
    class Meta:
        model = Reader

class BookType(DjangoObjectType):
    class Meta:
        model = Book

class BorrowRecordType(DjangoObjectType):
    class Meta:
        model = BorrowRecord

class UserType(DjangoObjectType):
    class Meta:
        model = User



class Query(graphene.ObjectType):
    all_readers = graphene.List(ReaderType)
    all_books = graphene.List(BookType)
    all_borrow_records = graphene.List(BorrowRecordType)
    all_users = graphene.List(UserType)
    available_books = graphene.List(BookType)

    def resolve_all_readers(self, info):
        return Reader.objects.all()

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_all_borrow_records(self, info):
        return BorrowRecord.objects.all()

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_available_books(self, info):
        return Book.objects.filter(available=True)



class BorrowBookMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        book_id = graphene.Int(required=True)
        days = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user_id, book_id, days):
        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)

            if not book.available:
                return BorrowBookMutation(success=False, message="Book is currently unavailable.")

            # Check if user already borrowed the book
            if BorrowRecord.objects.filter(user=user, book=book, is_returned=False).exists():
                return BorrowBookMutation(success=False, message="You have already borrowed this book.")

            return_date = datetime.now() + timedelta(days=days)
            BorrowRecord.objects.create(user=user, book=book, return_date=return_date, is_returned=False)

            # Mark book as unavailable
            book.available = False
            book.save()

            return BorrowBookMutation(success=True, message="Book borrowed successfully.")
        except User.DoesNotExist:
            return BorrowBookMutation(success=False, message="User not found.")
        except Book.DoesNotExist:
            return BorrowBookMutation(success=False, message="Book not found.")
        except Exception as e:
            return BorrowBookMutation(success=False, message=str(e))



class ReturnBookMutation(graphene.Mutation):
    class Arguments:
        borrow_record_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, borrow_record_id):
        try:
            borrow_record = BorrowRecord.objects.get(id=borrow_record_id, is_returned=False)
            borrow_record.is_returned = True
            borrow_record.save()

            # Mark book as available again
            borrow_record.book.available = True
            borrow_record.book.save()

            return ReturnBookMutation(success=True, message="Book returned successfully.")
        except BorrowRecord.DoesNotExist:
            return ReturnBookMutation(success=False, message="Borrow record not found or already returned.")
        except Exception as e:
            return ReturnBookMutation(success=False, message=str(e))



class CreateReader(graphene.Mutation):
    class Arguments:
        reference_id = graphene.String(required=True)
        reader_name = graphene.String(required=True)
        reader_contact = graphene.String(required=True)
        reader_address = graphene.String(required=True)
        active = graphene.Boolean(required=True)

    reader = graphene.Field(ReaderType)

    def mutate(self, info, reference_id, reader_name, reader_contact, reader_address, active):
        reader = Reader(
            reference_id=reference_id,
            reader_name=reader_name,
            reader_contact=reader_contact,
            reader_address=reader_address,
            active=active
        )
        reader.save()
        return CreateReader(reader=reader)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        isbn = graphene.String(required=True)
        price_5_days = graphene.Float(required=True)
        daily_rate = graphene.Float(required=True)
        available = graphene.Boolean(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, isbn, price_5_days, daily_rate, available):
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            price_5_days=price_5_days,
            daily_rate=daily_rate,
            available=available
        )
        book.save()
        return CreateBook(book=book)


class CreateBorrowRecord(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        book_id = graphene.ID(required=True)
        return_date = graphene.DateTime(required=False)

    borrow_record = graphene.Field(BorrowRecordType)

    def mutate(self, info, user_id, book_id, return_date=None):
        user = User.objects.get(pk=user_id)
        book = Book.objects.get(pk=book_id)

        if not book.available:
            raise Exception("Book is not available.")

        borrow_record = BorrowRecord(
            user=user,
            book=book,
            return_date=return_date,
            is_returned=False
        )
        borrow_record.save()

        book.available = False
        book.save()

        return CreateBorrowRecord(borrow_record=borrow_record)


class Mutation(graphene.ObjectType):
    create_reader = CreateReader.Field()
    create_book = CreateBook.Field()
    create_borrow_record = CreateBorrowRecord.Field()
    borrow_book = BorrowBookMutation.Field()
    return_book = ReturnBookMutation.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
