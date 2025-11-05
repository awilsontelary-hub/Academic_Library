"""
Forms for book management, borrowing, reviews, and search.
"""
from django import forms

from .models import BookBorrow, BookDetails, BookReview, Category


class BookUploadForm(forms.ModelForm):
    """Form for staff to upload new books to the library."""
    
    class Meta:
        model = BookDetails
        fields = ['title', 'author', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class BookBorrowForm(forms.ModelForm):
    """Form for students to request to borrow a book."""
    
    class Meta:
        model = BookBorrow
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional notes for your borrow request'
            }),
        }


class BookReviewForm(forms.ModelForm):
    """Form for users to submit or update book reviews."""
    
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts about this book...'
            }),
        }


class BookSearchForm(forms.Form):
    """Search form for filtering books by query and category."""
    
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search books by title, author, or description...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

