# AcademiaLink Library Management System

A comprehensive digital library management system built with Django, designed for academic institutions to manage books, users, and borrowing processes efficiently.

## 🚀 Features

### User Management
- **Multi-role Authentication**: Students, Staff/Teachers, and Administrators
- **User Profiles**: Complete user information requirements
- **Role-based Permissions**: Different access levels for different user types

### Library Management
- **Book Management**: Add, edit, and organize books with categories
- **File Upload**: Support for PDF, DOC, and image files
- **Book Preview**: Teachers and staff can preview books before borrowing
- **Advanced Search**: Search books by title, author, category, and description

### Borrowing System
- **Smart Borrowing**: Automated borrowing process with approval workflow
- **Request Management**: Teachers can approve/reject borrow requests
- **Due Date Tracking**: Automatic due date calculation and tracking
- **No Restrictions**: Staff and admin users can borrow without limitations

### Analytics & Statistics
- **Interactive Dashboard**: Comprehensive statistics with clickable sections
- **Download Tracking**: Real-time download statistics and user tracking
- **User Analytics**: Detailed user information with expandable sections
- **Activity Monitoring**: Recent downloads and borrow requests tracking

### Professional Design
- **Modern UI**: Blue and white library-themed design
- **Responsive Layout**: Works perfectly on all devices
- **Smooth Animations**: Professional transitions and hover effects
- **Intuitive Navigation**: Easy-to-use interface for all user types

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5.3.0, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **File Handling**: Pillow for image processing
- **Deployment**: Gunicorn, Whitenoise for static files
- **Environment**: Python-decouple for environment variables

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd Academic_Library-main
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
# Set SECRET_KEY, DEBUG, DATABASE_URL, EMAIL settings, etc.
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🚀 Deployment

### Using the Deployment Script
```bash
python deploy.py
```

### Manual Deployment Steps
1. Set environment variables for production
2. Configure database (PostgreSQL recommended)
3. Run `python manage.py collectstatic`
4. Run `python manage.py migrate`
5. Deploy using your preferred platform (Heroku, Digital Ocean, etc.)

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

## 📁 Project File Structure

```
Academic_Library-main/
├── apps/
│   ├── accounts/          # User authentication and profiles
│   │   ├── models.py      # Custom User model
│   │   ├── views.py       # Authentication views
│   │   ├── forms.py       # User forms
│   │   └── templates/     # Account templates
│   └── library/           # Library management
│       ├── models.py      # Book, Category, Borrow models
│       ├── views.py       # Library views
│       ├── forms.py       # Library forms
│       └── templates/     # Library templates
├── online_library/        # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI configuration
├── static/               # Static files (CSS, JS, Images)
├── media/                # User uploaded files
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── deploy.py            # Deployment script
├── Procfile             # Heroku deployment
└── README.md            # This file
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Database (for production)
DATABASE_URL=postgres://user:password@host:port/database
```

## 👥 User Roles & Permissions

### Students
- Browse and search books
- Request to borrow books
- View their borrowing history
- Access student dashboard

### Staff/Teachers
- All student permissions
- Preview books before borrowing
- Borrow books without restrictions
- Approve/reject student borrow requests
- Access staff dashboard with management tools

### Administrators
- All staff permissions
- Add and manage books
- Upload book files
- Access comprehensive statistics
- Manage all users and system settings
- Access Django admin panel

## 📊 Key Features Explained

### Interactive Statistics Dashboard
- Click on user analytics to see detailed user lists
- Expandable book categories showing all books
- Real-time download tracking with IP addresses
- Recent activity monitoring with status indicators

### Smart Borrowing System
- Automatic approval for staff and admin users
- Approval workflow for student requests
- Due date calculation and tracking
- Email notifications (configurable)

### File Management
- Secure file upload with type validation
- PDF preview functionality for authorized users
- Organized media storage with proper permissions
- Download tracking for analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For support and questions, please contact [a.wilsontelary@domain.com]

## 🙏 Acknowledgments

- Django framework for the robust backend
- Bootstrap for the responsive UI components
- FontAwesome for the beautiful icons
- The Django community for excellent documentation

---

**Academic Library Management System** - Empowering educational institutions with modern library management solutions.
