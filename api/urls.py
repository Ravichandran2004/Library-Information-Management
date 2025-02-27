from django.urls import path
from .views import (
    ReaderListCreateView, ReaderDetailView,
    BookListCreateView, BookDetailView,
    BorrowRecordListCreateView, BorrowRecordDetailView
)

urlpatterns = [
    path('readers/', ReaderListCreateView.as_view(), name='reader-list'),
    path('readers/<int:pk>/', ReaderDetailView.as_view(), name='reader-detail'),

    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('borrow-records/', BorrowRecordListCreateView.as_view(), name='borrow-list'),
    path('borrow-records/<int:pk>/', BorrowRecordDetailView.as_view(), name='borrow-detail'),
]
