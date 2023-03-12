from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as DjangoUserChangeForm,
    UserCreationForm as DjangoUserCreationForm,
)

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class UserInfoForm(forms.ModelForm):
    def has_changed(self):
        """Prevents forms with defaults from being recognized as empty/unchanged.

        When forms are used as inline children and need to be created with null/blank
        defaults when saving the parent model.
        """
        return not self.instance.pk or super().has_changed()
