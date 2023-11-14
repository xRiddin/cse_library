import email
from email import message
from multiprocessing import context
from turtle import st
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Book, Student, Magazine, Staff, Reference
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
# from .forms import Login
from .forms import SearchForm, addStudent, addBook, BookForm, MagForm, StaffForm, StudentForm, addMagazine, addReference, addStaff, ReferenceForm
from datetime import date, datetime, timedelta
import smtplib
import ssl
from email.message import EmailMessage



def login_user(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        password = request.POST['password']
        if authenticate(request, username=usn, password=password):
            login(request, authenticate(request, username=usn, password=password))
            messages.success(request, 'you have logged in...')
            return redirect('librarian')
        try:
            u = get_object_or_404(Student, usn=usn, password=password)
            context = {
                'name': u.name,
                'usn': u.usn,
                'email': u.email,
                'fine': u.fine,
                'issued': u.issued_Book,
            }
            messages.success(request, 'you have logged in...')
            return render(request, 'user.html', context)
        except Exception as e:
            print(e)
            messages.error(request, 'login failed...')
            return redirect('login_user')
    return render(request, 'login.html', {})


@login_required()
def data(request, usn_id,):
    u = get_object_or_404(Student, usn=usn_id)
    context = {
        'usn': u.usn,
        'email': u.email,
        'fine': u.fine,
        'issued': u.issued_Book,
    }
    messages.success(request, 'you have logged in...')
    return render(request, 'user.html', context)


@login_required()
def librarian(request):
    return render(request, 'librarian.html', {})


@login_required()
def lib_book(request):
    obj = Book.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'name': i.name,
            'isbn': i.isbn,
            'available': i.available,
            'author': i.author,
            'copies': i.copies,
            'issue_date': i.issue_date,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "lib_book.html", {'list': lis})


@login_required()
def lib_mag(request):
    obj = Magazine.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'name': i.name,
            'isbn': i.isbn,
            'available': i.available,
            'author': i.author,
            'copies': i.copies,
            'issue_date': i.issue_date,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "lib_mag.html", {'list': lis})


@login_required()
def lib_staff(request):
    obj = Staff.objects.all()
    lis = []
    for i in obj:
        if i.issued_book.all():
            for book in i.issued_book.all():
                lis.append({
            'id': i.id,
            'name': i.name,
            'staff_id': i.staff_id,
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
                'staff_id': i.staff_id,
                'email': i.email,
                'phone': i.phone,
                'fine': i.fine,
                'issued_book': None,
            })
    print(lis)
    return render(request, "lib_staff.html", {'list': lis})


@login_required()
def lib_student(request):
    obj = Student.objects.all()
    lis = []
    for i in obj:
        if i.issued_Book.all():
            for book in i.issued_Book.all():
                lis.append({
                    'id': i.id,
                    'name': i.name,
                    'usn': i.usn,
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
                'usn': i.usn,
                'email': i.email,
                'phone': i.phone,
                'fine': i.fine,
                'issued_book': None,
                })

    print(lis)
    return render(request, "lib_student.html", {'list': lis})


@login_required()
def lib_reference(request):
    obj = Reference.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'id': i.id,
            'name': i.name,
            'isbn': i.isbn,
            'available': i.available,
            'author': i.author,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "lib_reference.html", {'list': lis})

@login_required()
def lib_auto(request):
    email_sender = 'write-email-here'
    email_password = 'write-password-here'
    students = Student.objects.all()
    for student in students:
        if student.fine > 0:
            email_receiver = str(student.email)

            subject = 'Fine repayment'
            body = """
                 please pay your fine of Rs. """+str(student.fine)+""" as soon as possible
                """
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
    staff = Staff.objects.all()
    for staff in staff:
        if staff.fine > 0:
            email_receiver = str(staff.email)

            subject = 'Fine repayment'
            body = """
                 please pay your fine of Rs. """+str(staff.fine)+""" as soon as possible
                """
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
    return HttpResponse('Email sent successfully')


@login_required()
def lib_issue(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        isbn = request.POST.get('isbn')
        ret = request.POST.get('return_date')

        print(id, isbn)
        book = Book.objects.filter(isbn=isbn).first()

        if 'cs' in id:
            student = Student.objects.filter(usn=id).first()
            if student is not None and student.issued_Book is not None:
                if Book.objects.filter(issue_to=student.usn, isbn=isbn).exists():
                    messages.error(request, 'This book is already issued to the student')
                    return redirect('lib_issue')
                if student and student.issued_Book.all().count() >= 3:
                    messages.error(request, 'You can issue only 2 books')
                    return redirect('lib_issue')
                if book and book.copies == 0:
                    messages.error(request, 'Book not available')
                    return redirect('lib_issue')
                if book:
                    if student.fine == 0:
                        student.issued_Book.add(book)
                        book.issue_date = datetime.today()
                    else:
                        messages.error(request, 'You have fine of Rs.'+str(student.fine))
                        return redirect('lib_issue') 
                    if ret:
                        book.ret_date = ret
                    else:
                        book.ret_date = date.today() + timedelta(days=60)
                    book.issue_to = str(student.usn)
                    student.save()
                    book.save()
                else:
                    messages.error(request, 'Invalid ID')
                    return redirect('lib_issue') 
            else:
                messages.error(request, 'Invalid ID')
                return redirect('lib_issue')            
        else:
            staff = Staff.objects.filter(staff_id=id).first()
            if staff:
                if staff.issued_book.filter(isbn=isbn).exists():
                    messages.error(request, 'This book is already issued to the staff')
                    return redirect('lib_issue')
                if staff and staff.issued_book.count() >= 5:
                    messages.error(request, 'You can issue only 5 books')
                    return redirect('lib_issue')
                if staff and book:
                    if staff.fine > 0:
                        messages.error(request, 'You have fine of Rs.'+str(staff.fine))
                        return redirect('lib_issue')
                    staff.issued_book.add(book)
                    if ret:
                        book.ret_date = ret
                    else:
                        book.ret_date = date.today() + timedelta(days=60)
                    book.issue_to = str(staff.staff_id)
                    staff.save()
                    book.save()
                else:
                    messages.error(request, 'Invalid ID')
                    return redirect('lib_issue')  
            
            
        if book and book.copies > 0:
            book.copies -= 1
            book.save()
        context = {
            'name': student.name if student else staff.name,
            'book': book.name,
            'issue_date': book.issue_date,
            'return_date': book.ret_date,
        }
        messages.success(request, 'Book issued successfully')
        return render(request, 'lib_issue.html', context)
    return render(request, 'lib_issue.html', {})


@login_required()
def lib_return(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        isbn = request.POST.get('isbn')
        print(id, isbn)
        book = Book.objects.filter(isbn=isbn).first()
        if 'cs' in id:
            student = Student.objects.filter(usn=id).first()
            if book and student and student.issued_Book.filter(isbn=isbn).exists():
                student.save()
                if student.fine > 0:
                    messages.error(request, 'You have fine of Rs.'+str(student.fine))
                    return redirect('lib_return')
                student.issued_Book.remove(book)
                book.issue_to = None
                book.issue_date = None
                book.ret_date = None
                student.save()
                book.save()
            else:
                messages.error(request, "Invalid, no book issued")
                return redirect('lib_return')

        else:
            staff = Staff.objects.filter(staff_id=id).first()
            if book and staff and staff.issued_book.filter(isbn=isbn).exists():
                staff.save()
                if staff.fine > 0:
                    messages.error(request, 'You have fine of Rs.'+str(staff.fine))
                    return redirect('lib_return')
                staff.issued_book.remove(book)
                book.issue_to = None
                book.issue_date = None
                book.ret_date = None
                staff.save()
                book.save()
            else:
                messages.error(request, "Invalid, no book issued")
                return redirect('lib_return')

        if book:
            book.copies += 1
            book.save()
            
            context = {
            'name': student.name if student else staff.name,
            'book': book.name,
            'issue_date': book.issue_date,
            'return_date': book.ret_date,
            'fine': student.fine if student else staff.fine,
            }
            messages.success(request, 'Book returned successfully')
            return render(request, 'lib_return.html', context)
        else:
            return messages.error(request, 'Book not returned')
    return render(request, 'lib_return.html', {})

@login_required()
def repay_due(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        amount = request.POST.get('amount')
        student = None
        if id and amount:
            if 'cs' in id:
                student = Student.objects.filter(usn=id).first()
                if student:
                    if student.fine > 0:
                        if student.fine > int(amount):
                            student.fine -= int(amount)
                            student.save()
                        elif student.fine == int(amount):
                            student.fine = 0
                            student.save()
                        else:
                            messages.error(request, 'Invalid amount')
                            return redirect('repay_due')
                    else:
                        messages.error(request, 'You have no fine')
                        return redirect('repay_due')
                else:
                    messages.error(request, 'Invalid ID')
                    return redirect('repay_due')
            else:
                staff = Staff.objects.filter(staff_id=id).first()
                if staff:
                    if staff.fine > 0:
                        if staff.fine > int(amount):
                            staff.fine -= int(amount)
                            staff.save()
                        elif staff.fine == int(amount):
                            staff.fine = 0
                            staff.save()
                        else:
                            messages.error(request, 'Invalid amount')
                            return redirect('repay_due')
                    else:
                        messages.error(request, 'You have no fine')
                        return redirect('repay_due')
                else:
                    messages.error(request, 'Invalid ID')
                    return redirect('repay_due')
            context = {
                'name': student.name if student else staff.name,
                'fine': student.fine if student else staff.fine,
            }
            messages.success(request, 'Fine paid successfully')
            return render(request, 'payment.html', context)
        else:
            messages.error(request, 'Invalid details')
            return redirect('repay_due')
    return render(request, 'payment.html', {})
                


@login_required()
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


@login_required()
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

@login_required()
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('lib_student')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})


@login_required()
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff edited successfully')
            return redirect('lib_staff')
        else:
            messages.error(request, 'Invalid details')
            return redirect('lib_staff')
    else:

        form = StaffForm(instance=staff)
    return render(request, 'edit_staff.html', {'form': form})

def books(request, name=None):
    obj = Book.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'available': i.available,
            'author': i.author,
            'available_on': i.ret_date,
        })
    print(lis)
    return render(request, "book.html", {'list': lis})


def reference(request):
    obj = Reference.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'available': i.available,
            'author': i.author,
        })
    print(lis)
    return render(request, "reference.html", {'list': lis})

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


@login_required()
def add_book(request):
    print(request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        isbn = request.POST.get('isbn')
        author = request.POST.get('author')
        copies = request.POST.get('copies')
        category = request.POST.get('category')
        if name and isbn and author and copies and category:
            if Book.objects.filter(isbn=isbn).exists():
                messages.error(request, 'Book already exists')
                return redirect('add_book')
            else:
                book = Book(name=name, isbn=isbn, author=author, copies=copies, category=category)
                book.save()
                messages.success(request, 'Book added successfully')
                return redirect('add_book')
        return render(request, 'add_book.html', {})
    else:
        return render(request, 'add_book.html', {})

@login_required()
def add_magazine(request):
    print(request.user)
    form = addMagazine(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, 'add_magazine.html', context)


@login_required()
def add_staff(request):
    if request.method == 'POST':
        print(request.user)
        name = request.POST.get('name')
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if name and staff_id and email and phone and password:
            if Staff.objects.filter(staff_id=staff_id).exists():
                messages.error(request, 'Staff already exists')
                return redirect('add_staff')
            else:
                staff = Staff(name=name, staff_id=staff_id, email=email, phone=phone, password=password)
                staff.save()
                messages.success(request, 'Staff added successfully')
                return redirect('add_staff')
        return render(request, 'add_staff.html', {})
    else:
        return render(request, 'add_staff.html', {})
    

@login_required()
def add_student(request):
    if request.method == 'POST':
        print(request.user)
        name = request.POST.get('name')
        usn = request.POST.get('usn')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if name and usn and email and phone and password:
            if Student.objects.filter(usn=usn).exists():
                messages.error(request, 'student already exists')
                return redirect('add_student')
            else:
                stu = Student(name=name, usn=usn, email=email, phone=phone, password=password)
                stu.save()
                messages.success(request, 'Student added successfully')
                return redirect('add_student')
        return render(request, 'add_staff.html', {})
    else:
        return render(request, 'add_student.html', {})

@login_required()
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



def rules(request, id=None):
    if id:
        t = get_object_or_404(Student, id=id)
        context = {
            'name': t.name,
        }
        return render(request, 'rules.html', context)
    else:
        return render(request, 'rules.html', {})


def secret(request):
    return render(request, 'secret.html', {})


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
                'available': i.available,
                'author': i.author,
                'available_on': i.ret_date,
            })
        print(lis)
        return render(request, "book.html", {'list': lis})
    return render(request, 'search.html', {'form': form})


def contact(request):
    return render(request, 'contact_us.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'you have successully logged out')
    return redirect('login')
