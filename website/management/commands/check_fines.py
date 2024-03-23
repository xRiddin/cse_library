from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from website.models import Book, Users

class Command(BaseCommand):
    help = 'Check overdue books and apply fines'

    def handle(self, *args, **kwargs):
        # Get all books that have been issued
        issued_books = Book.objects.filter(status='issued')

        for book in issued_books:
            # Check if the return date has passed
            if book.ret_date < timezone.now().date():
                # Calculate the number of days overdue
                days_overdue = (timezone.now().date() - book.ret_date).days

                # Calculate the fine amount (2 per day)
                fine_amount = 2

                # Add the fine to the user's existing fine
                user = book.issue_to
                user.fine += fine_amount
                user.save()

                # Send an email to the user
                send_mail(
                    'Library fine notice',
                    f'You have a fine of {user.fine} for overdue books.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

        self.stdout.write(self.style.SUCCESS('Successfully checked for overdue books and applied fines.'))