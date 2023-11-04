from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Book, Student
from django.http import HttpResponse
# from .forms import Login
from .forms import CreateUser, SearchForm
from datetime import date


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
                'name': u.name,
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
def data(request, usn_id,):
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
            'issue': i.issue,
            'author': i.author,
            'available_on': i.ret_date,
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
                'issue': i.issue,
                'author': i.author,
                'available_on': i.ret_date,
            })
        print(lis)
        return render(request, "book.html", {'list': lis})
    return render(request, 'search.html', {'form': form})


def contact(request):
    return render(request, 'contact_us.html', {})