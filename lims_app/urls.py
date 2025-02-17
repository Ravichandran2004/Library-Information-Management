from django.urls import path
from . import views
from .views import book_list, book_detail, return_book
from .views import borrow_record_list

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('readers/', views.readers_tab, name='readers_tab'),
    path('readers/', views.readers, name='readers_tab'),
    path('shop/', views.shopping, name='shopping'),
    path('save', views.save_student, name='save'),
    path('readers/add/', views.save_reader, name='save_reader'),
    # Book Management URLs
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow/<int:book_id>/', views.borrow_record, name='borrow_record'),
    path('mybag/', views.my_bag, name='my_bag'),
    path('return/<int:book_id>/', views.return_book, name='returnbook'), 
    # path('returnbookS/', views.return_book, name='return_book'),
    
    
    
    
    
    
    # path('retunrbook', views.return_book, name='return_book'),
    # path('return/<int:book_id>/', views.return_book, name='return_book'),
    
    # Or path('', views.home, name='home') for root URL
    # path('books/return/<int:borrow_id>/', views.return_book, name='return_book'),
]

