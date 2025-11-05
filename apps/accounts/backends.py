"""
Custom authentication backend for institutional ID verification.
"""
from django.contrib.auth.backends import ModelBackend
from .models import User, InstitutionalID


class InstitutionalIDBackend(ModelBackend):
    """
    Enhanced authentication backend that supports logging in with institutional ID.
    
    This backend allows users who have already registered with their institutional ID
    to log in using that ID instead of their username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by username or institutional ID.
        
        Checks if the username is actually an institutional ID and
        finds the associated user account.
        """
        if not username or not password:
            return None
        
        try:
            # First, try to find a user by username (standard login)
            try:
                user = User.objects.get(username=username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            except User.DoesNotExist:
                pass
            
            # If not found, try to find by institutional ID
            inst_id = InstitutionalID.objects.get(institutional_id=username)
            
            # Check if this ID has been used (registered)
            if inst_id.used_by:
                user = inst_id.used_by
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            
            # ID exists but hasn't been used for registration yet
            return None
            
        except InstitutionalID.DoesNotExist:
            # Not an institutional ID, already tried username above
            return None
        except Exception:
            return None
