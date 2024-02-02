from distutils.command import upload
from webbrowser import get
from django.db import models
from django.utils import timesince
from datetime import datetime, timedelta, date
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser, BaseUserManager


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
# todo: add history for transaction

class Book(models.Model):
    class Program(models.TextChoices):
        UG = 'UG'
        PG = 'PG'

    name = models.CharField(max_length=200)
    isbn = models.IntegerField(default=None)
    publisher = models.CharField(max_length=400, default=None)
    access_code = models.IntegerField(default=None, primary_key=True)
    course = models.CharField(max_length=10, choices=Program.choices, default=Program.UG)
    edition = models.IntegerField(default=None)
    author = models.CharField(max_length=200, default=None)
    status = models.CharField(max_length=200, default="available")
    # copies = models.IntegerField(default=0)
    category = models.CharField(max_length=200, default=None, blank=True)
    issue_date = models.DateField(default=None, null=True, blank=True)
    ret_date = models.DateField(default=None, null=True, blank=True)
    issue_to = models.ForeignKey("Users", on_delete=models.SET_NULL, null=True, blank=True, related_name='books', to_field='id_number')
    reference = models.BooleanField(default=False)
    purchase_date = models.DateField(default=None, blank=True, null=True)
    cost = models.IntegerField(default=None, blank=True, null=True)
    pub_year = models.IntegerField(default=None, blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        #print(f"accession code: {self.access_code}; Book: {self.name} || ISBN: {self.isbn} edition: {self.edition}|| Author: {self.author} || volumes: {self.copies.all()} || category: {self.category} || ID: {self.issue_to.id_number},{self.issue_to.name} || From: {self.issue_date} || Till: {self.ret_date})")
        return f"access code: {self.access_code} || Book: {self.name} || ISBN: {self.isbn} || From: {self.issue_date} || Till: {self.ret_date} || status: {self.status}"
    
    class Meta:
        permissions = [
            ('only_view_book', 'Only View Book'),
            ('edit_only_book', 'Edit Only Book'),
            ('add_only_book', 'Add Only Book'),
        ]


class Book_Copies(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    total_copies = models.IntegerField(default=0)
    issued_copies = models.IntegerField(default=0)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return f"Book: {self.book} || Total Copies: {self.total_copies} || Issued Copies: {self.issued_copies} || Available Copies: {self.available_copies}"


class TransactionLog(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField(default=0, null=True, blank=True)
    transaction_type = models.CharField(max_length=200)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} || Book: {self.book} || Transaction Type: {self.transaction_type} || Transaction Date: {self.transaction_date}"


class Magazine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default=None, blank=True)    
    author = models.CharField(max_length=200, default=None)
    isbn = models.IntegerField(default=None)
    edition = models.CharField(max_length=200, default=None)
    publisher = models.CharField(max_length=400, default=None, blank=True, null=True)
    access_code = models.IntegerField(default=0, primary_key=True)
    cost = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return f"Magazine: {self.name}; access_code: {self.access_code} ; ISBN: {self.isbn} ; Author: {self.author} ;edition : {self.edition}"

    class Meta:
        permissions = [
            
            ('only_view_magazine', 'Only View Magazine'),
            ('edit_only_magazine', 'Edit Only Magazine'),
            ('add_only_magazine', 'Add Only Magazine'),
        ]


class File(models.Model):
    file = models.FileField(upload_to='files/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='files')
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return f"File: {self.file} ; Title: {self.title} ; Description: {self.description} ; Staff: {self.user} ;"
    
    def save(self, *args, **kwargs):
        """
        if self.user.user_type != 2 or self.user.user_type != 1:
            raise ValueError("Only staff and librarian can upload files")
        super().save(*args, **kwargs)
        """
        if self.user:
            self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ('only_view', 'Only View'),
            ('add', 'Add'),
            ('delete', 'Delete'),
        ]       


class Holidays(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Date: {self.date} ; Name: {self.name} ;"


class Notification(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date_uploaded = models.DateTimeField(auto_now_add=True)
    file_notification = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()
    def save(self, *args, **kwargs):
        if self.file_notification:
            if self.file_notification.user.user_type != 2 or self.file_notification.user.user_type != 1:
                raise ValueError("Only staff and librarian can upload notifications")
            self.file_notification.user.save()
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        issued_books = extra_fields.pop('issued_book', None)
        if issued_books is not None:
            user.issued_book.set(issued_books)

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)
        extra_fields.setdefault('name', 'admin')
        extra_fields.setdefault('phone', '1234567890')
        extra_fields.setdefault('id_number', 'admin')
        extra_fields.setdefault('fine', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class Users(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'librarian'),
      (2, 'staff'),
      (3, 'student'),
      (4, 'library_staff')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    fine = models.IntegerField(default=0)
    issued_book = models.ManyToManyField(Book, blank=True, related_name='users_books')
    id_number = models.CharField(max_length=200, primary_key=True)
    objects = UserManager()
    history = HistoricalRecords()

    def __str__(self):
        return f"Name: {self.name} ; ID: {self.id_number} type: {self.user_type}; password: {self.password} ;Email: {self.email} ; Phone: {self.phone} ; Fine: {self.fine} ; issued book: {self.issued_book} ;"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
               
        if self.issued_book:
            for book in self.issued_book.all():
                if book is None:
                    b = Book.objects.get(name='sample')
                    book = b
            """
                if self.user_type == 3:
                    if book.issue_date:
                        book.issue_date = datetime.today()
                        book.ret_date = get_expiry()
                        book.save()
                        super().save(*args, **kwargs)
                        self.fine = fine(book.ret_date)
                if self.user_type == 2:
                    if book.issue_date:
                        book.issue_date = datetime.today()
                        book.ret_date = get_expiry_staff()
                        book.save()
                        super().save(*args, **kwargs)
                        self.fine = fine(book.ret_date)
                super().save(*args, **kwargs)
    """
    class Meta:
        permissions = [
            ("librarian", "Librarian"),
        ]



"""
class Student(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default=None)
    usn = models.CharField(max_length=7)
    phone = models.IntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    fine = models.IntegerField(default=0, blank=True)
    issued_Book = models.ManyToManyField(Book, blank=True, related_name='student_books')
    # issued_Reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE, related_name='student_references')
    
    def __str__(self):
        return f"Name: {self.name} ; USN: {self.usn} ; User mail: {self.email} ;  fine: {self.fine} ; Book in Issue: {self.issued_Book} ;"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the staff instance first
        
    
        
        
        if self.issued_Reference is None:
            reference = Reference.objects.get(name='sample')
            self.issued_Reference = reference
        
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
        
    class Meta:
        permissions = [
            ("librarian", "Librarian"),
        ]


class Staff(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.IntegerField(default=0)
    password = models.IntegerField()
    fine = models.IntegerField(default=0)
    issued_book = models.ManyToManyField(Book, blank=True, related_name='staff_books')
    # issued_reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.CASCADE, related_name='staff_references')
    staff_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Name: {self.name} ; Staff ID: {self.staff_id} ; Email: {self.email} ; Phone: {self.phone} ; Fine: {self.fine} ; issued book: {self.issued_book} ;"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
       
       
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
        

    class Meta:
        permissions = [
            ("librarian", "Librarian"),
        ]



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