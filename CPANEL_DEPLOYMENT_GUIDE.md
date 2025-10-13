# 📋 cPanel Django Deployment Guide - Academic Library

## 🎯 **Complete cPanel Deployment Process**

### **Prerequisites**
- cPanel hosting account with Python 3.9+ support
- File Manager or FTP access
- Domain configured in cPanel

## 📦 **Step 1: Prepare Deployment Package**

### 1.1 Create Deployment Folder
Your project is now ready for cPanel. The structure should be:
```
Academic_Library/
├── apps/
├── online_library/
├── static/
├── media/
├── manage.py
├── passenger_wsgi.py  ✅ cPanel WSGI file
├── requirements.txt   ✅ Updated for cPanel
├── .env.cpanel       ✅ Environment template
└── db.sqlite3        (will be created)
```

### 1.2 Upload to cPanel
1. **Zip your project folder**
2. **Login to cPanel → File Manager**
3. **Navigate to your domain folder** (e.g., `public_html` or `yourdomain.com`)
4. **Upload and extract** the ZIP file

## 🐍 **Step 2: Set Up Python Application**

### 2.1 Create Python App in cPanel
1. **Find "Python App"** in cPanel (or "Setup Python App")
2. **Click "Create Application"**:
   - **Python Version**: 3.9 or higher
   - **Application Root**: `/Academic_Library`
   - **Application URL**: Leave blank (for root domain) or set subdirectory
   - **Application Startup File**: `passenger_wsgi.py`

### 2.2 Configure WSGI File
Edit `passenger_wsgi.py` with your actual cPanel paths:
```python
# Update this line with your actual path
project_home = '/home/yourusername/yourdomain.com/Academic_Library'
```

## 🔧 **Step 3: Environment Configuration**

### 3.1 Set Up Environment Variables
1. **Copy `.env.cpanel` to `.env`**
2. **Update with your details**:
```
DEBUG=False
SECRET_KEY=generate-a-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
USE_MYSQL=False  # Start with SQLite, change to True for MySQL
```

### 3.2 Install Dependencies
In cPanel Python App terminal or SSH:
```bash
pip install -r requirements.txt
```

## 🗄️ **Step 4: Database Setup (Choose One)**

### Option A: SQLite (Recommended for Start)
- ✅ **No additional setup required**
- ✅ **Automatically created**
- ✅ **Perfect for small to medium sites**

Keep in `.env`:
```
USE_MYSQL=False
```

### Option B: MySQL (For Larger Sites)
1. **Create MySQL Database in cPanel**:
   - Go to "MySQL Databases"
   - Create database: `yourusername_library`
   - Create user: `yourusername_libuser`
   - Assign all privileges

2. **Update `.env` file**:
```
USE_MYSQL=True
DB_NAME=yourusername_library
DB_USER=yourusername_libuser
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

## 🚀 **Step 5: Initialize Django Application**

### 5.1 Run Django Commands
In cPanel Python App terminal:
```bash
# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create admin user
python manage.py createsuperuser
```

### 5.2 Initialize Sample Data
```bash
python manage.py shell
```
Then run:
```python
# Create sample institutional IDs
from create_sample_ids import create_sample_ids
create_sample_ids()
exit()
```

## 📁 **Step 6: Configure File Permissions**

### Set Proper Permissions:
- **Python files (.py)**: 644
- **Directories**: 755
- **Media upload directory**: 755
- **Database file**: 644

## 🔄 **Step 7: Activate Application**

### 7.1 Start Application
1. **In cPanel Python App**: Click "Restart"
2. **Set domain mapping** if needed
3. **Verify startup file**: `passenger_wsgi.py`

### 7.2 Test Deployment
1. **Visit your domain** - Should show Academic Library homepage
2. **Access admin panel** - `yourdomain.com/admin`
3. **Test user registration** - Use institutional IDs: INST001-INST005
4. **Test file uploads** - Upload sample documents

## 🛡️ **Step 8: Security & Production Settings**

### 8.1 Security Checklist
- [x] **SECRET_KEY**: Generated and secure
- [x] **DEBUG=False**: Production mode enabled  
- [x] **ALLOWED_HOSTS**: Only your actual domains
- [x] **File permissions**: Properly configured

### 8.2 Generate Secure Secret Key
```python
import secrets
import string
alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
print(secret_key)
```

## 🔍 **Step 9: Testing & Verification**

### 9.1 Functionality Tests
- ✅ **Homepage loads correctly**
- ✅ **User registration with institutional verification**
- ✅ **Admin approval workflow**
- ✅ **Book upload and management**
- ✅ **Search and browsing**
- ✅ **Static files (CSS/JS) loading**

### 9.2 Admin Features
- ✅ **Admin panel access**
- ✅ **User management**
- ✅ **Institutional ID management**
- ✅ **Book categorization**

## 🛠️ **Troubleshooting**

### Common Issues & Solutions:

**500 Internal Server Error**:
- Check cPanel Error Logs
- Verify `passenger_wsgi.py` paths
- Ensure all dependencies installed

**Static Files Not Loading**:
- Run `python manage.py collectstatic`
- Check file permissions
- Verify STATIC_ROOT setting

**Database Connection Errors**:
- Verify MySQL credentials
- Check database user privileges
- Test SQLite as fallback

**Permission Denied Errors**:
- Set directories to 755
- Set files to 644
- Check media upload permissions

### Error Logs Location:
- **cPanel → Error Logs**
- **File path**: `/home/username/logs/`

## 🔄 **Maintenance & Updates**

### Regular Tasks:
1. **Monitor resource usage** in cPanel
2. **Check error logs** periodically
3. **Backup database** regularly
4. **Update dependencies** as needed

### For Updates:
1. Upload new files via File Manager
2. Run migrations: `python manage.py migrate`
3. Collect static files: `python manage.py collectstatic`
4. Restart Python application

## 📞 **Support Information**

If you encounter issues:
1. **Check cPanel documentation** for your hosting provider
2. **Contact hosting support** for Python app configuration
3. **Review Django deployment docs** for additional guidance

**Your Academic Library is now ready for cPanel deployment!** 🎉