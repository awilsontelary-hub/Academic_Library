from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    academic_level = forms.CharField(max_length=32, required=False)
    is_student = forms.BooleanField(required=False, initial=True)
    is_staff = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'academic_level', 'is_student', 'is_staff', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get('is_student')
        is_staff = cleaned_data.get('is_staff')
        
        if not is_student and not is_staff:
            raise forms.ValidationError("User must be either a student or staff member.")
        
        if is_student and is_staff:
            raise forms.ValidationError("User cannot be both student and staff.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.academic_level = self.cleaned_data['academic_level']
        user.student = self.cleaned_data['is_student']
        user.staff = self.cleaned_data['is_staff']
        
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'academic_level')
