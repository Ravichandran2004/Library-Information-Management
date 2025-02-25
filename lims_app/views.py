from django.shortcuts import render
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
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
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import pandas as pd


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
            cursor.execute("SELECT * FROM lims_app_reader WHERE reader_name LIKE %s", [f"%{query}%"])
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
    if request.method == "POST":
        # Match the form fields EXACTLY:
        # name="reader_name", name="reader_contact", name="reader_ref_id", name="reader_address"
        reader_name = request.POST['reader_name']
        reader_contact = request.POST['reader_contact']
        reader_ref_id = request.POST['reader_ref_id']
        reader_address = request.POST['reader_address']

        # Create and save a new Reader
        Reader.objects.create(
            reader_name=reader_name,
            reader_contact=reader_contact,
            reference_id=reader_ref_id,
            reader_address=reader_address,
            active=True  # or however you set default
        )

        return redirect('/readers/')  # or wherever your readers list is

    # If GET, just show the page or redirect
    return render(request, 'readers.html')

def search_readers(request):
    query = request.GET.get('query', '')
    if query:
        readers = Reader.objects.filter(reader_name__icontains=query)
    else:
        readers = Reader.objects.all()
    return render(request, 'readers.html', {'readers': readers, 'query': query})
# def save_reader(request):
#     reader_item= Reader(reference_id=request.POST['reader_ref_id'],
#                         reader_name = request.POST['reader_name'],
#                         reader_contact = request.POST['reader_contact'],
#                         reader_address = request.POST['reader_Address'],
#                         active=True
#
#     )
#     reader_item.save()
#     return redirect('/readers')




@login_required
def borrow_record(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if BorrowRecord.objects.filter(user=user, book=book, is_returned=False).exists():
        messages.error(request, "You have already borrowed this book.")
        return redirect('book_detail', book_id=book.id)

    if not book.available:
        messages.error(request, "This book is currently unavailable.")
        return redirect('book_list')

    borrow = BorrowRecord.objects.create(
        user=user,
        book=book,
        borrowed_date=timezone.now(),
        return_date=timezone.now() + timezone.timedelta(days=7),  # 7-day borrow period
        is_returned=False
    )

    book.available = False
    book.save()

    messages.success(request, "Book borrowed successfully!")
    return redirect('book_list')

def return_book(request, book_id):
    record = get_object_or_404(BorrowRecord, pk=book_id)
    if request.method == 'POST':
        record.is_returned = True
        record.return_date = timezone.now()
        record.save()
        return redirect('returns')
    return render(request, 'books/returnbook.html', {'borrow_record': record})

def returns(request):
    returned_records = BorrowRecord.objects.filter(user=request.user, is_returned=True)
    return render(request, 'returns.html', {'returned_records': returned_records})



def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ) if query else Book.objects.all()

    return render(request, 'books/book_list.html', {'books': books, 'query': query})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def borrow_record_list(request):
    borrow_records = BorrowRecord.objects.all()
    return render(request, "books/borrow_record.html", {"borrow_records": borrow_records})

def my_bag(request):
    borrow_records = BorrowRecord.objects.filter(user=request.user, is_returned=False)
    return render(request, 'books/mybag.html', {'borrow_records': borrow_records})

def borrow_record_list(request):
    query = request.GET.get('q', '')
    records = BorrowRecord.objects.all()

    if query:
        records = records.filter(book__title__icontains=query)  # Example search filter

    paginator = Paginator(records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'borrow_record_list.html', {'page_obj': page_obj, 'query': query})


def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        price_5_days = request.POST['price_5_days']
        daily_rate = request.POST['daily_rate']
        available = request.POST['available'] == 'True'

        # Save book to the database
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            price_5_days=price_5_days,
            daily_rate=daily_rate,
            available=available
        )

        return redirect('book_list')  # Redirect to book list after adding
    return render(request, 'add_book.html')

# Upload Books View
def upload_book(request):
    if request.method == "POST" and request.FILES.get('book_file'):
        book_file = request.FILES['book_file']

        if book_file.name.endswith('.csv'):
            df = pd.read_csv(book_file)
        elif book_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(book_file)
        else:
            return render(request, 'upload_book.html', {'error': 'Invalid file format'})

        # Insert data into database
        for _, row in df.iterrows():
            Book.objects.create(
                title=row['title'],
                author=row['author'],
                isbn=row['isbn'],
                price_5_days=row['price_5_days'],
                daily_rate=row['daily_rate'],
                available=row['available']
            )

        return redirect('book_list')  # Redirect after upload
    return render(request, 'upload_book.html')

def add_book(request):
    if request.method == "POST":
        # Handle form data...
        # ...
        return redirect('book_list')

    # Render the template in the subfolder "books"
    return render(request, 'books/add_book.html')




def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn")
        price_5_days = request.POST.get("price_5_days")
        daily_rate = request.POST.get("daily_rate")
        available = request.POST.get("available") == "True"

        # Create new book entry
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            price_5_days=price_5_days,
            daily_rate=daily_rate,
            available=available
        )

        return JsonResponse({"message": "Book added successfully!"})  # Send response to AJAX

    return render(request, "books/add_book.html")  # This will rarely be used since the modal is in book_list.html


def upload_book(request):
    if request.method == 'POST':
        # process your file upload
        ...
        return redirect('book_list')

    # IMPORTANT: If it's in 'templates/books/', you must prefix with 'books/'
    return render(request, 'books/upload_book.html')

def upload_book(request: HttpRequest) -> HttpResponse:
    """
    Uploads a CSV or Excel file containing book data and saves it to the database.
    Expected columns (case-insensitive):
        title, author, isbn, price_5_days, daily_rate, available
    """
    if request.method == "POST" and request.FILES.get('book_file'):
        book_file = request.FILES['book_file']

        # 1. Detect file type
        if book_file.name.endswith('.csv'):
            df = pd.read_csv(book_file)
        elif book_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(book_file)
        else:
            messages.error(request, "Invalid file format. Please upload a CSV or Excel file.")
            return redirect('upload_book')

        # 2. Print columns for debugging
        # Convert columns to lowercase for easier comparison
        actual_columns = set(col.lower() for col in df.columns)
        print("DataFrame columns (lowercased):", actual_columns)

        # 3. Define the expected columns (lowercase)
        expected_columns = {'title', 'author', 'isbn', 'price_5_days', 'daily_rate', 'available'}

        # 4. Check if the file has all the needed columns
        missing_cols = expected_columns - actual_columns
        if missing_cols:
            messages.error(request, f"Missing columns in the file: {', '.join(missing_cols)}")
            return redirect('upload_book')

        # 5. (Optional) Rename columns to match exactly your model fields
        #    Only rename columns that exist. Use `errors='ignore'` to skip missing.
        df.rename(columns={
            'Title': 'title',
            'Author': 'author',
            'ISBN': 'isbn',
            'Price_5_days': 'price_5_days',
            'Daily_rate': 'daily_rate',
            'Available': 'available'
        }, inplace=True, errors='ignore')

        # 6. Insert data into the database
        uploaded_count = 0
        for _, row in df.iterrows():
            try:
                Book.objects.create(
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    price_5_days=row['price_5_days'],
                    daily_rate=row['daily_rate'],
                    available=row['available']
                )
                uploaded_count += 1
            except Exception as e:
                # If there's an error (e.g., duplicate ISBN), handle or log it
                print(f"Error uploading row: {e}")

        messages.success(request, f"Successfully uploaded {uploaded_count} book(s).")
        return redirect('book_list')

    # If GET request, just render the upload page
    return render(request, 'books/upload_book.html')

def toggle_availability(request, book_id):
    """
    Toggle a book's availability from True to False or False to True.
    """
    if request.method == "POST":
        book = get_object_or_404(Book, pk=book_id)
        book.available = not book.available  # Flip True to False or vice versa
        book.save()
    return redirect('book_list')

def book_list(request):
    # 1. Fetch all (or filtered) books
    query = request.GET.get('q', '')
    if query:
        # Example filter if you already had search logic
        books_list = Book.objects.filter(title__icontains=query)
    else:
        books_list = Book.objects.all()

    # 2. Use Paginator: 10 books per page (change 10 to whatever page size you want)
    paginator = Paginator(books_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 3. Pass page_obj to the template as "books"
    return render(request, 'books/book_list.html', {
        'books': page_obj,
        'query': query,  # so your search box still works
    })

def receipt(request, record_id):
    record = get_object_or_404(BorrowRecord, pk=record_id)
    # Optionally check if record.is_returned == True
    # or if record.user == request.user, etc.

    return render(request, 'receipt.html', {'record': record})

def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # creates a staff user
            return redirect('somewhere')  # e.g. staff list or login
    else:
        form = StaffRegistrationForm()
    return render(request, 'register_staff.html', {'form': form})