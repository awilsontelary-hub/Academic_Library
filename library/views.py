from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import timedelta
from apps.accounts.decorators import teacher_required, student_required
from apps.accounts.models import User
from .models import BookDetails, BookFile, BookBorrow, BookReview, Category, Recommendation
from .forms import BookUploadForm, BookBorrowForm, BookReviewForm, BookSearchForm
from django.views.decorators.http import require_POST
import json

def home_view(request):
    """Home page with featured books and statistics"""
    featured_books = BookDetails.objects.all()[:6]
    total_books = BookDetails.objects.count()
    total_users = User.objects.count()
    recent_books = BookDetails.objects.order_by('-created_at')[:3]
    
    context = {
        'featured_books': featured_books,
        'total_books': total_books,
        'total_users': total_users,
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
    
    context = {
        'pending_borrows': pending_borrows,
        'all_borrows': all_borrows,
        'total_books': total_books,
        'total_borrows': total_borrows,
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
    if request.user.is_authenticated and request.user.student:
        existing_borrow = BookBorrow.objects.filter(book=book, borrower=request.user, status__in=['pending', 'approved']).exists()
        can_borrow = not existing_borrow
    
    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'can_borrow': can_borrow,
    }
    return render(request, 'library/book_detail.html', context)

@login_required
def download_book_file(request, file_id):
    """Secure book file download"""
    book_file = get_object_or_404(BookFile, id=file_id)
    
    # Check if user has access to this book
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in.")
    
    # Log the download
    # You could add download tracking here
    
    return FileResponse(book_file.file, as_attachment=True)

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
    borrow = get_object_or_404(BookBorrow, id=borrow_id)
    borrow.status = 'approved'
    borrow.approved_by = request.user
    borrow.save()
    
    messages.success(request, 'Borrow request approved!')
    return redirect('library:manage_borrows')

@login_required
@teacher_required
@require_POST
def reject_borrow(request, borrow_id):
    """Reject a borrow request"""
    borrow = get_object_or_404(BookBorrow, id=borrow_id)
    borrow.status = 'rejected'
    borrow.approved_by = request.user
    borrow.save()
    
    messages.success(request, 'Borrow request rejected!')
    return redirect('library:manage_borrows')

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
