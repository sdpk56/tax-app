# Advanced Tax Calculator Application

A modern, trending tax calculator application built with Flask that provides comprehensive tax calculation, analysis, and comparison tools for Indian income tax regimes.

## Features 🚀

### Core Features
- ✅ **Advanced Tax Calculation**: Calculate income tax with precision including surcharge and health & education cess
- ✅ **Dual Tax Regime Support**: Compare Old vs New tax regimes and get recommendations
- ✅ **Deductions & Rebates**: Support for standard deductions, Section 80C, 80D, and custom rebates
- ✅ **Tax Slab Breakdown**: Detailed slab-wise tax breakdown visualization
- ✅ **Monthly Income Analysis**: Calculate monthly take-home and tax distribution
- ✅ **Effective Tax Rate**: Real-time effective tax rate calculation
- ✅ **Tax History Tracking**: Save and manage all tax calculations with pagination
- ✅ **Regime Comparison**: Side-by-side comparison with savings calculation
- ✅ **User Authentication**: Secure JWT-based authentication
- ✅ **Responsive UI**: Modern, gradient-based UI with Bootstrap 4

### Technical Highlights
- Type hints and comprehensive docstrings throughout
- RESTful API with detailed documentation
- Database persistence with SQLAlchemy ORM
- Comprehensive logging and error handling
- Production-ready with Docker and Docker Compose
- Kubernetes-ready with Helm charts

---

## Project Structure

```
tax-app/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── auth.py               # Authentication endpoints (signup/login)
│   ├── routes.py             # Tax calculation and history endpoints
│   ├── models.py             # Database models (User, TaxCalculation)
│   ├── database.py           # SQLAlchemy setup
│   ├── config.py             # Configuration management
│   ├── tax_calculator.py     # Core tax calculation logic
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Docker configuration
│
├── frontend/
│   ├── app.py                # Flask frontend application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   └── templates/
│       ├── base.html         # Base template with navigation
│       ├── index.html        # Home page
│       ├── login.html        # Login page
│       ├── register.html     # Registration page
│       ├── calculate_tax.html # Main tax calculator (modern UI)
│       └── tax_history.html  # Tax calculation history
│
├── helm/
│   └── tax-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/         # K8s manifests
│
├── docker-compose.yml        # Multi-container orchestration
└── API_DOCUMENTATION.md      # Comprehensive API docs
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (optional)
- PostgreSQL (or use Docker)

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd tax-app
```

2. **Set up environment variables**
```bash
# Create .env file
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

3. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start backend server
python app.py
```

4. **Frontend Setup** (in another terminal)
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start frontend server
python app.py
```

5. **Access the application**
- Frontend: http://localhost:8000
- Backend API: http://localhost:5000

### Docker Setup

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - Login and get JWT token

### Tax Calculation
- `POST /calculate-tax` - Calculate income tax with deductions
- `POST /compare-regimes` - Compare old vs new regime
- `GET /tax-slabs/{regime}?income=value` - Get slab breakdown

### Tax History
- `GET /tax-history` - Get user's calculation history (paginated)
- `DELETE /tax-history/{calc_id}` - Delete specific calculation

### User Info
- `GET /user-info` - Get current user information

**Full API documentation**: See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## Tax Calculation Features

### Supported Tax Regimes (FY 2024-25)

**Old Regime:**
- 0 - ₹2.5L: 0%
- ₹2.5L - ₹5L: 5%
- ₹5L - ₹10L: 20%
- ₹10L+: 30%

**New Regime:**
- 0 - ₹2.5L: 0%
- ₹2.5L - ₹5L: 5%
- ₹5L - ₹7.5L: 10%
- ₹7.5L - ₹10L: 15%
- ₹10L - ₹12.5L: 20%
- ₹12.5L - ₹15L: 25%
- ₹15L+: 30%

### Calculation Components
- **Base Tax**: Calculated from slabs
- **Surcharge**: 10% (₹1-10L), 15% (₹10-20L), 25% (₹20L+)
- **Health & Education Cess**: 4% on (base tax + surcharge)
- **Effective Tax Rate**: (Total Tax / Gross Income) × 100

### Example Calculation
```
Income: ₹10,00,000
Deductions: ₹1,50,000
Taxable Income: ₹8,50,000

Base Tax:
  - 0-2.5L @ 0% = ₹0
  - 2.5L-5L @ 5% = ₹12,500
  - 5L-8.5L @ 10-15% (new regime) = Varies

Surcharge: Calculated based on income level
Cess: 4% on (base tax + surcharge)

Total Tax: Includes all components
Take-home: Income - Total Tax
```

---

## Features Walkthrough

### 1. Tax Calculator
- Enter annual income
- Select tax regime (Old/New)
- Add optional deductions
- Get instant calculation with:
  - Total tax liability
  - Effective tax rate
  - Monthly take-home
  - Detailed slab breakdown

### 2. Regime Comparison
- Compare tax liability across both regimes
- See potential savings
- Get recommendation on which regime to choose
- Automatically identify the more beneficial regime

### 3. Tax History
- View all previous calculations
- Sorted by most recent first
- Pagination support (10 results per page)
- Delete old calculations
- Track tax planning over time

### 4. Slab Breakdown
- Visual representation of income distribution
- Tax contribution per slab
- Clear understanding of how income is taxed

---

## Database Models

### User Model
```python
- id (Primary Key)
- username (String, Unique)
- password (String, Hashed)
- created_at (DateTime)
- tax_calculations (Relationship)
```

### TaxCalculation Model
```python
- id (Primary Key)
- user_id (Foreign Key)
- gross_income (Float)
- deductions (Float)
- taxable_income (Float)
- base_tax (Float)
- surcharge (Float)
- health_education_cess (Float)
- total_tax (Float)
- effective_tax_rate (Float)
- regime (String)
- take_home_annual (Float)
- take_home_monthly (Float)
- created_at (DateTime)
```

---

## Configuration

### Environment Variables
```env
FLASK_ENV=production              # development or production
DB_USER=postgres                  # Database user
DB_PASSWORD=secure_password       # Database password
DB_NAME=taxdb                     # Database name
JWT_SECRET_KEY=secure_jwt_key     # JWT signing key
FLASK_SECRET_KEY=secure_key       # Flask session key
BACKEND_URL=http://backend:5000   # Backend URL
LOG_LEVEL=INFO                    # Logging level
```

### Configuration File (backend/config.py)
- Database connection pooling
- JWT token expiration (30 minutes)
- Logging configuration
- Flask environment settings

---

## Security Features

- ✅ Password hashing with pbkdf2:sha256
- ✅ JWT-based authentication
- ✅ CORS configuration for frontend access
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Session-based tracking
- ✅ Environment variable protection

---

## Deployment

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes (Helm)
```bash
helm install tax-app ./helm/tax-app/
helm upgrade tax-app ./helm/tax-app/
helm uninstall tax-app
```

### Environment-specific deployment
- Development: `docker-compose -f docker-compose.yml`
- Production: Add production-specific docker-compose override file

---

## Development

### Code Style
- PEP 8 compliant
- Type hints throughout
- Comprehensive docstrings
- Consistent naming conventions

### Testing (Future)
```bash
pytest tests/
pytest --cov=backend tests/
```

### Adding New Features
1. Update `tax_calculator.py` for logic changes
2. Add new route in `routes.py`
3. Create/update HTML templates in `frontend/templates/`
4. Update API documentation
5. Test thoroughly with different income levels

---

## Performance Optimization

- Database indexing on frequently queried fields
- Pagination for large datasets
- Efficient tax calculation algorithm (O(n) where n = number of slabs)
- Client-side caching (frontend)
- Minified CSS/JS (production)

---

## Known Limitations

- Tax rules are for FY 2024-25 (update required for new fiscal year)
- Single currency (INR only)
- No multi-user concurrent calculation limits
- No rate limiting on API (should be added for production)

---

## Future Enhancements

- [ ] Investment portfolio integration
- [ ] Tax saving recommendations
- [ ] Real-time tax rule updates
- [ ] Graphical tax analysis charts
- [ ] Export to PDF/Excel
- [ ] Multiple income sources support
- [ ] Advance tax payment scheduler
- [ ] Tax filing deadline reminders
- [ ] Mobile app (React Native)
- [ ] API rate limiting

---

## Support & Documentation

- **API Documentation**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Issues**: Report via GitHub Issues
- **Discussions**: GitHub Discussions

---

## License

MIT License - See LICENSE file for details

---

## Changelog

### Version 1.1.0 (Current)
- Added tax history tracking
- Implemented regime comparison
- Enhanced UI with modern gradient design
- Added surcharge and cess calculations
- Implemented pagination for history
- Added comprehensive API documentation

### Version 1.0.0
- Basic tax calculation
- User authentication
- Simple UI with Bootstrap

---

**Last Updated**: December 4, 2024
**Version**: 1.1.0
