from django.contrib import admin
from .models import Student, Book
# from .forms import BookAdminForm


class StudAdmin(admin.ModelAdmin):
    search_fields = ('usn', 'email', 'name', 'issued__name')
    list_display = ('name', 'usn', 'email', 'issued', 'fine')
    raw_id_fields = ('issued',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'issued':
            kwargs['queryset'] = Book.objects.filter(issue=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class BookAdmin(admin.ModelAdmin):
    search_fields = ('name', 'isbn',)
    list_display = ('name',
                    'isbn',
                    'issue',
                    # 'issue_to',
                    'issue_date',
                    'ret_date'
                    )
    """
    raw_id_fields = ('issue_to',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'issue_to':
            kwargs['queryset'] = Student.objects.filter(issue=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """
    # form = BookAdminForm


# Register your models here.
admin.site.register(Student, StudAdmin)
admin.site.register(Book, BookAdmin)



