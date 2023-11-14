from django.urls import path
from . import views
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Other URL patterns
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('book/', views.books, name="books"),
    path("logout/", views.logout_user, name='logout_user'),
    path('data/<int:usn_id>/user', views.data, name='data'),
    path('createuser/', views.createuser, name='createuser'),
    path('rules/', views.rules, name='rules'),
    path('rules/<int:id>/', views.rules, name='rules'),
    path('secret/', views.secret, name='secret'),
    path('references/', views.reference, name='reference'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('librarian/books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('librarian/', views.librarian, name='librarian'),
    path('librarian/lib_book/', views.lib_book, name='lib_book'),
    path('librarian/lib_mag/', views.lib_mag, name='lib_mag'),
    path('librarian/lib_staff/', views.lib_staff, name='lib_staff'),
    path('librarian/lib_student/', views.lib_student, name='lib_student'),
    path('librarian/lib_issue/', views.lib_issue, name='lib_issue'),
    path('librarian/lib_return/', views.lib_return, name='lib_return'),
    path('librarian/lib_reference/', views.lib_reference, name='lib_reference'),
    #path('librarian/books/issue/<int:book_id>/', views.lib_issue, name='lib_issue'),
    #path('librarian/books/return/<int:book_id>/', views.lib_return, name='lib_return'),
    path('librarian/magazines/edit/<int:magazine_id>/', views.edit_magazine, name='edit_magazine'),
    path('librarian/staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('librarian/student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('librarian/reference/edit/<int:reference_id>/', views.edit_reference, name='edit_reference'),
    path('librarian/books/add/', views.add_book, name='add_book'),
    path('librarian/magazines/add/', views.add_magazine, name='add_magazine'),
    path('librarian/staff/add/', views.add_staff, name='add_staff'),
    path('librarian/student/add/', views.add_student, name='add_student'),
    path('librarian/reference/add/', views.add_reference, name='add_reference'),
    path('librarian/payments/', views.repay_due, name='repay_due'),
    path('librarian/lib_auto/', views.lib_auto, name='lib_auto'),
]
