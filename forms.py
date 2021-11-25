# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import forms as auth_forms
from .models import User


class AccountCreationForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput, help_text='Required.')
    confirm_privacy = forms.BooleanField()

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'full_name', 'confirm_privacy')
        required = ('first_name', 'last_name', 'full_name', 'confirm_privacy')

    def get_user_email(self):
        return self.user.email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        user = self.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.full_name = self.cleaned_data['full_name']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountCreationByAdminForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(AccountCreationByAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(AccountCreationByAdminForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2


class EditAccountForm(UserChangeForm):

    password = auth_forms.ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"/accounts/password_change/\">this form</a>."
        )

    # use input for text rather than text area
    full_name = forms.CharField(widget=forms.TextInput, help_text='Required.')

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'full_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
