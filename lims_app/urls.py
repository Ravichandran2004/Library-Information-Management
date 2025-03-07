from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from lims_app import views
from .views import MyBagView, my_bag_api

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('readers/', views.readers_tab, name='readers_tab'),
    path('readers/', views.readers, name='readers_tab'),
    path('shop/', views.shopping, name='shopping'),
    path('save', views.save_student, name='save'),
    path('readers/add/', views.save_reader, name='save_reader'),
    path('search/', views.search_readers, name='search_readers'),
    # path('readers/add/', views.save_reader, name='save_reader'),
    # Book Management URLs
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow/<int:book_id>/', views.borrow_record, name='borrow_record'),
    path('mybag/', views.my_bag, name='my_bag'),
    path('my bag-api/', MyBagView.as_view(), name='my_bag_api'),  # New API view
    path('my bag-api/', my_bag_api, name='my_bag_api'),
    path('return-book/<int:book_id>/', views.return_book, name='return_book'),
    path('returns/', views.returns, name='returns'),
    path('add/', views.add_book, name='add_book'),
    path('upload/', views.upload_book, name='upload_book'),
    path('', views.book_list, name='book_list'),  # Example
    path('books/<int:book_id>/toggle_availability/', views.toggle_availability, name='toggle_availability'),
    path('returns/receipt/<int:record_id>/', views.receipt, name='receipt'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

]

