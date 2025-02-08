from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from.models import Reader
from.models import *
from django.db import connection
from django.shortcuts import render, get_object_or_404
from .models import Book  

# Create your views here.
def home(request):
    return render(request, 'home.html',context={"current_tab":"home"})

def readers(request):
    return render(request, 'readers.html',context={"current_tab":"readers"})

def shopping(request):
    return HttpResponse("Welcome to Shopping")

def save_student(request):
    student_name =request.POST['student_name']
    return render(request, 'Welcome.html',context={'student_name':student_name})
    
def readers_tab(request):
    if request.method =="GET":
        readers = Reader.objects.all()
    # This line of code is rendering the 'readers.html' template with the context data provided. The
    # template will be displayed to the user with the current tab set to "readers" and the list of
    # readers passed in the context variable 'readers'. This allows the template to access and display
    # the list of readers in the HTML page.
        print("Readers",readers)
        return render(request, "readers.html",
                      context={"current_tab":"readers",
                               "readers":readers})

    else:
        query = request.POST.get('query', '')
        with connection.cursor() as cursor:
            cursor.execute("SELECT* FROM lims_app_reader where reader_name LIKE '%"+query+"%'")
            rows = cursor.fetchall()
            readers = []
            for row in rows:
                reader = Reader(id=row[0],
                                reference_id=row[1],
                                reader_name=row[2],
                                reader_contact=row[3],
                                reader_address=row[4],
                                active=row[5] 
                            )
                readers.append(reader)
                return render(request, "readers.html", context={"current_tab": "readers", "readers": readers, "query": query})
                return render(request, "readers.html",
                      context={"current_tab":"readers",
                               "readers":readers})
        

def save_reader(request):
    reader_item= Reader(reference_id=request.POST['reader_ref_id'],
                        reader_name = request.POST['reader_name'],
                        reader_contact = request.POST['reader_contact'],
                        reader_address = request.POST['reader_Address'],
                        active=True
    )
    reader_item.save()
    return redirect('/readers')

# def book_detail(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)  # Get the book or show 404 error
#     return render(request, 'library/book.html', {'book': book})  # Pass the book to the template

def book_detail(request, book_id):
    """
    View to display details of a specific book.

    Args:
        request: The HTTP request object.
        book_id: The ID of the book to display.

    Returns:
        A rendered HTML template (book.html) with the book details.
    """
    book = get_object_or_404(Book, pk=book_id)  # Retrieve the book or show 404
    return render(request, 'library/book.html', {'book': book})  # Pass book to the template

def book_list(request):
    books = Book.objects.all()
    return render(request, 'lims_app/book_list.html', {'books': books}) 