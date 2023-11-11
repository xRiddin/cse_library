from django.contrib import admin
from .models import Student, Book, Staff, Reference, Magazine
# from .forms import BookAdminForm


class StudAdmin(admin.ModelAdmin):

    def issued_Books(self, obj):
        return ", ".join([str(book) for book in obj.issued_Book.all()])

    # def issued_References(self, obj):
     #   return ", ".join([str(magazine) for magazine in obj.issued_Reference.all()])
    search_fields = ('usn', 'email', 'name', 'issued__name')
    list_display = ('name', 'usn', 'email', 'issued_Books', 'fine')
    raw_id_fields = ('issued_Book', )
    change_form_template = 'admin/website/Student/change_form.html'
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'issued_Book':
            kwargs['queryset'] = Book.objects.filter(available=True)
            # kwargs['to_field_name'] = 'name'
        #if db_field.name == 'issued_Reference':
         #   kwargs['queryset'] = Book.objects.filter(available=True)
            # kwargs['to_field_name'] = 'name'
        return super().formfield_for_manytomany(db_field, request, **kwargs)



class BookAdmin(admin.ModelAdmin):
    search_fields = ('name', 'isbn',)
    list_display = ('name',
                    'isbn',
                    'copies',
                    'author',
                    'available',

                    # 'issue_to',
                    # 'issue_date',
                    # 'ret_date'
                    )
    """
    raw_id_fields = ('issue_to',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'issue_to':
            kwargs['queryset'] = Student.objects.filter(issue=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """
    # form = BookAdminForm


class StaffAdmin(admin.ModelAdmin):
    def issued_books(self, obj):
        return ", ".join([str(book) for book in obj.issued_book.all()])

    #def issued_references(self, obj):
    #    return ", ".join([str(magazine) for magazine in obj.issued_reference.all()])

    search_fields = ('name', 'email', 'phone', 'staff_id')
    list_display = ('name', 'email', 'phone', 'staff_id', 'issued_books', 'fine')
    raw_id_fields = ('issued_book',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'issued_book':
            kwargs['queryset'] = Book.objects.filter(available=True)
            # kwargs['to_field_name'] = 'name'
        #if db_field.name == 'issued_reference':
         #   kwargs['queryset'] = Book.objects.filter(available=True)
            # kwargs['to_field_name'] = 'name'
        return super().formfield_for_manytomany(db_field, request, **kwargs)


#class ReferenceAdmin(admin.ModelAdmin):
#    search_fields = ('name', 'author', 'isbn')
#    list_display = ('name', 'isbn', 'copies', 'author', 'available', 'issue_to', )


# Register your models here.
admin.site.register(Student, StudAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reference)
admin.site.register(Magazine)
admin.site.register(Staff, StaffAdmin)


