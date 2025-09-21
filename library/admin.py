from django.contrib import admin
from .models import Category, BookDetails, BookFile, Recommendation, BookBorrow, BookReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(BookDetails)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'uploaded_by', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'file', 'file_size', 'uploaded_at')
    search_fields = ('book__title', 'file')
    list_filter = ('uploaded_at',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('book', 'recommended_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('book__title', 'recommended_by__username')

@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'status', 'borrowed_date', 'due_date', 'return_date')
    list_filter = ('status', 'borrowed_date', 'due_date')
    search_fields = ('book__title', 'borrower__username', 'borrower__first_name', 'borrower__last_name')
    readonly_fields = ('borrowed_date',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'borrower', 'approved_by')

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'reviewer__username', 'reviewer__first_name', 'reviewer__last_name')
    readonly_fields = ('created_at', 'updated_at')
