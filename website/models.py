from django.db import models
# dfrom django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.IntegerField(default=0)
    issue = models.BooleanField(default=False)

    def __str__(self):
        return f"Book: {self.name} ; ISBN: {self.isbn} ; Issued: {self.issue})"


class Student(models.Model):
    name = models.CharField(max_length=20, default='NAME')
    usn = models.IntegerField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    fine = models.IntegerField(default=0)
    issued = models.OneToOneField(Book, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"USN: {self.usn} ; User mail: {self.email} ;  fine: {self.fine} ; Book in Issue: {self.issued} ;  Password: {self.password}"
