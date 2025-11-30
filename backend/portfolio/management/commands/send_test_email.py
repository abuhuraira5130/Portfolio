from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email to verify SMTP configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str)

    def handle(self, *args, **options):
        recipient = options['recipient']
        send_mail(
            subject='SMTP Test',
            message='This is a SMTP test email from Django.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f'Test email sent to {recipient}'))