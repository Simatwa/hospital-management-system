from django import forms
from users.models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserCreationForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
            "date_of_birth",
            "location",
            "password",
            # "profile",
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return make_password(password)
        return password


class CustomUserUpdateForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "username",
            "email",
            "password",
            "gender",
            "last_name",
            "profile",
        ]
