from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email harus diisi')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    role_choices = [
    ('1', 'Admin'),
    ('2', 'Mentor'),
    ('3', 'Mentee'),
    ]
    role = models.CharField(max_length=1, choices=role_choices, default='3')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username or self.email.split('@')[0]
    
    def get_role_display(self):
        return dict(User.role_choices)[self.role]
    
    def get_bio(self):
        return self.bio
    
class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verification_status = models.BooleanField(default=False)
    verification_document = models.CharField(max_length=255)
    # classes_taught = models.ManyToManyField('Class', related_name='mentors') TODO: uncomment this when Class model is created

class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # enrolled_classes = models.ManyToManyField('Class', related_name='mentees') TODO: uncomment this when Class model is created