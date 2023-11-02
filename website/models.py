from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
# dfrom django.contrib.auth.models import User


def get_expiry():
    return datetime.today() + timedelta(days=15)


class Book(models.Model):
    # issue_to = models.OneToOneField('Student', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    isbn = models.IntegerField(default=0)
    issue = models.BooleanField(default=False)
    issue_date = models.DateField(default=timezone.now)
    ret_date = models.DateField(default=get_expiry)

    def __str__(self):
        return f"Book: {self.name} ; ISBN: {self.isbn} ; Issued: {self.issue}; From: {self.issue_date}; Till: {self.ret_date})"


class Student(models.Model):
    name = models.CharField(max_length=20, default='NAME')
    usn = models.IntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    fine = models.IntegerField(default=0)
    issue = models.BooleanField(default=False)
    issued = models.OneToOneField(Book, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name} ; USN: {self.usn} ; User mail: {self.email} ;  fine: {self.fine} ; Book in Issue: {self.issued} ;"

    def save(self, *args, **kwargs):
        if self.issued:
            self.issued.issue = True
            self.issued.save()
        else:
            if self.issued_id:
                previous_book = Book.objects.get(id=self.issued_id)
                if previous_book.issue:
                    previous_book.issue = False
                    previous_book.save()
        super().save(*args, **kwargs)

        if not self.issued:
            Book.objects.filter(issue=True).update(issue=False)
