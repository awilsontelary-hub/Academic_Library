from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.utils import timezone
from apps.accounts.decorators import teacher_required, student_required
from apps.accounts.models import User
from .models import BookDetails, BookFile, BookBorrow, BookReview, Category, BookDownload
from .forms import BookUploadForm, BookBorrowForm, BookReviewForm, BookSearchForm
from django.views.decorators.http import require_POST

def home_view(request):
    """Home page with featured books and statistics"""
    featured_books = BookDetails.objects.all()[:6]
    total_books = BookDetails.objects.count()
    total_users = User.objects.count()
    total_downloads = BookDownload.objects.count()
    recent_books = BookDetails.objects.order_by('-created_at')[:3]
    
    context = {
        'featured_books': featured_books,
        'total_books': total_books,
        'total_users': total_users,
        'total_downloads': total_downloads,
        'recent_books': recent_books,
    }
    return render(request, 'library/home.html', context)

@login_required
def student_dashboard(request):
    """Student dashboard with borrowed books and recommendations"""
    user = request.user
    borrowed_books = BookBorrow.objects.filter(borrower=user).order_by('-borrowed_date')
    overdue_books = borrowed_books.filter(status='approved', due_date__lt=timezone.now(), return_date__isnull=True)
    recent_books = BookDetails.objects.order_by('-created_at')[:5]
    
    context = {
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books,
        'recent_books': recent_books,
    }
    return render(request, 'library/student_dashboard.html', context)

@login_required
@teacher_required
def teacher_dashboard(request):
    """Teacher dashboard with book management and pending borrows"""
    pending_borrows = BookBorrow.objects.filter(status='pending').order_by('-borrowed_date')
    all_borrows = BookBorrow.objects.all().order_by('-borrowed_date')[:10]
    total_books = BookDetails.objects.count()
    total_borrows = BookBorrow.objects.count()
    recent_books = BookDetails.objects.order_by('-created_at')[:12]  # Show more books for teachers
    
    context = {
        'pending_borrows': pending_borrows,
        'all_borrows': all_borrows,
        'total_books': total_books,
        'total_borrows': total_borrows,
        'recent_books': recent_books,
    }
    return render(request, 'library/teacher_dashboard.html', context)

def book_list(request):
    """Public book list with search and filtering"""
    books = BookDetails.objects.all()
    categories = Category.objects.all()
    search_form = BookSearchForm(request.GET)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category:
            books = books.filter(category=category)
    
    # Add average rating to each book
    for book in books:
        book.avg_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    context = {
        'books': books,
        'categories': categories,
        'search_form': search_form,
    }
    return render(request, 'library/book_list.html', context)

def book_detail(request, book_id):
    """Detailed book view with reviews and borrow option"""
    book = get_object_or_404(BookDetails, id=book_id)
    reviews = book.reviews.all()[:10]
    avg_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Check if user can borrow this book
    can_borrow = False
    has_approved_access = False
    is_staff_access = False
    
    if request.user.is_authenticated:
        # Staff/teachers and admin/superusers have unrestricted access
        if request.user.staff or request.user.is_superuser:
            has_approved_access = True
            is_staff_access = True
        elif request.user.student:
            existing_borrow = BookBorrow.objects.filter(book=book, borrower=request.user, status__in=['pending', 'approved']).exists()
            can_borrow = not existing_borrow
            
            # Check if user has approved access to this book
            has_approved_access = BookBorrow.objects.filter(
                book=book, 
                borrower=request.user, 
                status='approved'
            ).exists()
    
    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'can_borrow': can_borrow,
        'has_approved_access': has_approved_access,
        'is_staff_access': is_staff_access,
    }
    return render(request, 'library/book_detail.html', context)

@login_required
def download_book_file(request, file_id):
    """Secure book file download - for approved borrowers, staff, or admin"""
    book_file = get_object_or_404(BookFile, id=file_id)
    
    # Check if user has approved access to this book
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    
    # Staff/teachers and admin/superusers have unrestricted access
    if request.user.staff or request.user.is_superuser:
        # Track the download
        BookDownload.objects.create(
            book_file=book_file,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
        )
        return FileResponse(book_file.file, as_attachment=True)
    
    # For students, check if user has an approved borrow for this book
    has_access = BookBorrow.objects.filter(
        book=book_file.book,
        borrower=request.user,
        status='approved'
    ).exists()
    
    if not has_access:
        return HttpResponseForbidden("You don't have permission to download this book. Please borrow it first.")
    
    # Track the download for students too
    BookDownload.objects.create(
        book_file=book_file,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
    )
    
    return FileResponse(book_file.file, as_attachment=True)

@login_required
def preview_book_file(request, file_id):
    """Preview book file in browser - for approved borrowers, staff, or admin"""
    book_file = get_object_or_404(BookFile, id=file_id)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    
    # Staff/teachers and admin/superusers have unrestricted access
    has_access = False
    if request.user.staff or request.user.is_superuser:
        has_access = True
    else:
        # For students, check if user has an approved borrow for this book
        has_access = BookBorrow.objects.filter(
            book=book_file.book,
            borrower=request.user,
            status='approved'
        ).exists()
    
    if not has_access:
        return HttpResponseForbidden("You don't have permission to preview this book. Please borrow it first.")
    
    # Get file extension to determine if it's previewable
    file_extension = book_file.file.name.split('.')[-1].lower()
    
    # Only allow preview for certain file types
    previewable_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'txt']
    
    if file_extension not in previewable_extensions:
        return HttpResponseForbidden("This file type cannot be previewed.")
    
    # For PDF files, serve inline; for images and text, also serve inline
    if file_extension == 'pdf':
        response = FileResponse(book_file.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{book_file.file.name.split("/")[-1]}"'
    elif file_extension in ['jpg', 'jpeg', 'png']:
        response = FileResponse(book_file.file, content_type=f'image/{file_extension}')
        response['Content-Disposition'] = f'inline; filename="{book_file.file.name.split("/")[-1]}"'
    elif file_extension == 'txt':
        response = FileResponse(book_file.file, content_type='text/plain')
        response['Content-Disposition'] = f'inline; filename="{book_file.file.name.split("/")[-1]}"'
    
    return response

@login_required
@teacher_required
def upload_book(request):
    """Book upload form for teachers"""
    if request.method == 'POST':
        form = BookUploadForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            
            # Handle file uploads
            files = request.FILES.getlist('files')
            for file in files:
                BookFile.objects.create(book=book, file=file)
            
            messages.success(request, 'Book uploaded successfully!')
            return redirect('library:book_detail', book_id=book.id)
    else:
        form = BookUploadForm()
    
    return render(request, 'library/upload_book.html', {'form': form})

@login_required
@student_required
def borrow_book(request, book_id):
    """Borrow a book (student only)"""
    book = get_object_or_404(BookDetails, id=book_id)
    
    if request.method == 'POST':
        form = BookBorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            borrow.borrower = request.user
            borrow.save()
            
            messages.success(request, 'Borrow request submitted successfully!')
            return redirect('library:book_detail', book_id=book.id)
    else:
        form = BookBorrowForm()
    
    return render(request, 'library/borrow_book.html', {'form': form, 'book': book})

@login_required
@teacher_required
def statistics_view(request):
    """Statistics dashboard for admin and staff users"""
    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    # Basic statistics
    total_books = BookDetails.objects.count()
    total_users = User.objects.count()
    total_downloads = BookDownload.objects.count()
    total_borrows = BookBorrow.objects.count()
    active_borrows = BookBorrow.objects.filter(status='approved', return_date__isnull=True).count()
    
    # User statistics
    total_students = User.objects.filter(student=True).count()
    total_staff = User.objects.filter(staff=True).count()
    total_admin = User.objects.filter(is_superuser=True).count()
    
    # Detailed user lists
    all_students = User.objects.filter(student=True).order_by('first_name', 'last_name')
    all_staff = User.objects.filter(staff=True).order_by('first_name', 'last_name')
    all_admins = User.objects.filter(is_superuser=True).order_by('first_name', 'last_name')
    
    # Book statistics with detailed book lists
    books_by_category = []
    category_stats = BookDetails.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    for category in category_stats:
        category_name = category['category__name']
        if category_name:
            books = BookDetails.objects.filter(category__name=category_name).order_by('title')[:10]
        else:
            books = BookDetails.objects.filter(category__isnull=True).order_by('title')[:10]
        
        books_by_category.append({
            'category__name': category_name,
            'count': category['count'],
            'books': books
        })
    
    # Download statistics (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_downloads = BookDownload.objects.filter(
        downloaded_at__gte=thirty_days_ago
    ).count()
    
    # Most downloaded books
    most_downloaded_books = BookDetails.objects.annotate(
        download_count=Count('files__downloads')
    ).filter(download_count__gt=0).order_by('-download_count')[:5]
    
    # Recent activity
    recent_downloads_list = BookDownload.objects.select_related(
        'book_file__book', 'user'
    ).order_by('-downloaded_at')[:10]
    
    recent_borrows = BookBorrow.objects.select_related(
        'book', 'borrower'
    ).order_by('-borrowed_date')[:10]
    
    # Pending requests
    pending_borrows = BookBorrow.objects.filter(status='pending').count()
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_downloads': total_downloads,
        'total_borrows': total_borrows,
        'active_borrows': active_borrows,
        'total_students': total_students,
        'total_staff': total_staff,
        'total_admin': total_admin,
        'all_students': all_students,
        'all_staff': all_staff,
        'all_admins': all_admins,
        'books_by_category': books_by_category,
        'recent_downloads': recent_downloads,
        'most_downloaded_books': most_downloaded_books,
        'recent_downloads_list': recent_downloads_list,
        'recent_borrows': recent_borrows,
        'pending_borrows': pending_borrows,
    }
    return render(request, 'library/statistics.html', context)

@login_required
@teacher_required
def manage_borrows(request):
    """Manage book borrows (teacher only)"""
    borrows = BookBorrow.objects.all().order_by('-borrowed_date')
    
    context = {
        'borrows': borrows,
    }
    return render(request, 'library/manage_borrows.html', context)

@login_required
@teacher_required
@require_POST
def approve_borrow(request, borrow_id):
    """Approve a borrow request"""
    try:
        borrow = get_object_or_404(BookBorrow, id=borrow_id)
        borrow.status = 'approved'
        borrow.approved_by = request.user
        borrow.save()
        
        messages.success(request, f'Borrow request for "{borrow.book.title}" has been approved!')
        
        # Always redirect to teacher dashboard for now to test
        return redirect('library:teacher_dashboard')
        
    except Exception as e:
        messages.error(request, f'Error approving borrow request: {str(e)}')
        return redirect('library:teacher_dashboard')

@login_required
@teacher_required
@require_POST
def reject_borrow(request, borrow_id):
    """Reject a borrow request"""
    try:
        borrow = get_object_or_404(BookBorrow, id=borrow_id)
        borrow.status = 'rejected'
        borrow.approved_by = request.user
        borrow.save()
        
        messages.success(request, f'Borrow request for "{borrow.book.title}" has been rejected!')
        
        # Always redirect to teacher dashboard for now to test
        return redirect('library:teacher_dashboard')
        
    except Exception as e:
        messages.error(request, f'Error rejecting borrow request: {str(e)}')
        return redirect('library:teacher_dashboard')

@login_required
@require_POST
def return_book(request, borrow_id):
    """Return a borrowed book"""
    borrow = get_object_or_404(BookBorrow, id=borrow_id, borrower=request.user)
    borrow.status = 'returned'
    borrow.return_date = timezone.now()
    borrow.save()
    
    messages.success(request, 'Book returned successfully!')
    return redirect('library:student_dashboard')

@login_required
def add_review(request, book_id):
    """Add a book review"""
    book = get_object_or_404(BookDetails, id=book_id)
    
    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review, created = BookReview.objects.get_or_create(
                book=book,
                reviewer=request.user,
                defaults=form.cleaned_data
            )
            if not created:
                review.rating = form.cleaned_data['rating']
                review.comment = form.cleaned_data['comment']
                review.save()
            
            messages.success(request, 'Review added successfully!')
            return redirect('library:book_detail', book_id=book.id)
    else:
        form = BookReviewForm()
    
    return render(request, 'library/add_review.html', {'form': form, 'book': book})

def faq_view(request):
    """FAQ page with common questions and answers"""
    return render(request, 'library/faq.html')

def about_view(request):
    """About page with library information and features"""
    # Get some statistics for the about page
    total_books = BookDetails.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    total_downloads = BookDownload.objects.count()
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_downloads': total_downloads,
    }
    return render(request, 'library/about.html', context)
