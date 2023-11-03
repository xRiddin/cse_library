from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Book, Student
from django.http import HttpResponse
# from .forms import Login
from .forms import CreateUser
from datetime import date

"""
def login_user(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        password = request.POST['password']
        user = authenticate(request, username=usn, password=password)
        if user is not None:
            print("success")
            login(request, user)
            u = get_object_or_404(Student, pk=usn)
            context = {
                'usn': u.usn,
                'email': u.email,
                'fine': u.fine,
                'issued': u.issued,
            }
            return render(request, 'user.html', context)
        else:
            print("fail")
            messages.error(request, 'Invalid email or password')
    else:
        form = Login()

    return render(request, 'login.html', {})
"""


def login_user(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        password = request.POST['password']
        try:
            u = get_object_or_404(Student, usn=usn, password=password)
            fine = 0
            if u.issued:
                if u.issued.issue:
                    days = (date.today() - u.issued.issue_date)
                    print(date.today())
                    d = days.days
                    if d > 15:
                        day = d - 15
                        fine = day * 10
                        u.fine = fine
            context = {
                'usn': u.usn,
                'email': u.email,
                'fine': u.fine,
                'issued': u.issued,
            }
            messages.success(request, 'you have logged in...')
            return render(request, 'user.html', context)
        except Exception as e:
            print(e)
            messages.error(request, 'login failed...')
            return redirect('login_user')
    return render(request, 'login.html', {})


@login_required()
def data(request, usn_id):
    u = get_object_or_404(Student, usn=usn_id)
    context = {
        'usn': u.usn,
        'email': u.email,
        'fine': u.fine,
        'issued': u.issued,
    }

    messages.success(request, 'you have logged in...')
    return render(request, 'user.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'you have successully logged out')
    return redirect('login')


def books(request, name=None):
    obj = Book.objects.all()
    lis = []
    for i in obj:
        lis.append({
            'name': i.name,
            'isbn': i.isbn,
            'issue': i.issue
        })
    print(lis)
    return render(request, "book.html", {'list': lis})


@login_required()
def createuser(request):
    print(request.user)
    form = CreateUser(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': form

    }
    return render(request, 'createuser.html', context)


def index(request, id):
    return HttpResponse("<h1>%s</h1>" % id)


"""em = Book(name='Book Name', isbn=123456, issue=True)
            em.save()
            new_user = Stu(email=email, password=password, fine=1, issued=em)
            new_user.save()
            return redirect('data')"""
