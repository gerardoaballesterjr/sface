from django import forms
from core import models

class SeminarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-1',
                'autocomplete': 'off',
            })

    class Meta:
        model = models.Seminar
        fields = ['name', 'description']