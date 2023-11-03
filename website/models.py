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
    usn = models.CharField(max_length=20, default=0)

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
            Book.objects.filter(usn=self.usn).update(issue=False)
            Book.objects.filter(usn=self.usn).update(usn=0)
            self.issued.issue = True
            self.issued.usn = self.usn
            self.issued.save()
        else:
            Book.objects.filter(usn=self.usn).update(issue=False)
            Book.objects.filter(usn=self.usn).update(usn=0)
        super().save(*args, **kwargs)
