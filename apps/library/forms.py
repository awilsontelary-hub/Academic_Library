from django import forms
from .models import BookDetails, BookBorrow, BookReview, Category

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = BookDetails
        fields = ['title', 'author', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = BookBorrow
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes for your borrow request'}),
        }

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts about this book...'}),
        }

class BookSearchForm(forms.Form):
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
