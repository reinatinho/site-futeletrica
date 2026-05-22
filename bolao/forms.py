from django import forms
from .models import Participante


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Usuário',
            'class': 'form-input',
            'autocomplete': 'username',
        })
    )
    pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'PIN (4 dígitos)',
            'class': 'form-input',
            'inputmode': 'numeric',
            'pattern': '[0-9]{4}',
            'maxlength': '4',
        })
    )

    def clean_pin(self):
        pin = self.cleaned_data.get('pin', '')
        if not pin.isdigit() or len(pin) != 4:
            raise forms.ValidationError('O PIN deve conter exatamente 4 dígitos numéricos.')
        return pin


class CadastroForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Usuário',
            'class': 'form-input',
            'autocomplete': 'username',
        })
    )
    nome = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome',
            'class': 'form-input',
        })
    )
    sobrenome = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Sobrenome',
            'class': 'form-input',
        })
    )
    pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'PIN (4 dígitos)',
            'class': 'form-input',
            'inputmode': 'numeric',
            'pattern': '[0-9]{4}',
            'maxlength': '4',
        })
    )
    pin_confirma = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme o PIN',
            'class': 'form-input',
            'inputmode': 'numeric',
            'pattern': '[0-9]{4}',
            'maxlength': '4',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().lower()
        if Participante.objects.filter(username=username).exists():
            raise forms.ValidationError('Este usuário já existe.')
        return username

    def clean_pin(self):
        pin = self.cleaned_data.get('pin', '')
        if not pin.isdigit() or len(pin) != 4:
            raise forms.ValidationError('O PIN deve conter exatamente 4 dígitos numéricos.')
        return pin

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        pin_confirma = cleaned_data.get('pin_confirma')
        if pin and pin_confirma and pin != pin_confirma:
            self.add_error('pin_confirma', 'Os PINs não coincidem.')
        return cleaned_data
