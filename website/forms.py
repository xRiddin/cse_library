from django import forms
from .models import Student, Book, Magazine, Staff, Reference


class Login(forms.Form):
    email = forms.CharField(label="email", max_length=20)
    password = forms.CharField(label='password', max_length=20)


class SearchForm(forms.Form):
    query = forms.CharField()


class BookForm(forms.ModelForm):
    name = forms.CharField(label='Book Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter book name'}))
    isbn = forms.CharField(label='ISBN', max_length=13, widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN'}))
    author = forms.CharField(label='Author', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter author name'}))
    copies = forms.IntegerField(label='Copies', widget=forms.NumberInput(attrs={'min': '1'}))
    available = forms.BooleanField(label='Available', required=False)
    
    class Meta:
        model = Book
        fields = ['name', 'isbn', 'author', 'copies', 'available']


class MagForm(forms.ModelForm):
    name = forms.CharField(label='Magazine Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter magazine name'}))
    isbn = forms.CharField(label='ISBN', max_length=13, widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN'}))
    author = forms.CharField(label='Author', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter author name'}))
    copies = forms.IntegerField(label='Copies', widget=forms.NumberInput(attrs={'min': '1'}))
    available = forms.BooleanField(label='Available', required=False)
    
    class Meta:
        model = Magazine
        fields = ['name', 'isbn', 'author', 'copies', 'available']

class StaffForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))
    staff_id = forms.CharField(label='Staff ID', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter staff ID'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    phone = forms.IntegerField(label='Phone', widget=forms.NumberInput(attrs={'min': '1'}))
    fine = forms.IntegerField(label='Fine', widget=forms.NumberInput(attrs={'min': '0'}))
    issued_book = forms.IntegerField(label='Issued Books', widget=forms.NumberInput(attrs={'min': '0'}))
    issued_magazine = forms.IntegerField(label='Issued Magazines', widget=forms.NumberInput(attrs={'min': '0'}))
    
    class Meta:
        model = Staff
        fields = ['name', 'staff_id', 'email', 'phone', 'fine', 'issued_book', 'issued_magazine']


class StudentForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))
    usn = forms.CharField(label='USN', max_length=7, widget=forms.TextInput(attrs={'placeholder': 'Enter USN'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    phone = forms.IntegerField(label='Phone', widget=forms.NumberInput(attrs={'min': '1'}))
    fine = forms.IntegerField(label='Fine', widget=forms.NumberInput(attrs={'min': '0'}))
    issued_book = forms.IntegerField(label='Issued Books', widget=forms.NumberInput(attrs={'min': '0'}))
    issued_magazine = forms.IntegerField(label='Issued Magazines', widget=forms.NumberInput(attrs={'min': '0'}))
    
    class Meta:
        model = Student
        fields = ['name', 'usn', 'email', 'phone', 'fine', 'issued_book', 'issued_magazine']


class ReferenceForm(forms.ModelForm):
    name = forms.CharField(label='Reference Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter reference name'}))
    category = forms.CharField(label='Category', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter category'}))
    isbn = forms.CharField(label='ISBN', max_length=13, widget=forms.TextInput(attrs={'placeholder': 'Enter ISBN'}))
    author = forms.CharField(label='Author', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter author name'}))
    copies = forms.IntegerField(label='Copies', widget=forms.NumberInput(attrs={'min': '1'}))
    available = forms.BooleanField(label='Available', required=False)
    
    class Meta:
        model = Reference
        fields = ['name', 'category', 'isbn', 'author', 'copies', 'available']


class addStudent(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={
        'class': "name-field",
        'rows': '1'
    }))
    usn = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'usn-field',
        'rows': 1
    }))

    email = forms.CharField(widget=forms.Textarea(attrs={
        'class': "email-field",
        'rows': '1'
    }))
    password = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'password-field',
        'rows': 1
    }))
    phone = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'phone-field',
        'rows': 1
    }))

    class Meta:
        model = Student
        fields = [
            'name',
            'usn',
            'email',
            'password',
            'phone'
        ]


class addBook(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
    }))
    isbn = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    author = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
    }))
    copies = forms.CharField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    category = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Book
        fields = [
            'name',
            'isbn',
            'author',
            'category',
            'copies',
            
            
        ]


class addMagazine(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={
        'class': "name-field",
        'rows': '1'
    }))
    isbn = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'isbn-field',
        'rows': 1
    }))
    author = forms.CharField(widget=forms.Textarea(attrs={
        'class': "author-field",
        'rows': '1'
    }))
    copies = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'copies-field',
        'rows': 1
    }))
    
    category = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'category-field',
        'rows': 1
    }))

    class Meta:
        model = Magazine
        fields = [
            'name',
            'isbn',
            'author',
            'copies',
            'category',
            'available',
        ]


class addStaff(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={
        'class': "name-field",
        'rows': '1'
    }))
    staff_id = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'staff_id-field',
        'rows': 1
    }))
    email = forms.CharField(widget=forms.Textarea(attrs={
        'class': "email-field",
        'rows': '1'
    }))
    password = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'password-field',
        'rows': 1
    }))
    phone = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'phone-field',
        'rows': 1
    }))

    class Meta:
        model = Staff
        fields = [
            'name',
            'staff_id',
            'email',
            'phone',
            'password',
        ]


class addReference(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={
        'class': "name-field",
        'rows': '1'
    }))
    isbn = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'isbn-field',
        'rows': 1
    }))
    author = forms.CharField(widget=forms.Textarea(attrs={
        'class': "author-field",
        'rows': '1'
    }))
    copies = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'copies-field',
        'rows': 1
    }))
    available = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'available-field',
        'rows': 1
    }))
    category = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'category-field',
        'rows': 1
    }))

    class Meta:
        model = Reference
        fields = [
            'name',
            'isbn',
            'author',
            'copies',
            'category',
            'available',
        ]
