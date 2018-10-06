from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if os.environ['RDS_DB_NAME']:
            email = os.environ['DJANGO_ADMIN_EMAIL']
            pw = os.environ['DJANGO_ADMIN_PASSWORD']
        else:
            email = "admin@admin.com"
            pw = "admin"
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=pw)
            print("Superuser created: email: {}, password: {}".format(email, pw))
