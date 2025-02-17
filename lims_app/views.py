from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from.models import Reader
from.models import *
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, BorrowRecord
from .forms import BorrowBookForm
from django.db.models import Q
from django.utils import timezone
# from .forms import BorrowRecordForm

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

def return_book(request, book_id):
    borrow_record = get_object_or_404(BorrowRecord, id=book_id)
    context = {'borrow_record': borrow_record}
    return render(request, 'books/return_book.html', {"return_books": return_book})

def book_list(request):
    books = Book.objects.all()  # Fetch all books
    return render(request, "books/book_list.html", {"books": books})

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'query': query})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def borrow_record_list(request):
    borrow_records = BorrowRecord.objects.all()
    return render(request, "books/borrow_record.html", {"borrow_records": borrow_records})
    
@login_required
def borrow_record(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        BorrowRecord.objects.create(
            user=request.user,
            book=book,
            borrowed_date=timezone.now(),
            return_date=timezone.now() + timezone.timedelta(days=5),
            is_returned=False
        )
        book.available = False
        book.save()
        return redirect('books/my_bag')  # Redirect to 'My Bag' page after borrowing
    else:
        return render(request, 'books/book_unavailable.html', {'book': book})

def my_bag(request):
    borrow_records = BorrowRecord.objects.filter(user=request.user, is_returned=False)
    return render(request, 'books/mybag.html', {'borrow_records': borrow_records})  

# def borrow_record(request, book_id):
#     if request.method == 'POST':
#         form = BorrowRecordForm(request.POST) # Bind the form
#         if form.is_valid():
#             try:
#                 borrow_record = form.save(commit=False) # Don't save yet
#                 borrow_record.book_id = book_id # Set book_id manually
#                 borrow_record.save()  # Try to save the record
#                 return redirect('my_bag')  # Redirect on success
#             except ValidationError as e:
#                 # Handle the validation error
#                 form.add_error(None, e)  # Add to form errors
#                 # Example: Render the form again with the error message
#                 return render(request, 'borrow_template.html', {'form': form, 'error_message': e}) # Or return form errors
#         else:
#             return render(request, 'borrow_template.html', {'form': form}) # Return form with errors
#     else:  # GET request
#         form = BorrowRecordForm()
#         return render(request, 'borrow_template.html', {'form': form})


# @login_required
# def return_book(request, book_id):
#     borrow_record = get_object_or_404(BorrowRecord, book_id=book_id, user=request.user, is_returned=False)
#     if request.method == 'POST':
#         borrow_record.is_returned = True
#         borrow_record.return_date = timezone.now()
#         borrow_record.save()
#         book = borrow_record.book
#         book.available = True
#         book.save()
#         return redirect('my_bag')  # Redirect to 'My Bag' page after returning
#     return render(request, 'return_book.html', {'borrow_record': borrow_record})
