from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    """Inherit everything in UserChangeForm but pass the custom user model instead of base user model"""

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    """Inherits UserCreationForm and uses custom user model. Provides first_name, last_name, and email fields for user creation."""

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")

    error_mesages = {
        "duplicate": "A user with this email already exists.",
    }

    def clean_email(self):
        """Checks if email provided is already in the database and will return email. Otherwise it returns an error"""
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])
