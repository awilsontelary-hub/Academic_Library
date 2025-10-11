from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Change the header (top of admin page)
admin.site.site_header = "Academic Library"

# Change the title (browser tab)
admin.site.site_title = "Academic Library"

# Change the index page title
admin.site.index_title = "Welcome to Academic Library"


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
import io
from .models import User, InstitutionalID
from .forms import BulkInstitutionalIDForm

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'account_type_display', 'institutional_id_display', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'student', 'staff', 'academic_level')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Academic Information', {
            'fields': ('student', 'staff', 'academic_level', 'institutional_id')
        }),
        ('Personal Information', {
            'fields': ('address', 'phone_number', 'date_of_birth')
        }),
    )
    
    def account_type_display(self, obj):
        if obj.student:
            return format_html('<span style="color: #2563eb; font-weight: bold;">Student</span>')
        elif obj.staff:
            return format_html('<span style="color: #059669; font-weight: bold;">Staff</span>')
        return format_html('<span style="color: #6b7280;">Unknown</span>')
    account_type_display.short_description = 'Account Type'
    
    def institutional_id_display(self, obj):
        if obj.institutional_id:
            return format_html(
                '<span style="background: #f3f4f6; padding: 4px 8px; border-radius: 6px; font-family: monospace;">{}</span>',
                obj.institutional_id.institutional_id
            )
        return format_html('<span style="color: #dc2626;">No ID</span>')
    institutional_id_display.short_description = 'Institutional ID'

@admin.register(InstitutionalID)
class InstitutionalIDAdmin(admin.ModelAdmin):
    list_display = (
        'institutional_id', 'account_type', 'status_display', 'full_name', 
        'academic_level', 'department', 'created_at', 'expires_at', 'is_expired_display'
    )
    list_filter = ('status', 'account_type', 'academic_level', 'department', 'created_at')
    search_fields = ('institutional_id', 'first_name', 'last_name', 'email', 'department')
    readonly_fields = ('created_at', 'used_at', 'used_by')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('institutional_id', 'account_type', 'status')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'academic_level', 'department')
        }),
        ('Validity', {
            'fields': ('expires_at',)
        }),
        ('Usage Tracking', {
            'fields': ('created_at', 'used_at', 'used_by'),
            'classes': ('collapse',)
        }),
        ('Administrative', {
            'fields': ('added_by', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_active', 'mark_as_expired', 'mark_as_revoked', 'export_as_csv', 'bulk_import_ids']
    
    def status_display(self, obj):
        colors = {
            'active': '#059669',
            'used': '#2563eb',
            'expired': '#dc2626',
            'revoked': '#991b1b'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: uppercase;">{}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.status
        )
    status_display.short_description = 'Status'
    
    def is_expired_display(self, obj):
        if obj.is_expired():
            return format_html('<span style="color: #dc2626; font-weight: bold;">Yes</span>')
        return format_html('<span style="color: #059669; font-weight: bold;">No</span>')
    is_expired_display.short_description = 'Expired'
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} IDs marked as active.', messages.SUCCESS)
    mark_as_active.short_description = "Mark selected IDs as active"
    
    def mark_as_expired(self, request, queryset):
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} IDs marked as expired.', messages.SUCCESS)
    mark_as_expired.short_description = "Mark selected IDs as expired"
    
    def mark_as_revoked(self, request, queryset):
        updated = queryset.update(status='revoked')
        self.message_user(request, f'{updated} IDs marked as revoked.', messages.SUCCESS)
    mark_as_revoked.short_description = "Mark selected IDs as revoked"
    
    def export_as_csv(self, request, queryset):
        """Export selected institutional IDs as CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="institutional_ids.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Institutional ID', 'Account Type', 'Status', 'First Name', 'Last Name',
            'Email', 'Academic Level', 'Department', 'Created At', 'Expires At', 'Notes'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.institutional_id,
                obj.account_type,
                obj.status,
                obj.first_name or '',
                obj.last_name or '',
                obj.email or '',
                obj.academic_level or '',
                obj.department or '',
                obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else '',
                obj.expires_at.strftime('%Y-%m-%d %H:%M:%S') if obj.expires_at else '',
                obj.notes or ''
            ])
        
        return response
    export_as_csv.short_description = "Export selected IDs as CSV"
    
    def bulk_import_ids(self, request, queryset):
        """Bulk import institutional IDs from CSV"""
        if request.method == 'POST':
            form = BulkInstitutionalIDForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                
                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.DictReader(io_string)
                    
                    created_count = 0
                    error_count = 0
                    errors = []
                    
                    for row_num, row in enumerate(reader, start=2):
                        try:
                            institutional_id = row.get('institutional_id', '').strip()
                            if not institutional_id:
                                continue
                            
                            # Check if ID already exists
                            if InstitutionalID.objects.filter(institutional_id=institutional_id).exists():
                                errors.append(f"Row {row_num}: ID '{institutional_id}' already exists")
                                error_count += 1
                                continue
                            
                            InstitutionalID.objects.create(
                                institutional_id=institutional_id,
                                account_type=row.get('account_type', 'student'),
                                first_name=row.get('first_name', '').strip(),
                                last_name=row.get('last_name', '').strip(),
                                email=row.get('email', '').strip(),
                                academic_level=row.get('academic_level', '').strip(),
                                department=row.get('department', '').strip(),
                                added_by=request.user
                            )
                            created_count += 1
                            
                        except Exception as e:
                            errors.append(f"Row {row_num}: {str(e)}")
                            error_count += 1
                    
                    if created_count > 0:
                        self.message_user(request, f'Successfully imported {created_count} institutional IDs.', messages.SUCCESS)
                    
                    if error_count > 0:
                        error_message = f'{error_count} errors occurred:\n' + '\n'.join(errors[:10])
                        if len(errors) > 10:
                            error_message += f'\n... and {len(errors) - 10} more errors'
                        self.message_user(request, error_message, messages.ERROR)
                    
                except Exception as e:
                    self.message_user(request, f'Error processing CSV file: {str(e)}', messages.ERROR)
                
                return redirect(request.get_full_path())
        else:
            form = BulkInstitutionalIDForm()
        
        return render(request, 'admin/accounts/institutionalid/bulk_import.html', {
            'form': form,
            'title': 'Bulk Import Institutional IDs',
            'opts': self.model._meta,
        })
    bulk_import_ids.short_description = "Bulk import IDs from CSV"
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

# Register the models
admin.site.register(User, CustomUserAdmin)
