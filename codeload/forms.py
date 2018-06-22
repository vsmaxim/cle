from django import forms
from .models import Solutions, Task


class FileUploadForm(forms.Form):
    file = forms.FileField()