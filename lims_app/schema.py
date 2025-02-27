# lims_app/schema.py

import graphene
from graphene_django import DjangoObjectType
from .models import Reader, Book, BorrowRecord
from django.contrib.auth.models import User

# Define GraphQL types for each model
class ReaderType(DjangoObjectType):
    class Meta:
        model = Reader
        fields = ('id', 'reference_id', 'reader_name', 'reader_contact', 'reader_address', 'active')

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'isbn', 'price_5_days', 'daily_rate', 'available')

class BorrowRecordType(DjangoObjectType):
    class Meta:
        model = BorrowRecord
        fields = ('id', 'user', 'book', 'borrowed_date', 'return_date', 'is_returned')

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')



# Define Query class
class Query(graphene.ObjectType):
    all_readers = graphene.List(ReaderType)
    all_books = graphene.List(BookType)
    all_borrow_records = graphene.List(BorrowRecordType)
    all_users = graphene.List(UserType)

    def resolve_all_readers(root, info):
        return Reader.objects.all()

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_all_borrow_records(root, info):
        return BorrowRecord.objects.all()

    def resolve_all_users(root, info):
        return User.objects.all()

# Define Mutations for creating records
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
        borrow_record = BorrowRecord(
            user=user,
            book=book,
            return_date=return_date,
            is_returned=False
        )
        borrow_record.save()
        return CreateBorrowRecord(borrow_record=borrow_record)

# Define the Mutation class
class Mutation(graphene.ObjectType):
    create_reader = CreateReader.Field()
    create_book = CreateBook.Field()
    create_borrow_record = CreateBorrowRecord.Field()

# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
