from tkinter import N
from webbrowser import get
from django.db import models
from django.utils import timesince
from datetime import datetime, timedelta, date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def get_expiry():
    return datetime.today() + timedelta(days=15)


def get_expiry_staff():
    return datetime.today() + timedelta(days=60)


def fine(ret_date):
    if not ret_date:
        return 0
    ret_date = ret_date.date()
    today = datetime.today().date()
    if ret_date < today:
        days = (today - ret_date).days
        fine = days * 10
        return fine
    return 0

def fine_staff(ret_date):
    if not ret_date:
        return 0
    ret_date = ret_date.date() if isinstance(ret_date, datetime) else ret_date
    today = date.today()
    if ret_date < today:
        days = (today - ret_date).days
        fine = days * 10
        return fine
    return 0

class Book(models.Model):
    # issue_to = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    isbn = models.IntegerField(default=None)
    author = models.CharField(max_length=200, default=None)
    copies = models.IntegerField(default=0)
    category = models.CharField(max_length=200, default=None, blank=True)
    available = models.BooleanField(default=True)
    issue_date = models.DateField(default=None, null=True, blank=True)
    ret_date = models.DateField(default=None, null=True, blank=True)
    issue_to = models.CharField(max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return f"Book: {self.name} || ISBN: {self.isbn} || Author: {self.author} || copies: {self.copies} || category: {self.category} || ID: {self.issue_to} || From: {self.issue_date} || Till: {self.ret_date})"


class Magazine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default=None, blank=True)    
    author = models.CharField(max_length=200, default=None)
    isbn = models.IntegerField(default=None)
    copies = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    issue_date = models.DateField(default=None, null=True, blank=True)
    ret_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return f"Magazine: {self.name} ; ISBN: {self.isbn} ; Author: {self.author} ; Available: {self.available}; copies: {self.copies} ; From: {self.issue_date}; Till: {self.ret_date})"


class Reference(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default=None, blank=True, null=True)
    author = models.CharField(max_length=200, default=None, blank=True, null=True)
    copies = models.IntegerField(default=0)
    isbn = models.IntegerField(default=None)
    available = models.BooleanField(default=True)
    issue_date = models.DateField(default=None, null=True, blank=True)
    ret_date = models.DateField(default=None, null=True, blank=True)
    issue_to = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Book: {self.name} ; ISBN: {self.isbn} ; Author: {self.author} ; category: {self.category} Issued: {self.available}; copies: {self.copies}; ID: {self.issue_to} ; From: {self.issue_date}; Till: {self.ret_date})"


class Student(models.Model):
    name = models.CharField(max_length=20, default=None)
    usn = models.CharField(max_length=7)
    phone = models.IntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    fine = models.IntegerField(default=0, blank=True)
    issued_Book = models.ManyToManyField(Book, blank=True, null=True, related_name='student_books')
    # issued_Reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE, related_name='student_references')
    """
    @property
    def fine():
       ...
    """
    def __str__(self):
        return f"Name: {self.name} ; USN: {self.usn} ; User mail: {self.email} ;  fine: {self.fine} ; Book in Issue: {self.issued_Book} ;"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the staff instance first
        
    
        
        """
        if self.issued_Reference is None:
            reference = Reference.objects.get(name='sample')
            self.issued_Reference = reference
        """
        if self.issued_Book:
            for book in self.issued_Book.all():
                if book is None:
                    b = Book.objects.get(name='sample')
                    book = b
                if book.issue_date:
                    book.issue_date = datetime.today()
                    book.ret_date = get_expiry()
                    book.save()
                    super().save(*args, **kwargs)
                    self.fine = fine(book.ret_date)
                super().save(*args, **kwargs)

            
        else:
            print("No copies of the book are available.")
        """
        if self.issued_Reference:
            self.issued_Reference.issue_date = datetime.today()
            print('issue date', self.issued_Reference.issue_date)
            self.issued_Reference.ret_date = get_expiry()
            print('ret date', self.issued_Reference.ret_date)
            super().save(*args, **kwargs)
            self.fine = fine(self.issued_Reference.ret_date)
            print('fine:', self.fine)

        else:
            print("No copies of the reference are available.")
                    # raise ValidationError("No copies of the reference are available.")
        """


class Staff(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.IntegerField(default=0)
    password = models.IntegerField()
    fine = models.IntegerField(default=0)
    issued_book = models.ManyToManyField(Book, blank=True, null=True, related_name='staff_books')
    # issued_reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE, related_name='staff_references')
    staff_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Name: {self.name} ; Staff ID: {self.staff_id} ; Email: {self.email} ; Phone: {self.phone} ; Fine: {self.fine} ; issued book: {self.issued_book} ;"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
       
        """
        if self.issued_reference is None:
            reference = Reference.objects.get(name='sample')
            self.issued_reference = reference
        """
        if self.issued_book:
            for book in self.issued_book.all():
                if book is None:
                    b = Book.objects.get(name='sample')
                    book = b
                if book.issue_date:
                    book.issue_date = datetime.today()
                    book.ret_date = get_expiry_staff()
                    book.save()
                    super().save(*args, **kwargs)
                    self.fine = fine_staff(book.ret_date)
                super().save(*args, **kwargs)
            
        else:
            raise ValidationError("No copies of the book are available.")
        """
        if self.issued_reference:
            if self.issued_reference:
                self.issued_reference.issue_date = datetime.today()
                self.issued_reference.ret_date = get_expiry()       
                super().save(*args, **kwargs)
                self.fine = fine(self.issued_reference.ret_date)
            else:
                raise ValidationError("No copies of the reference are available.")
        else:
            raise ValidationError("No copies of the reference are available.")
        """
"""
class Issue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    issue_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('student', 'book'), ('staff', 'book'))
    
    def __str__(self):
        return f"Student: {self.student} ; Staff: {self.staff} ; Book: {self.book} ; Issue Date: {self.issue_date} ; Expiry Date: {self.expiry_date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.student:
            if self.student.issued_Book.count() > 3:
                raise ValidationError("Maximum number of books issued.")
            else:
                self.student.issued_Book.add(self.book)
                self.book.issue_to = str(self.student.usn)
                self.issue_date = self.issue_date
                self.book.issue_date = self.issue_date
                if self.expiry_date:
                    self.book.ret_date = self.expiry_date
                else:
                    self.book.ret_date = get_expiry()
                self.student.save()
                self.book.save()
        elif self.staff:
            if self.staff.issued_book.count() > 5:
                raise ValidationError("Maximum number of books issued.")
            else:
                self.staff.issued_book.add(self.book)
                self.book.issue_date = self.issue_date
                if self.expiry_date:
                    self.book.ret_date = self.expiry_date
                else:
                    self.book.ret_date = get_expiry()                
                self.book.save()
                self.staff.save()

        super().save(*args, **kwargs)


class Return(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    issue_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('student', 'book'), ('staff', 'book'))
    

    def __str__(self):
        return f"Student: {self.student} ; Staff: {self.staff} ; Book: {self.book} ; Issue Date: {self.issue_date} ; Expiry Date: {self.expiry_date}; fine: {self.student.fine}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.student:
            if self.student.issued_Book.count() > 3:
                raise ValidationError("Maximum number of books issued.")
            else:
                self.student.issued_Book.remove(self.book)
                self.student.fine = fine(self.book.issue_date)
                self.book.issue_to = None
                self.book.issue_date = None
                self.student.save()
                self.book.save()
                self.expiry_date = None
        elif self.staff:
            if self.staff.issued_book.count() > 5:
                raise ValidationError("Maximum number of books issued.")
            else:
                self.staff.issued_book.remove(self.book)
                self.staff.fine = fine_staff(self.book.issue_date)
                self.book.issue_to = None
                self.book.issue_date = None
                self.issue_date = None
                self.staff.save()
                self.book.save()
                self.expiry_date = None
        super().save(*args, **kwargs)    

"""
@receiver(post_save, sender=Book)
def post_save_book(sender, instance, **kwargs):
    # Perform your action here
    print(f"A book was saved: {instance.name}")
