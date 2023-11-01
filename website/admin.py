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
                    'issue'
                    )
    # form = BookAdminForm


# Register your models here.
admin.site.register(Student, StudAdmin)
admin.site.register(Book, BookAdmin)



