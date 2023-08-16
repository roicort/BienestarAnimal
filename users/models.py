from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as OriginalGroup
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

# Create your models here.

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    # history = AuditlogHistoryField(pk_indexable=False)
    email = models.EmailField(unique=True)
    safe_delete = models.BooleanField(default=False)
    username = models.CharField(
        "username",
        max_length=150,
        primary_key=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    @property
    def nombre_completo(self):
        try:
            return self.perfilgeneral.nombre_completo
        except:
            return self.email

    def __str__(self):
        return self.nombre_completo

    @staticmethod
    @receiver(pre_delete, sender='users.User')
    def safe_delete_usuario(sender, instance, **kwargs):
        instance.safe_delete = True
        instance.save()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Group(OriginalGroup):
    class Meta:
        proxy = True
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


auditlog.register(User)
auditlog.register(Group)
