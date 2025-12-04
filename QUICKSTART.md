# Quick Start Guide

## 🚀 Running the Tax Calculator in 5 Minutes

### Option 1: Docker Compose (Recommended)

```bash
# 1. Navigate to project directory
cd tax-app

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be ready (check logs)
docker-compose logs -f

# 4. Access the application
# Frontend: http://localhost:8000
# Backend: http://localhost:5000

# 5. Stop services
docker-compose down
```

### Option 2: Local Development

#### Backend Setup
```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Set up database (use PostgreSQL or SQLite for dev)
# Update DATABASE_URL in .env or config.py

# 3. Run backend
python app.py
# Server runs on http://localhost:5000
```

#### Frontend Setup (new terminal)
```bash
# 1. Install frontend dependencies
cd frontend
pip install -r requirements.txt

# 2. Run frontend
python app.py
# Server runs on http://localhost:8000
```

---

## 📝 First Steps

### 1. Register Account
1. Go to http://localhost:8000
2. Click "Register"
3. Enter username and password
4. Click "Register"

### 2. Login
1. Click "Login"
2. Enter your credentials
3. Click "Login"

### 3. Calculate Tax
1. Click "Calculate Tax" from navigation
2. Enter your annual income (e.g., 1000000)
3. Select tax regime (Old or New)
4. **Optional**: Add deductions (e.g., 80C = 150000)
5. Click "Calculate Tax"

### Result Shows:
- ✅ Total tax liability
- ✅ Effective tax rate
- ✅ Monthly and annual take-home
- ✅ Slab-wise breakdown
- ✅ Surcharge and cess details

### 4. Compare Regimes
1. Click "Compare Regimes" button
2. See side-by-side comparison
3. View potential savings
4. Get recommendation on which regime to use

### 5. View History
1. Click "History" in navigation
2. See all your previous calculations
3. Delete calculations if needed
4. Use pagination to browse

---

## 🔐 Sample Credentials for Testing

**Note**: Create your own account via Registration page

```
Username: testuser
Password: testpass123
```

---

## 💡 Example Scenarios

### Scenario 1: Salaried Employee
```
Annual Income: ₹12,00,000
80C Deductions: ₹1,50,000
80D Insurance: ₹50,000
Total Deductions: ₹2,00,000

Old Regime: Tax = ₹2,45,000
New Regime: Tax = ₹2,68,800

Old Regime Saves: ₹23,800 per year
Recommendation: Choose Old Regime
```

### Scenario 2: High Income Individual
```
Annual Income: ₹50,00,000
Deductions: ₹2,00,000

Base Tax: ₹12,50,000
Surcharge (25%): ₹3,12,500
Cess (4%): ₹6,25,000

Total Tax: ₹22,18,500
Effective Rate: 44.37%
Monthly Take-Home: ₹2,31,791.67
```

### Scenario 3: Budget Calculation
```
Want to keep ₹10,00,000 after tax?

Old Regime with ₹1,50,000 deductions:
Required Income: ~₹11,50,000

New Regime without deductions:
Required Income: ~₹11,45,000
```

---

## 🛠️ Environment Setup

### Create .env file
```bash
# For Docker
echo "FLASK_ENV=development
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_NAME=taxdb
JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
FLASK_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
BACKEND_URL=http://tax-backend:5000" > .env
```

### For Local Development
```bash
# Backend/.env
export DATABASE_URL="postgresql://postgres:password@localhost/taxdb"
export JWT_SECRET_KEY="your-secret-key"
export FLASK_ENV="development"
```

---

## 📱 API Usage Examples

### Calculate Tax via API
```bash
# Get token first
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

# Use token to calculate tax
curl -X POST http://localhost:5000/calculate-tax \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "income": 1000000,
    "regime": "new",
    "deductions": 150000
  }'
```

### Get Tax History
```bash
curl -X GET "http://localhost:5000/tax-history?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Compare Regimes
```bash
curl -X POST http://localhost:5000/compare-regimes \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "income": 1000000,
    "deductions": 150000
  }'
```

---

## 🐛 Troubleshooting

### Issue: Can't connect to backend
**Solution**: 
- Check if backend is running: `http://localhost:5000/user-info`
- Verify `BACKEND_URL` in frontend environment
- Check Docker logs: `docker-compose logs tax-backend`

### Issue: Database connection error
**Solution**:
- Verify PostgreSQL is running
- Check DATABASE_URL configuration
- Ensure database exists: `createdb taxdb`

### Issue: Login not working
**Solution**:
- Clear browser cookies/session
- Check if user exists
- Verify JWT_SECRET_KEY is set

### Issue: Calculations not saving
**Solution**:
- Check database logs
- Verify user_id is correct
- Check disk space on database

---

## 📚 More Resources

- **Full API Docs**: See [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
- **Features List**: See [FEATURES.md](../FEATURES.md)
- **Tax Rules**: Current FY 2024-25 rates (update yearly)

---

## 🎯 Next Steps

1. **Explore the Calculator**
   - Try different income levels
   - Compare both tax regimes
   - Save calculations for reference

2. **Read Documentation**
   - API_DOCUMENTATION.md for backend integration
   - FEATURES.md for detailed feature list

3. **Customize**
   - Update tax slabs in `backend/tax_calculator.py`
   - Modify UI in `frontend/templates/`
   - Add new deduction types in routes

4. **Deploy**
   - Use Docker Compose for local/staging
   - Use Helm for Kubernetes deployment
   - Configure for your environment

---

## ❓ FAQ

**Q: How accurate are the calculations?**
A: Calculations follow official FY 2024-25 tax slabs and rules.

**Q: Can I use this for official tax filing?**
A: Use for estimation only. Consult a CA for official filing.

**Q: Is my data secure?**
A: Yes, passwords are hashed and JWT-secured. Self-hosted option available.

**Q: How do I update tax rules for new fiscal year?**
A: Update `tax_slabs` dictionary in `backend/tax_calculator.py`

**Q: Can I export results?**
A: Currently supports JSON via API. PDF export coming soon.

---

**Happy Tax Calculating! 📊💰**
