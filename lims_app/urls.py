from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), # Or path('', views.home, name='home') for root URL
    path('readers/', views.readers_tab, name='readers_tab'),
    path('readers/', views.readers, name='readers_tab'),
    path('shop/', views.shopping, name='shopping'),
    path('save', views.save_student, name='save'),
    path('readers/add/', views.save_reader, name='save_reader'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/', views.book_list, name='book_list'),
]

