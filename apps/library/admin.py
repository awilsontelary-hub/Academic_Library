from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.utils.safestring import mark_safe
from .models import Category, BookDetails, BookFile, Recommendation, BookBorrow, BookReview, BookDownload
from apps.accounts.models import User

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'book_count')
    search_fields = ('name',)
    list_per_page = 20
    
    def book_count(self, obj):
        """Display the number of books in this category"""
        count = obj.books.count()
        return format_html(
            '<span style="color: #0066cc; font-weight: bold;">{} books</span>',
            count
        )
    book_count.short_description = 'Books Count'

@admin.register(BookDetails)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'uploaded_by', 'file_count', 'download_count', 'created_at')
    search_fields = ('title', 'author', 'description')
    list_filter = ('category', 'created_at', 'uploaded_by')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    # Custom actions for bulk operations
    actions = ['delete_selected_books', 'export_book_data']
    
    def file_count(self, obj):
        """Display number of files for this book"""
        count = obj.files.count()
        if count == 0:
            return format_html('<span style="color: #ba2121;">No files</span>')
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">{} file{}</span>',
            count, 's' if count != 1 else ''
        )
    file_count.short_description = 'Files'
    
    def download_count(self, obj):
        """Display total downloads for this book"""
        count = BookDownload.objects.filter(book_file__book=obj).count()
        return format_html(
            '<span style="color: #0066cc;">{} downloads</span>',
            count
        )
    download_count.short_description = 'Downloads'
    
    def delete_selected_books(self, request, queryset):
        """Custom bulk delete action with confirmation"""
        count = queryset.count()
        total_files = BookFile.objects.filter(book__in=queryset).count()
        
        # Delete the books (files will be deleted due to CASCADE)
        queryset.delete()
        
        self.message_user(
            request,
            f'Successfully deleted {count} book(s) and {total_files} associated file(s).',
            messages.SUCCESS
        )
    delete_selected_books.short_description = "Delete selected books and all their files"
    
    def export_book_data(self, request, queryset):
        """Custom action to export book data"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Category', 'Uploaded By', 'Created At', 'File Count', 'Download Count'])
        
        for book in queryset:
            writer.writerow([
                book.title,
                book.author,
                book.category.name if book.category else 'No Category',
                book.uploaded_by.username if book.uploaded_by else 'Unknown',
                book.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                book.files.count(),
                BookDownload.objects.filter(book_file__book=book).count()
            ])
        
        return response
    export_book_data.short_description = "Export selected books to CSV"

@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'file_name', 'file_size_mb', 'uploaded_at', 'download_count')
    search_fields = ('book__title', 'file')
    list_filter = ('uploaded_at', 'book__category')
    readonly_fields = ('uploaded_at', 'file_size')
    list_per_page = 30
    
    actions = ['delete_selected_files']
    
    def book_title(self, obj):
        """Display book title with link"""
        return format_html(
            '<a href="{}" style="text-decoration: none; color: #417690;">{}</a>',
            reverse('admin:library_bookdetails_change', args=[obj.book.id]),
            obj.book.title[:50] + ('...' if len(obj.book.title) > 50 else '')
        )
    book_title.short_description = 'Book'
    book_title.admin_order_field = 'book__title'
    
    def file_name(self, obj):
        """Display file name"""
        name = obj.file.name.split('/')[-1] if obj.file else 'No file'
        return format_html(
            '<span style="font-family: monospace; color: #333;">{}</span>',
            name[:40] + ('...' if len(name) > 40 else '')
        )
    file_name.short_description = 'File Name'
    
    def file_size_mb(self, obj):
        """Display file size in MB"""
        if obj.file_size:
            size_mb = obj.file_size / (1024 * 1024)
            if size_mb < 1:
                return format_html('<span style="color: #28a745;">{:.2f} KB</span>', obj.file_size / 1024)
            else:
                return format_html('<span style="color: #0066cc;">{:.2f} MB</span>', size_mb)
        return format_html('<span style="color: #6c757d;">Unknown</span>')
    file_size_mb.short_description = 'Size'
    
    def download_count(self, obj):
        """Display download count"""
        count = obj.downloads.count()
        return format_html(
            '<span style="color: #17a2b8; font-weight: bold;">{} downloads</span>',
            count
        )
    download_count.short_description = 'Downloads'
    
    def delete_selected_files(self, request, queryset):
        """Custom bulk delete for files"""
        count = queryset.count()
        books_affected = set(f.book.title for f in queryset)
        
        # Delete the files
        queryset.delete()
        
        self.message_user(
            request,
            f'Successfully deleted {count} file(s) from {len(books_affected)} book(s)',
            messages.SUCCESS
        )
    delete_selected_files.short_description = "Delete selected files"

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'recommended_by', 'message_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('book__title', 'recommended_by__username', 'message')
    readonly_fields = ('created_at',)
    
    def book_title(self, obj):
        return obj.book.title[:50] + ('...' if len(obj.book.title) > 50 else '')
    book_title.short_description = 'Book'
    
    def message_preview(self, obj):
        if obj.message:
            return obj.message[:100] + ('...' if len(obj.message) > 100 else '')
        return format_html('<span style="color: #6c757d;">No message</span>')
    message_preview.short_description = 'Message'

@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'borrower_info', 'status_display', 'borrowed_date', 'due_date')
    list_filter = ('status', 'borrowed_date', 'due_date')
    search_fields = ('book__title', 'borrower__username', 'borrower__first_name', 'borrower__last_name')
    readonly_fields = ('borrowed_date',)
    actions = ['approve_borrows', 'mark_as_returned']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'borrower', 'approved_by')
    
    def book_title(self, obj):
        return obj.book.title[:40] + ('...' if len(obj.book.title) > 40 else '')
    book_title.short_description = 'Book'
    
    def borrower_info(self, obj):
        return format_html(
            '<div><strong>{}</strong></div><div style="color: #6c757d; font-size: 11px;">{}</div>',
            obj.borrower.username,
            obj.borrower.email
        )
    borrower_info.short_description = 'Borrower'
    
    def status_display(self, obj):
        colors = {
            'pending': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545',
            'returned': '#17a2b8',
            'overdue': '#e74c3c'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def approve_borrows(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='approved', approved_by=request.user)
        self.message_user(request, f'Approved {updated} borrow request(s).', messages.SUCCESS)
    approve_borrows.short_description = "Approve selected borrow requests"
    
    def mark_as_returned(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='approved').update(status='returned', return_date=timezone.now())
        self.message_user(request, f'Marked {updated} borrow(s) as returned.', messages.SUCCESS)
    mark_as_returned.short_description = "Mark selected borrows as returned"

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'reviewer_info', 'rating_display', 'comment_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'reviewer__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    def book_title(self, obj):
        return obj.book.title[:40] + ('...' if len(obj.book.title) > 40 else '')
    book_title.short_description = 'Book'
    
    def reviewer_info(self, obj):
        return format_html(
            '<div><strong>{}</strong></div><div style="color: #6c757d; font-size: 11px;">{}</div>',
            obj.reviewer.username,
            obj.reviewer.email
        )
    reviewer_info.short_description = 'Reviewer'
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}</span> <span style="color: #6c757d;">({}/5)</span>',
            stars, obj.rating
        )
    rating_display.short_description = 'Rating'
    
    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:80] + ('...' if len(obj.comment) > 80 else '')
        return format_html('<span style="color: #6c757d;">No comment</span>')
    comment_preview.short_description = 'Comment'

@admin.register(BookDownload)
class BookDownloadAdmin(admin.ModelAdmin):
    list_display = ('book_info', 'user_info', 'downloaded_at', 'ip_address')
    list_filter = ('downloaded_at', 'book_file__book__category')
    search_fields = ('book_file__book__title', 'user__username', 'ip_address')
    readonly_fields = ('downloaded_at', 'ip_address', 'user_agent')
    date_hierarchy = 'downloaded_at'
    list_per_page = 50
    
    def book_info(self, obj):
        return format_html(
            '<div><strong>{}</strong></div>'
            '<div style="color: #6c757d; font-size: 11px;">{}</div>',
            obj.book_file.book.title[:40] + ('...' if len(obj.book_file.book.title) > 40 else ''),
            obj.book_file.file.name.split('/')[-1] if obj.book_file.file else 'No file'
        )
    book_info.short_description = 'Book & File'
    
    def user_info(self, obj):
        return format_html(
            '<div><strong>{}</strong></div>'
            '<div style="color: #6c757d; font-size: 11px;">{}</div>',
            obj.user.username,
            obj.user.email
        )
    user_info.short_description = 'User'

# Custom Admin Site Configuration
admin.site.site_header = "AcademiaLink Library Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Library Management Dashboard"
admin.site.enable_nav_sidebar = True
