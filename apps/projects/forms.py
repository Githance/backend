from django import forms

from .models import Project


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            "intro": forms.Textarea,
            "description": forms.Textarea,
        }
        fields = ("intro",)
