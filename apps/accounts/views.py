"""
Account views for user authentication, registration, and profile management.
"""
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserUpdateForm


class CustomLoginView(LoginView):
    """
    Custom login view with role-based redirection.
    
    Redirects users to appropriate dashboards based on their role:
    - Staff/Faculty: Teacher dashboard
    - Students: Student dashboard
    - Others: Home page
    """
    
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Determine redirect URL based on user role."""
        if self.request.user.staff:
            return reverse_lazy('library:teacher_dashboard')
        elif self.request.user.student:
            return reverse_lazy('library:student_dashboard')
        return reverse_lazy('library:home')


def register_view(request):
    """
    User registration view with institutional ID verification.
    
    New users must provide a valid institutional ID. After successful
    registration, accounts are automatically activated and users can log in immediately.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Registration successful! Your account has been activated. '
                'You can now log in with your username and password, or use your institutional ID.'
            )
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    User profile view and update form.
    
    Allows authenticated users to view and update their profile information.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


def logout_view(request):
    """
    Logout view.
    
    Logs out the current user and redirects to home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('library:home')

