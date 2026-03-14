from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from utils.models import UUIDModel

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email harus diisi'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser harus memiliki is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser harus memiliki is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
    

class CoreUser(AbstractUser, UUIDModel):
    username = None 
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(upload_to='assets/user/images', blank=True, null=True)
    date_joined = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []        

    objects = CustomUserManager()

    class Meta:
        db_table = 'core_user' 
        verbose_name = _('Core User')

    def __str__(self):
        return self.email


class CoreStudent(models.Model):
    user = models.OneToOneField(
        CoreUser, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        db_column='user_id' 
    )
    nis = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    rombel = models.CharField(max_length=100)
    rayon = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_student'
        verbose_name = "Core Student"

    def __str__(self):
        return f"Student: {self.name} ({self.nis})"


class CoreAdmin(models.Model):
    user = models.OneToOneField(
        CoreUser, 
        on_delete=models.CASCADE, 
        related_name='admin_profile',
        db_column='user_id'
    )
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'core_admin'
        verbose_name = "Core Admin"

    def __str__(self):
        return f"Admin: {self.name}"