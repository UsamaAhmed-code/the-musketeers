from dataclasses import fields
from django import forms
from .models import Document


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title' , 'content' ]
 