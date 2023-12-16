
from django.contrib import admin
from django.urls import path,include
from bookapp.views import *
urlpatterns = [
    path('add_new', addNewBook, name='add new book'), 
    path('add_old', addOldBook, name='add old book'), 
    path('book_search', searchBook, name='book search'), 
    path('book_request', book_request, name='book request'),
    path('history', history, name='history'),
    path('req_all', req_all, name='issued'),
    path('issued', issued, name='issued'),
    path('all_issued', all_issued, name='all issued'),
    path('close', close, name='close'),
]
