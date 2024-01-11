from django.contrib.auth import forms
from core import models

class LoginForm(forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-3',
                'autocomplete': 'off',
            })

    class Meta:
        model = models.User
        fields = ['username', 'password']