from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    # Public pages
    path('admin/', name='admin'),
    path("", views.home_view, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("faq/", views.faq_view, name="faq"),
    path("about/", views.about_view, name="about"),
    
    # Student pages
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("books/<int:book_id>/borrow/", views.borrow_book, name="borrow_book"),
    path("books/<int:book_id>/review/", views.add_review, name="add_review"),
    path("borrows/<int:borrow_id>/return/", views.return_book, name="return_book"),
    
    # Teacher pages
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("statistics/", views.statistics_view, name="statistics"),
    path("upload/", views.upload_book, name="upload_book"),
    path("borrows/", views.manage_borrows, name="manage_borrows"),
    path("borrows/<int:borrow_id>/approve/", views.approve_borrow, name="approve_borrow"),
    path("borrows/<int:borrow_id>/reject/", views.reject_borrow, name="reject_borrow"),
    
    # File downloads and previews
    path("download/<int:file_id>/", views.download_book_file, name="download_book"),
    path("preview/<int:file_id>/", views.preview_book_file, name="preview_book"),
]
