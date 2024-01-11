from django.contrib.auth import forms
from core import models

class UserCreationForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-1',
                'autocomplete': 'off',
            })

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UserChangeForm(forms.UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields:
            self.fields[name].help_text = None
            self.fields[name].widget.attrs.update({
                'class': 'form-control mb-1',
                'autocomplete': 'off',
            })

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username']