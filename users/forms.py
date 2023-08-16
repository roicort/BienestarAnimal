from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserEditForm(UserEditForm):
    username = forms.CharField(required=True, label=_("ID de usuario"))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(required=True, label=_("ID de usuario"))