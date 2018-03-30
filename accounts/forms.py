from django import forms
from django.contrib.auth import password_validation


class ChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
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

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        # if not self.user.check_password(old_password):
        #     raise forms.ValidationError(
        #         self.error_messages['password_incorrect'],
        #         code='password_incorrect',
        #     )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        # password = self.cleaned_data["new_password1"]
        # self.user.set_password(password)
        # if commit:
        #     self.user.save()
        return None
