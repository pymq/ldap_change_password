from django import forms
from django.contrib.auth import password_validation
from django.conf import settings
import ldap


class ChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
        'invalid_credentials': ("Invalid username or old password."),
    }
    username = forms.CharField(max_length=254, required=True)
    old_password = forms.CharField(
        label='Old password',
        max_length=254,
        required=True,
        widget=forms.PasswordInput,
    )
    new_password1 = forms.CharField(
        label='New password',
        max_length=254,
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        max_length=254,
        required=True,
        widget=forms.PasswordInput,
        help_text=("Enter the same password as before, for verification."),
    )

    def clean(self):
        """
        Validates that the old_password and username are correct.
        """
        old_password = self.cleaned_data["old_password"]
        username = self.cleaned_data["username"]

        try:
            con = ldap.initialize(settings.LDAP_CONNECTION_URL, bytes_mode=False)
            con.simple_bind_s(f'uid={username},{settings.LDAP_PATH}', old_password)
            con.unbind_s()
        except ldap.INVALID_CREDENTIALS:
            raise forms.ValidationError(
                self.error_messages['invalid_credentials'],
                code='invalid_credentials',
            )
        return super().clean()

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self):
        old_password = self.cleaned_data["old_password"]
        new_password = self.cleaned_data["new_password1"]
        username = self.cleaned_data["username"]
        con = ldap.initialize(settings.LDAP_CONNECTION_URL, bytes_mode=False)
        con.simple_bind_s(f'uid={username},{settings.LDAP_PATH}', old_password)
        con.passwd_s(f'uid={username},{settings.LDAP_PATH}', old_password, new_password)
        con.unbind_s()
        return None
