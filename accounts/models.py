from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
# local


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, password=password, **kwargs)
        user.staff = True
        user.superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, default="default@default.com")
    first_name = models.CharField(max_length=40, default="default_first", blank=True)
    last_name = models.CharField(max_length=150, default="default_second", blank=True)
    phone_number = models.CharField(max_length=12, default="+91 12345679", blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)

    NOT_EVALUATED = 'NE'
    INTERVIEW_SET = 'IS'
    INTERVIEW_CONFIRMED = 'IC'
    INTERVIEWED = 'ID'
    ACCEPTED = 'AC'

    STATUS_CHOISES = (
        (NOT_EVALUATED, 'Not evaluated'),
        (INTERVIEW_SET, 'Interview set'),
        (INTERVIEW_CONFIRMED, 'Interview confirmed'),
        (INTERVIEWED, 'Interviewed'),
        (ACCEPTED, 'Accepted'),
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOISES,
        default=NOT_EVALUATED,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        if self.email == None:
            return 'error'
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name
        return "Error"

    def get_short_name(self):
        if self.first_name == None:
            return 'error'
        return self.first_name

    def get_status(self):
        if self.status == None:
            return 'error'
        return self.status

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
        print("sent")