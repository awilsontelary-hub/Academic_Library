from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Change the header (top of admin page)
admin.site.site_header = "Academic Library"

# Change the title (browser tab)
admin.site.site_title = "Academic Library"

# Change the index page title
admin.site.index_title = "Welcome to Academic Library"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Optional: customize the fields you see in admin
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('staff', 'student')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Fields', {'fields': ('staff', 'student')}),
    )

    search_fields = ('title', 'book')
