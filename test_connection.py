#!/usr/bin/env python
"""
Test script to verify database connection and application setup.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

print("=" * 60)
print("TAX-APP DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Checking Environment Variables...")
required_vars = [
    'DATABASE_URL',
    'JWT_SECRET_KEY',
    'FLASK_SECRET_KEY',
    'FLASK_ENV'
]

for var in required_vars:
    value = os.getenv(var, 'NOT SET')
    if value == 'NOT SET':
        print(f"   ❌ {var}: NOT SET")
    else:
        # Hide sensitive values
        if 'SECRET' in var or 'PASSWORD' in var:
            print(f"   ✅ {var}: {'*' * 20}")
        elif 'DATABASE_URL' in var:
            print(f"   ✅ {var}: {value[:50]}...")
        else:
            print(f"   ✅ {var}: {value}")

# Test 2: Check Python imports
print("\n2. Checking Python Dependencies...")
try:
    import flask
    print(f"   ✅ Flask: {flask.__version__}")
except ImportError as e:
    print(f"   ❌ Flask: {e}")

try:
    import sqlalchemy
    print(f"   ✅ SQLAlchemy: {sqlalchemy.__version__}")
except ImportError as e:
    print(f"   ❌ SQLAlchemy: {e}")

try:
    import flask_jwt_extended
    print(f"   ✅ Flask-JWT-Extended: Installed")
except ImportError as e:
    print(f"   ❌ Flask-JWT-Extended: {e}")

try:
    import flask_cors
    print(f"   ✅ Flask-CORS: Installed")
except ImportError as e:
    print(f"   ❌ Flask-CORS: {e}")

# Test 3: Test database connection
print("\n3. Testing Database Connection...")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from config import Config
    print(f"   ✅ Config loaded")
    print(f"      DATABASE_URL: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")
except Exception as e:
    print(f"   ❌ Config: {e}")
    sys.exit(1)

try:
    from flask import Flask
    from database import db, init_db
    
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        from models import User
        user_count = User.query.count()
        print(f"   ✅ Database Connection: Success")
        print(f"      Users in database: {user_count}")
except Exception as e:
    print(f"   ❌ Database Connection: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Check models
print("\n4. Checking Database Models...")
try:
    from models import User, TaxCalculation
    print(f"   ✅ User model: OK")
    print(f"   ✅ TaxCalculation model: OK")
except Exception as e:
    print(f"   ❌ Models: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 60)
print("\nIf any ❌ errors appear above, please fix them before running the app.")
