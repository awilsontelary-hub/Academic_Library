# 🐍 PythonAnywhere Django Deployment Guide - Academic Library

## 🎯 **Complete PythonAnywhere Deployment Process**

### **Prerequisites**
- PythonAnywhere account (free or paid)
- Your Django project files ready
- Basic understanding of Python/Django

---

## 📦 **Step 1: Upload Your Project**

### **Option A: Git Clone (Recommended)**
1. **Open PythonAnywhere Console** (Bash)
2. **Clone your repository**:
   ```bash
   git clone https://github.com/yourusername/Academic_Library.git
   cd Academic_Library
   ```

### **Option B: File Upload**
1. **Go to Files tab** in PythonAnywhere
2. **Upload your project ZIP file**
3. **Extract to home directory**

---

## 🐍 **Step 2: Set Up Virtual Environment**

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 academic_library

# Activate virtual environment
workon academic_library

# Install dependencies
pip install -r requirements.txt
```

---

## 🔧 **Step 3: Configure Environment Variables**

1. **Copy environment template**:
   ```bash
   cp .env.pythonanywhere .env
   ```

2. **Edit `.env` file** with your details:
   ```
   DEBUG=False
   SECRET_KEY=your-secure-secret-key-here
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   ```

3. **Generate secure secret key**:
   ```python
   python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"
   ```

---

## 🗄️ **Step 4: Database Setup (Choose One)**

### **Option A: SQLite (Easiest)**
- Keep `USE_MYSQL=False` in `.env`
- Database will be created automatically
- **Good for**: Development, small projects

### **Option B: MySQL (Recommended for Production)**

1. **Create MySQL Database**:
   - Go to **PythonAnywhere Dashboard → Databases**
   - Create database: `yourusername$library`
   - Note the connection details

2. **Update `.env` file**:
   ```
   USE_MYSQL=True
   DB_NAME=yourusername$library
   DB_USER=yourusername
   DB_PASSWORD=your_mysql_password
   DB_HOST=yourusername.mysql.pythonanywhere-services.com
   DB_PORT=3306
   ```

---

## 🚀 **Step 5: Initialize Django Application**

```bash
# Run the automated setup script
python pythonanywhere_setup.py

# OR run commands manually:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 🌐 **Step 6: Configure Web App**

### **6.1 Create Web App**
1. **Go to Web tab** in PythonAnywhere
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**

### **6.2 Configure WSGI File**
1. **Edit WSGI file** (in Web tab)
2. **Replace content** with `pythonanywhere_wsgi.py`
3. **Update the path**:
   ```python
   project_home = '/home/yourusername/Academic_Library'
   ```

### **6.3 Set Virtual Environment**
1. **In Web tab, find "Virtualenv" section**
2. **Enter path**: `/home/yourusername/.virtualenvs/academic_library`

### **6.4 Configure Static Files**
1. **In Web tab, Static files section**
2. **Add mapping**:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/Academic_Library/staticfiles/`

3. **Add media files mapping**:
   - **URL**: `/media/`
   - **Directory**: `/home/yourusername/Academic_Library/media/`

---

## 🔄 **Step 7: Go Live**

1. **Click "Reload" button** in Web tab
2. **Visit your site**: `https://yourusername.pythonanywhere.com`
3. **Test functionality**:
   - Homepage loads ✅
   - User registration works ✅
   - Admin panel accessible ✅
   - File uploads work ✅

---

## ✅ **Step 8: Post-Deployment Testing**

### **8.1 Test Core Features**
- **Homepage**: Clean layout, navigation works
- **User Registration**: Test with sample IDs (INST001-INST005)
- **Admin Panel**: Access at `/admin`
- **Book Management**: Upload, browse, search
- **User Approval**: Admin approval workflow

### **8.2 Test Sample Data**
Available institutional IDs for testing:
- `INST001` - Student (Computer Science)
- `INST002` - Student (Engineering)  
- `INST003` - Staff (Library Sciences)
- `INST004` - Student (Mathematics)
- `INST005` - Staff (IT Support)

---

## 🛠️ **Maintenance & Updates**

### **Regular Tasks**
1. **Monitor resource usage** (CPU seconds, disk space)
2. **Check error logs** in PythonAnywhere
3. **Backup database** regularly
4. **Update dependencies** as needed

### **For Updates**
```bash
# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Reload web app
# (Use reload button in Web tab)
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

**🚨 500 Internal Server Error**:
- Check error logs in Web tab
- Verify WSGI file paths
- Ensure virtual environment is correct

**🚨 Static Files Not Loading**:
- Run `python manage.py collectstatic`
- Check static files mapping in Web tab
- Verify file permissions

**🚨 Database Connection Errors**:
- Verify MySQL credentials in `.env`
- Check database exists in Databases tab
- Test with SQLite first

**🚨 Import Errors**:
- Ensure virtual environment is activated
- Check all dependencies installed
- Verify Python path in WSGI file

### **Getting Help**
- **PythonAnywhere Help**: Use help chat in dashboard
- **Django Documentation**: https://docs.djangoproject.com/
- **Error Logs**: Available in Web tab

---

## 🎯 **PythonAnywhere Account Limits**

### **Free Account**
- ✅ **One web app**
- ✅ **512MB disk space**
- ✅ **100 seconds CPU/day**
- ✅ **SQLite databases**
- ❌ No custom domains
- ❌ No SSH access

### **Paid Accounts**
- ✅ **Multiple web apps**
- ✅ **More disk space & CPU**
- ✅ **MySQL databases**
- ✅ **Custom domains**
- ✅ **SSH access**
- ✅ **Always-on tasks**

---

## 📞 **Support Resources**

- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **Django Documentation**: https://docs.djangoproject.com/
- **Academic Library Issues**: Check your repository issues

---

**Your Academic Library Django application is now ready for PythonAnywhere deployment!** 🎉

**Live URL**: `https://yourusername.pythonanywhere.com`  
**Admin Panel**: `https://yourusername.pythonanywhere.com/admin`