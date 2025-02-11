from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserCred, Department

class CustomUserCreationForm(UserCreationForm):
    department = forms.ChoiceField(choices=Department.choices, label="Departman")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # UserCred kaydını oluştur
            department = self.cleaned_data['department']
            UserCred.objects.create(user=user, department=department)
        return user