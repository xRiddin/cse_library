from email import message
from turtle import st
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Book, Users, Magazine, File
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
# from .forms import Login
from .forms import SearchForm, BookForm, MagForm, addMagazine, UserForm
from datetime import date, datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from email.message import EmailMessage
from django.contrib.auth.decorators import permission_required
from .decorators import group_required
from django.contrib.auth.models import Group





def login_user(request):
    if request.method == 'POST':
        id_number = request.POST['usn']
        password = request.POST['password']
        user = authenticate(request, username=id_number, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 1:
                return redirect('librarian')
            elif user.user_type == 2:
                return redirect('staff_dashboard', id=user.id)
            else:
                return redirect('student', usn_id=user.id_number)
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_user')        
    return render(request, 'login.html', {})


@login_required()
@group_required('student')
def student(request, usn_id):
    u = get_object_or_404(Users, id_number=usn_id)
    issued_books = u.issued_book.all()  # Retrieve the issued books for the user
    book_list = []
    for book in issued_books:
        book_list.append({
            'id': book.id,
            'name': book.name,
            'isbn': book.isbn,
            'edition': book.edition,
            'author': book.author,
            'issue_date': book.issue_date,
            'available_on': book.ret_date,
        })
    context = {
        'name': u.name,
        'phone': u.phone,
        'usn': u.id_number,
        'email': u.email,
        'fine': u.fine,
        'issued': book_list,
    }
    messages.success(request, 'you have logged in...')
    return render(request, 'user.html', context)

@login_required()
@group_required('staff')
def staff_about(request, id):
    u = get_object_or_404(Users, id=id)
    context = {
        'name': u.name,
        'phone': u.phone,
        'staff_id': u.id_number,
        'email': u.email,
        'fine': u.fine,
        'issued': u.issued_book,
    }
    messages.success(request, 'you have logged in...')
    return render(request, 'user.html', context)


@login_required()
@permission_required('librarian')
def librarian(request):
    return render(request, 'librarian.html', {})


@login_required()
@permission_required('librarian')
def lib_book(request):
    obj = Book.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'name': i.name,
            'isbn': i.isbn,
            'edition': i.edition,
            'author': i.author,
            'copies': i.copies,
            'reference': i.reference,
            'issue_date': i.issue_date,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "lib_book.html", {'list': lis})


@login_required()
@permission_required('librarian')
def lib_mag(request):
    obj = Magazine.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'name': i.name,
            'isbn': i.isbn,
            'author': i.author,
            'category': i.category,
            'edition': i.edition,
        })
    print(lis)
    return render(request, "lib_mag.html", {'list': lis})


@login_required()
@permission_required('librarian')
def lib_staff(request):
    obj = Users.objects.filter(user_type=2)
    lis = []
    for i in obj:
        if i.issued_book.all():
            for book in i.issued_book.all():
                lis.append({
            'id': i.id,
            'name': i.name,
            'staff_id': i.id_number,
            'email': i.email, 
            'phone': i.phone,
            'fine': i.fine,
            'issued_book': book,
            'ret_date': book.ret_date,
            #'issued_reference': i.issued_reference,
            })
        else:
            lis.append({
                'id': i.id,
                'name': i.name,
                'staff_id': i.id_number,
                'email': i.email,
                'phone': i.phone,
                'fine': i.fine,
                'issued_book': None,
            })
    print(lis)
    return render(request, "lib_staff.html", {'list': lis})


@login_required()
@permission_required('librarian')
def lib_student(request):
    obj = Users.objects.filter(user_type=3)
    lis = []
    for i in obj:
        if i.issued_book.all():
            for book in i.issued_book.all():
                lis.append({
                    'id': i.id,
                    'name': i.name,
                    'usn': i.id_number,
                    'email': i.email,
                    'phone': i.phone,
                    'fine': i.fine,
                    'issued_book': book,
                    'ret_date': book.ret_date,

                    #'issued_reference': i.issued_Reference,
                })
        else:
            lis.append({
                'id': i.id,
                'name': i.name,
                'usn': i.id_number,
                'email': i.email,
                'phone': i.phone,
                'fine': i.fine,
                'issued_book': None,
                })

    print(lis)
    return render(request, "lib_student.html", {'list': lis})


@login_required()
@permission_required('librarian')
def lib_auto(request):
    students = Users.objects.filter(user_type=3)
    for student in students:
        if student.fine > 0:
            subject = 'Fine repayment'
            body = f"Please pay your fine of Rs. {student.fine} as soon as possible."
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [student.email],
            )
    staff = Users.objects.filter(user_type=2)
    for staff in staff:
        if staff.fine > 0:
            subject = 'Fine repayment'
            body = f"Please pay your fine of Rs. {staff.fine} as soon as possible."
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [staff.email],
            )
    return HttpResponse('Email sent successfully')


@login_required()
@permission_required('librarian')
def lib_issue(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        isbn = request.POST.get('isbn')
        ret = request.POST.get('return_date')

        print(id, isbn)
        book = Book.objects.filter(isbn=isbn).first()
        user = Users.objects.filter(id_number=id).first()
        if user and book:
            if user.user_type == 3:      
                if Book.objects.filter(issue_to=user.id_number, isbn=isbn).exists():
                    messages.error(request, 'This book is already issued to the student')
                    return redirect('lib_issue')
                if user.issued_book.all().count() >= 3:
                    messages.error(request, 'You can issue only 2 books')
                    return redirect('lib_issue')
                if book.copies == 0:
                    messages.error(request, 'Book not available')
                    return redirect('lib_issue')
                
                if user.fine == 0:
                    user.issued_book.add(book)
                else:
                    messages.error(request, 'You have fine of Rs.'+str(user.fine))
                    return redirect('lib_issue') 
                if ret:
                    book.ret_date = ret
                else:
                    book.ret_date = date.today() + timedelta(days=15)
                book.issue_to = str(user.id_number)
                book.issue_date = date.today()
                book.copies -= 1
                user.save()
                book.save()
                context = {
                        'name': user.name,
                        'book': book.name,
                        'issue_date': book.issue_date,
                        'return_date': book.ret_date,
                        }
                messages.success(request, 'Book issued successfully')
                return render(request, 'lib_issue.html', context)
            
            if user.user_type == 2:
                if user.issued_book.filter(isbn=isbn).exists():
                    messages.error(request, 'This book is already issued to the staff')
                    return redirect('lib_issue')
                if user.issued_book.count() >= 5:
                    messages.error(request, 'You can issue only 5 books')
                    return redirect('lib_issue')
                if book and book.copies == 0:
                    messages.error(request, 'Book not available')
                    return redirect('lib_issue')
                
                if user.fine > 0:
                    messages.error(request, 'You have fine of Rs.'+str(user.fine))
                    return redirect('lib_issue')
                else:
                    user.issued_book.add(book)
                    if ret:
                        book.ret_date = ret
                    else:
                        book.ret_date = date.today() + timedelta(days=60)
                    book.issue_date = date.today()
                    book.issue_to = str(user.id_number)
                    book.copies -= 1
                    user.save()
                    book.save()
                    context = {
                        'name': user.name,
                        'book': book.name,
                        'issue_date': book.issue_date,
                        'return_date': book.ret_date,
                    }
                    messages.success(request, 'Book issued successfully')
                    return render(request, 'lib_issue.html', context)
        else:
            messages.error(request, 'Invalid ID')
            return redirect('lib_issue')
    return render(request, 'lib_issue.html', {})


@login_required()
@permission_required('librarian')
def lib_return(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        isbn = request.POST.get('isbn')
        print(id, isbn)
        book = Book.objects.filter(isbn=isbn).first()
        user = Users.objects.filter(id_number=id).first()
        if user and book:
            if user.issued_book.filter(isbn=isbn).exists():
                user.save()
                if user.fine > 0:
                    messages.error(request, 'You have fine of Rs.'+str(user.fine))
                    return redirect('lib_return')
                user.issued_book.remove(book)
                book.issue_to = None
                book.issue_date = None
                book.ret_date = None
                book.copies += 1
                user.save()
                book.save()
                context = {
                'name': user.name,
                'book': book.name,
                'issue_date': book.issue_date,
                'return_date': book.ret_date,
                'fine': user.fine,
                }
                messages.success(request, 'Book returned successfully')
                return render(request, 'lib_return.html', context)
            else:
                messages.error(request, "Invalid, no book issued")
                return redirect('lib_return')
        else:
            messages.error(request, 'Invalid ID')
            return redirect('lib_return')
    return render(request, 'lib_return.html', {})


@login_required()
@permission_required('librarian')
def repay_due(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        amount = request.POST.get('amount')
        user = Users.objects.filter(id_number=id).first()
        if user and amount:
            if user.fine > 0:
                if user.fine > int(amount):
                    user.fine -= int(amount)
                    user.save()
                elif user.fine == int(amount):
                    user.fine = 0
                    user.save()
                else:
                    messages.error(request, 'Invalid amount')
                    return redirect('repay_due')

                context = {
                    'name': user.name,
                    'fine': user.fine,
                }
                messages.success(request, 'Fine paid successfully')
                return render(request, 'payment.html', context)
            else:
                messages.error(request, 'You have no fine')
                return redirect('repay_due')
        else:
            messages.error(request, 'Invalid details')
            return redirect('repay_due')
    return render(request, 'payment.html', {})
                

@login_required()
@permission_required('librarian')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book edited successfully')
            return redirect('lib_book')
        else:
            messages.error(request, 'Invalid details')
            print(form.errors)  # Debugging statement
            return redirect('lib_book')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})


@login_required()
@permission_required('librarian')
def edit_magazine(request, magazine_id):
    magazine = get_object_or_404(Magazine, id=magazine_id)
    if request.method == "POST":
        form = MagForm(request.POST, instance=magazine)
        if form.is_valid():
            form.save()
            return redirect('lib_mag')
    else:
        form = MagForm(instance=magazine)
    return render(request, 'edit_magazine.html', {'form': form})

"""
@login_required()
@permission_required('librarian')
def edit_reference(request, reference_id):
    reference = get_object_or_404(Reference, id=reference_id)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            return redirect('lib_reference')
    else:
        form = MagForm(instance=reference)
    return render(request, 'edit_reference.html', {'form': form})
"""


@login_required()
@permission_required('librarian')
def edit_student(request, id):
    student = get_object_or_404(Users, id=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student edited successfully')
            return redirect('lib_student')
        else:
            messages.error(request, 'Invalid details')
            return redirect('lib_student')
    else:
        form = UserForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})


@login_required()
@permission_required('librarian')
def edit_staff(request, id):
    staff = get_object_or_404(Users, id=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff edited successfully')
            return redirect('lib_staff')
        else:
            messages.error(request, 'Invalid details')
            return redirect('lib_staff')
    else:

        form = UserForm(instance=staff)
    return render(request, 'edit_staff.html', {'form': form})


@login_required()
@group_required('student', 'staff')
def books(request, name=None):
    user = Users.objects.get(username=request.user.username)
    if user.user_type not in [2, 3]:  # 2 and 3 are the user types for staff and student
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login_user')
    obj = Book.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'copies': i.copies,
            'edition': i.edition,
            'author': i.author,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "book.html", {'list': lis})


"""
@login_required()
@permission_required('view_magazine')
def reference(request):
    obj = Reference.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'copies': i.copies,
            'edition': i.edition,
            'author': i.author,
        })
    print(lis)
    return render(request, "reference.html", {'list': lis})
"""


@login_required()
@group_required('student', 'staff')
def mag(request):
    user = Users.objects.get(username=request.user.username)
    if user.user_type not in [2, 3]:  # 2 and 3 are the user types for staff and student
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login_user')
    obj = Magazine.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'author': i.author,
            'category': i.category,
            'edition': i.edition,
        })
    print(lis)
    return render(request, "mag.html", {'list': lis})

"""
@login_required()
def createuser(request):
    print(request.user)
    form = addStudent(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'createuser.html', context)
"""

@login_required()
@permission_required('librarian')
def add_book(request):
    print(request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        isbn = request.POST.get('isbn')
        author = request.POST.get('author')
        copies = request.POST.get('copies')
        reference = request.POST.get('reference', False)
        edition = request.POST.get('edition')
        category = request.POST.get('category')
        if name and isbn and author and copies and category:
            if Book.objects.filter(isbn=isbn).exists():
                messages.error(request, 'Book already exists')
                return redirect('add_book')
            else:
                book = Book(name=name, isbn=isbn, author=author, copies=copies, category=category, edition=edition, reference=reference)
                book.save()
                messages.success(request, 'Book added successfully')
                return redirect('add_book')
        return render(request, 'add_book.html', {})
    else:
        return render(request, 'add_book.html', {})

@login_required()
@permission_required('librarian')
def add_magazine(request):
    print(request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        isbn = request.POST.get('isbn')
        author = request.POST.get('author')
        category = request.POST.get('category')
        edition = request.POST.get('edition')
        if name and isbn and author and edition and category:
            if Magazine.objects.filter(isbn=isbn).exists():
                messages.error(request, 'Magazine already exists')
                return redirect('add_magazine')
            else:
                magazine = Magazine(name=name, isbn=isbn, author=author, category=category, edition=edition)
                magazine.save()
                messages.success(request, 'Magazine added successfully')
                return redirect('add_magazine')
        return render(request, 'add_magazine.html', {})

    return render(request, 'add_magazine.html', {})


@login_required()
@permission_required('librarian')
def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if name and staff_id and email and phone and password:
            if Users.objects.filter(username=staff_id).exists():
                messages.error(request, 'Staff already exists')
                return redirect('add_staff')
            else:
                user = Users.objects.create_user(username=staff_id, id_number=staff_id, email=email, password=password, name=name, phone=phone, user_type=2)
                staff_group = Group.objects.get(name='staff')
                staff_group.user_set.add(user)
                user.save()
                messages.success(request, 'Staff added successfully')
                return redirect('add_staff')
        return render(request, 'add_staff.html', {})
    else:
        return render(request, 'add_staff.html', {})
    
@login_required()
@permission_required('librarian')
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        usn = request.POST.get('usn')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if name and usn and email and phone and password:
            if Users.objects.filter(username=usn).exists():
                messages.error(request, 'Student already exists')
                return redirect('add_student')
            else:
                user = Users.objects.create_user(username=usn, id_number=usn, email=email, password=password, name=name, phone=phone, user_type=3)
                student_group = Group.objects.get(name='student')    
                student_group.user_set.add(user)
                user.save()
                messages.success(request, 'Student added successfully')
                return redirect('add_student')
        return render(request, 'add_student.html', {})
    else:
        return render(request, 'add_student.html', {})

"""
@login_required()
@permission_required('librarian')   
def add_reference(request):
    print(request.user)
    form = addReference(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'add_reference.html', context)

def home(request):
    return render(request, 'home.html', {})
"""


def rules(request, id=None):
    if id:
        t = get_object_or_404(Users, id=id)
        context = {
            'name': t.name,
        }
        return render(request, 'rules.html', context)
    else:
        return render(request, 'rules.html', {})


def secret(request):
    return render(request, 'secret.html', {})

@login_required()
@group_required('student', 'staff')
def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data['query']
        print(query)
        obj = Book.objects.filter(name__icontains=query)
        lis = []
        for i in obj:
            lis.append({
                'name': i.name,
                'isbn': i.isbn,
                'copies': i.copies,
                'edition': i.edition,
                'author': i.author,
                'available_on': i.ret_date,
            })
        print(lis)
        return render(request, "search.html", {'list': lis})
    return render(request, 'search.html', {'form': form})

@login_required()
@group_required('student', 'staff')
def contact(request):
    return render(request, 'contact_us.html', {})


def home(request):
    return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'you have successully logged out')
    return redirect('login')

@login_required()
@group_required('staff')
def staff_dashboard(request, id):
    user = Users.objects.get(id=id)
    context = {
        'user': user,
    }
    return render(request, 'staff_dash.html', context)

@login_required()
@group_required('student', 'staff')
def files(request):
    obj = File.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'title': i.title,
            'description': i.description,
            'file': i.file,
            'date': i.date_uploaded,
        })
    print(lis)
    return render(request, "files.html", {'list': lis})

@login_required()
@group_required('staff')
def files_delete(request, id):
    try:
        obj = File.objects.filter(user_num=id)
        obj.delete()
    except:
        messages.error(request, 'You do not have permission to delete this file')
        return redirect('files')
    return redirect('files')


@login_required()
@group_required('staff')
def staff_files(request, id):
    if request.method == 'POST':
            file = request.FILES['document']
            title = request.POST.get('title')
            description = request.POST.get('desp')
            print(title, description, file)
            fs = FileSystemStorage()
            name = fs.save(file.name, file)
            url = fs.url(name)
            user = Users.objects.get(id=id)
            new_file = File(file=url, title=title, description=description, user=user, user_num=id)
            new_file.save()
            messages.success(request, 'File uploaded successfully')
            return redirect('staff_files', id=id)
    obj = File.objects.filter(user_num=id)
    user = Users.objects.get(id=id)
    lis = []
    for i in obj:
        lis.append({
            'id': id,
            'from': user.name,
            'title': i.title,
            'description': i.description,
            'file': i.file,
        })
    print(lis)
    return render(request, "staff_files.html", {'list': lis, 'id': id})

@login_required()
@permission_required('librarian')
def lib_files(request):
    obj = File.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'title': i.title,
            'description': i.description,
            'file': i.file,
            'date': i.date_uploaded,
        })
    print(lis)
    return render(request, "lib_files.html", {'list': lis})

@login_required()
@permission_required('librarian')
def lib_files_delete(request, id):
    obj = File.objects.get(id=id)
    obj.delete()
    return redirect('lib_files')
    