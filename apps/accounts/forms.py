from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, InstitutionalID

class CustomUserCreationForm(UserCreationForm):
    # Institutional verification field
    institutional_id = forms.CharField(
        max_length=20,
        required=True,
        help_text="Enter your institutional ID (Student ID or Employee ID)",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., STU2024001 or EMP2024001',
            'class': 'form-control'
        })
    )
    
    # Basic user information
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Account type fields (will be auto-filled based on institutional ID)
    is_student = forms.BooleanField(required=False, initial=True)
    is_staff = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ('institutional_id', 'username', 'email', 'first_name', 'last_name', 
                 'is_student', 'is_staff', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_student', 'is_staff']:
                field.widget.attrs['class'] = 'form-control'
        
        # Make account type fields read-only since they'll be determined by institutional ID
        self.fields['is_student'].widget.attrs['style'] = 'display: none;'
        self.fields['is_staff'].widget.attrs['style'] = 'display: none;'

    def clean_institutional_id(self):
        """Validate the institutional ID"""
        institutional_id = self.cleaned_data.get('institutional_id')
        
        if not institutional_id:
            raise ValidationError("Institutional ID is required.")
        
        # Check if the institutional ID exists and is available
        try:
            id_record = InstitutionalID.objects.get(institutional_id=institutional_id)
        except InstitutionalID.DoesNotExist:
            raise ValidationError(
                "Invalid institutional ID. Please contact the library administration "
                "if you believe this is an error."
            )
        
        # Check if the ID is available for use
        if not id_record.is_available:
            if id_record.status == 'used':
                raise ValidationError(
                    "This institutional ID has already been used for registration."
                )
            elif id_record.status == 'expired':
                raise ValidationError(
                    "This institutional ID has expired. Please contact administration."
                )
            elif id_record.status == 'revoked':
                raise ValidationError(
                    "This institutional ID has been revoked. Please contact administration."
                )
            else:
                raise ValidationError(
                    "This institutional ID is not available for registration."
                )
        
        # Check if ID has expired
        if id_record.is_expired():
            raise ValidationError(
                "This institutional ID has expired. Please contact administration."
            )
        
        # Store the ID record for use in save method
        self.institutional_id_record = id_record
        return institutional_id

    def clean_email(self):
        """Validate email and check for duplicates"""
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        
        return email

    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        
        return username

    def clean(self):
        """Final form validation"""
        cleaned_data = super().clean()
        
        # Auto-set account type based on institutional ID
        if hasattr(self, 'institutional_id_record'):
            id_record = self.institutional_id_record
            
            if id_record.account_type == 'student':
                cleaned_data['is_student'] = True
                cleaned_data['is_staff'] = False
            elif id_record.account_type == 'staff':
                cleaned_data['is_student'] = False
                cleaned_data['is_staff'] = True
            
            # Pre-fill information if available in institutional record
            if id_record.first_name and not cleaned_data.get('first_name'):
                cleaned_data['first_name'] = id_record.first_name
            
            if id_record.last_name and not cleaned_data.get('last_name'):
                cleaned_data['last_name'] = id_record.last_name
            
            if id_record.email and not cleaned_data.get('email'):
                cleaned_data['email'] = id_record.email
        
        return cleaned_data

    def save(self, commit=True):
        """Save the user and link to institutional ID"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.student = self.cleaned_data['is_student']
        user.staff = self.cleaned_data['is_staff']
        
        # Set academic level from institutional ID if available
        if hasattr(self, 'institutional_id_record'):
            id_record = self.institutional_id_record
            if id_record.academic_level:
                user.academic_level = id_record.academic_level
        
        # Set user as inactive until admin approval
        user.is_active = False
        
        if commit:
            # Save user first without institutional_id to avoid constraint issues
            user.save()
            
            # Now link user to institutional ID and mark it as used
            if hasattr(self, 'institutional_id_record'):
                user.institutional_id = self.institutional_id_record
                user.save(update_fields=['institutional_id'])
                self.institutional_id_record.mark_as_used(user)
        
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class InstitutionalIDForm(forms.ModelForm):
    """Form for administrators to add/edit institutional IDs"""
    
    class Meta:
        model = InstitutionalID
        fields = ('institutional_id', 'account_type', 'first_name', 'last_name', 
                 'email', 'academic_level', 'department', 'expires_at', 'notes')
        widgets = {
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class BulkInstitutionalIDForm(forms.Form):
    """Form for bulk importing institutional IDs via CSV"""
    
    csv_file = forms.FileField(
        help_text="Upload a CSV file with columns: institutional_id, account_type, first_name, last_name, email, academic_level, department"
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        
        if not file.name.endswith('.csv'):
            raise ValidationError("Please upload a CSV file.")
        
        return file
