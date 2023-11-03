from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User


def get_expiry():
    return datetime.today() + timedelta(days=15)


class Book(models.Model):
    # issue_to = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    isbn = models.IntegerField(default=0)
    author = models.CharField(max_length=200, default='EWIT')
    issue = models.BooleanField(default=False)
    issue_date = models.DateField(default=timezone.now)
    ret_date = models.DateField(default=get_expiry)

    def __str__(self):
        return f"Book: {self.name} ; ISBN: {self.isbn} ; Author: {self.author} ; Issued: {self.issue}; From: {self.issue_date}; Till: {self.ret_date})"


class Student(models.Model):
    name = models.CharField(max_length=20, default='NAME')
    usn = models.CharField(max_length=7)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    fine = models.IntegerField(default=0)
    issue = models.BooleanField(default=False)
    issued = models.OneToOneField(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='issued_by')

    """
    @property
    def fine():
       ...
    """
    def __str__(self):
        return f"Name: {self.name} ; USN: {self.usn} ; User mail: {self.email} ;  fine: {self.fine} ; Book in Issue: {self.issued} ;"

    def save(self, *args, **kwargs):
        if self.issued:
            self.issued.issue = True
            self.issued.save()
        else:
            if self.issued_id:
                previous_book = Book.objects.get(id=self.issued_id)
                print(previous_book)
                if previous_book.issue:
                    previous_book.issue = False
                    previous_book.save()
        super().save(*args, **kwargs)

        s = Student.objects.all()
        b = Book.objects.all()
        for i in b:
            for j in s:
                if j.issued is not None:
                    if j.issued.isbn == i.isbn:
                        print(j.issued.isbn, i.isbn)
                        i.issue = True
                        i.save()
                    else:
                        i.issue = False
                        i.save()
                else:
                    i.issue = False
                    i.save()

        super().save(*args, **kwargs)
        """
        if not self.issued:
            b = Book.objects.all()
            for i in b:
                print(i)
                if i.issue:
                    i.issue = True
                else:
                    i.issue = False

            # Book.objects.filter(issue=True).update(issue=False)
        """