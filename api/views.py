from rest_framework import generics
from .models import Reader, Book, BorrowRecord
from .serializers import ReaderSerializer, BookSerializer, BorrowRecordSerializer

# Reader API Views
class ReaderListCreateView(generics.ListCreateAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

class ReaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

# Book API Views
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Borrow Record API Views
class BorrowRecordListCreateView(generics.ListCreateAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

class BorrowRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
