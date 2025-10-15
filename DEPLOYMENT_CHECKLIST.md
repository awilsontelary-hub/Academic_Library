# Quick PythonAnywhere Deployment Checklist

## Pre-Deployment ✅
- [ ] PythonAnywhere account created
- [ ] Project files ready (all cleaned up)
- [ ] Requirements.txt up to date
- [ ] Secret key generated

## Upload & Setup ✅
- [ ] Project uploaded/cloned to PythonAnywhere
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables configured (`.env` file)

## Database Configuration ✅
**SQLite (Simple)**:
- [ ] Set `USE_MYSQL=False` in `.env`

**MySQL (Production)**:
- [ ] MySQL database created in PythonAnywhere
- [ ] Database credentials added to `.env`
- [ ] Set `USE_MYSQL=True` in `.env`

## Django Setup ✅
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Sample institutional IDs created (optional)

## Web App Configuration ✅
- [ ] Web app created (Manual configuration, Python 3.10)
- [ ] WSGI file configured (`pythonanywhere_wsgi.py` content)
- [ ] Virtual environment path set
- [ ] Static files mapping configured (`/static/` → `/staticfiles/`)
- [ ] Media files mapping configured (`/media/` → `/media/`)

## Go Live & Test ✅
- [ ] Web app reloaded
- [ ] Homepage loads correctly
- [ ] User registration works (test with INST001)
- [ ] Admin panel accessible
- [ ] File uploads working
- [ ] Navigation and footer correct

## Post-Deployment ✅
- [ ] Error logs checked
- [ ] Performance tested
- [ ] Backup plan established
- [ ] Update procedure documented

---

**🎯 Your Academic Library is ready for PythonAnywhere hosting!**

**Quick Commands:**
```bash
# Activate environment
workon academic_library

# Run setup script
python pythonanywhere_setup.py

# Manual commands if needed
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

**Test URLs:**
- **Main Site**: `https://yourusername.pythonanywhere.com`
- **Admin**: `https://yourusername.pythonanywhere.com/admin`

**Sample Test IDs**: INST001, INST002, INST003, INST004, INST005