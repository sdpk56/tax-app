# Troubleshooting Guide - Connection Errors

## Issue: "Expecting value: line 1 column 1 (char 0)"

This error occurs when the frontend cannot parse a JSON response from the backend, usually because:
1. Backend is not running
2. Backend is returning an error page (HTML) instead of JSON
3. Backend crashed and is not responding
4. Database connection failed

---

## Quick Fix Steps

### Step 1: Check if Backend is Running

**On Windows:**
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000
```

**On Mac/Linux:**
```bash
# Check if port 5000 is in use
lsof -i :5000
```

If nothing shows up, the backend is NOT running.

### Step 2: Start the Backend Properly

**Option A: Direct Python (Development)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Option B: Docker Compose (Recommended)**
```bash
cd tax-app
docker-compose up -d
docker-compose logs -f tax-backend
```

### Step 3: Verify Backend Health

Open in browser or terminal:
```bash
curl http://localhost:5000/health
# Should return: {"status":"healthy"}
```

If this fails, check the backend logs:
```bash
# Docker
docker-compose logs tax-backend

# Or if running directly
# Check terminal where you started app.py for error messages
```

### Step 4: Check Database Connection

The backend needs PostgreSQL. Verify:

**Option A: Using Docker Compose (Easiest)**
```bash
docker-compose up -d postgres
docker-compose logs postgres
```

**Option B: Local PostgreSQL**
```bash
# Windows
psql -U postgres -c "SELECT 1"

# Mac/Linux
psql -U postgres -c "SELECT 1"
```

If database doesn't exist:
```bash
createdb taxdb
```

### Step 5: Check Environment Variables

Backend needs these environment variables:

```bash
# Create .env file in project root
cat > .env << EOF
FLASK_ENV=development
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_NAME=taxdb
JWT_SECRET_KEY=your-super-secret-key
FLASK_SECRET_KEY=your-flask-secret-key
BACKEND_URL=http://localhost:5000
EOF
```

---

## Common Scenarios & Solutions

### Scenario 1: PostgreSQL Connection Error

**Error in logs:**
```
Error creating database tables: could not connect to server: 
No such file or directory
```

**Solution:**
```bash
# Start PostgreSQL
# Docker
docker-compose up -d postgres
docker-compose logs -f postgres

# Or if using local PostgreSQL, make sure it's running
# Windows: Services → PostgreSQL
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Scenario 2: Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Find and kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>

# Then start fresh
python app.py
```

### Scenario 3: BACKEND_URL Mismatch

**Error:** Frontend cannot reach backend

**Check:** Frontend `app.py` has correct BACKEND_URL:
```python
# Should be one of:
BACKEND_URL = "http://localhost:5000"      # Local dev
BACKEND_URL = "http://tax-backend:5000"    # Docker
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
```

### Scenario 4: Database Tables Not Created

**Error:** No "users" table found

**Solution:**
```bash
# Kill and restart backend (it will auto-create tables)
# Or manually initialize:

cd backend
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Tables created!')
"
```

---

## Step-by-Step Verification

Run these checks in order:

### 1. Backend Health
```bash
curl -v http://localhost:5000/health
# Expected: 200 OK with {"status":"healthy"}
```

### 2. Database
```bash
curl -v http://localhost:5000/login -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
# Expected: 401 with JSON error message (NOT HTML error page)
```

### 3. Frontend URL
```bash
curl -v http://localhost:8000/
# Expected: 200 OK with HTML homepage
```

### 4. Frontend Connection Test
Navigate to:
```
http://localhost:8000/register
```

Try registering with:
- Username: `testuser123`
- Password: `test@123`

Check console for errors (F12 → Console tab)

---

## Docker Specific Troubleshooting

### Check All Containers Running
```bash
docker-compose ps
# Should show 3 containers: postgres, backend, frontend
# All should have status "Up"
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f tax-backend
docker-compose logs -f postgres
```

### Restart Services
```bash
# Hard restart
docker-compose down
docker-compose up -d

# Check status
docker-compose ps
```

### Database Issues
```bash
# Recreate database container
docker-compose down postgres
docker volume rm tax-app_postgres_data
docker-compose up -d postgres
```

---

## Enable Debug Logging

### Backend

Edit `backend/app.py`:
```python
# Change from INFO to DEBUG
logging.basicConfig(level=logging.DEBUG, ...)
```

Restart backend to see detailed logs.

### Frontend

Open browser console (F12) and add to `calculate_tax.html`:
```javascript
// Add before axios calls
axios.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Error:', error);
    throw error;
  }
);
```

---

## Still Not Working?

### Checklist
- [ ] Backend running on port 5000
- [ ] Frontend running on port 8000
- [ ] PostgreSQL running and accessible
- [ ] `taxdb` database exists
- [ ] `.env` file has correct variables
- [ ] No port conflicts
- [ ] Backend logs show "Database tables checked/created"
- [ ] Health check returns 200 OK

### Get More Info

1. **Check backend console output** - Copy any error messages
2. **Check Docker logs** - `docker-compose logs tax-backend`
3. **Check browser console** - F12 → Console tab
4. **Check database connection** - Try `psql -U postgres -d taxdb`

### Last Resort

Full reset:
```bash
# Remove everything
docker-compose down -v

# Clean up
rm -rf backend/__pycache__
rm -rf frontend/__pycache__

# Start fresh
docker-compose up -d
docker-compose logs -f
```

---

## Quick Reference

| Issue | Solution |
|-------|----------|
| Backend not running | `python app.py` in backend folder |
| Port 5000 in use | Kill process: `lsof -i :5000 \| kill -9` |
| Database not found | Start PostgreSQL or use Docker |
| JSON parse error | Check backend logs for actual error |
| 404 on login | Check BACKEND_URL in frontend |
| CORS error | Backend CORS already configured, clear cache |
| Timeout | Backend taking too long, increase timeout |

---

**Still having issues?** Check the logs first, they usually tell you exactly what's wrong! 🔍

