from django import forms
from .models import Student, Book


class Login(forms.Form):
    email = forms.CharField(label="email", max_length=20)
    password = forms.CharField(label='password', max_length=20)


class CreateUser(forms.ModelForm):
    email = forms.CharField(widget=forms.Textarea(attrs={
        'class': "email-field",
        'rows': '1'
    }))
    password = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'password-field',
        'rows': 1
    }))

    class Meta:
        model = Student
        fields = [
            'usn',
            'email',
            'password',
            'fine',
            'issued'
        ]


class UploadBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'isbn',
            'issue',
        ]

"""
class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['issued'].widget = forms.TextInput(attrs={'class': 'vTextField'})
"""