#!/usr/bin/env python
"""
Database migration script to update schema to match models.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from flask import Flask
from config import Config
from database import db, init_db
from models import User, TaxCalculation

print("=" * 60)
print("DATABASE MIGRATION")
print("=" * 60)

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

with app.app_context():
    print("\n1. Dropping existing tables...")
    try:
        db.drop_all()
        print("   ✅ Tables dropped")
    except Exception as e:
        print(f"   ⚠️  Error dropping tables: {e}")
    
    print("\n2. Creating new tables with correct schema...")
    try:
        db.create_all()
        print("   ✅ Tables created successfully")
    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        sys.exit(1)
    
    print("\n3. Verifying tables...")
    try:
        user_count = User.query.count()
        tax_calc_count = TaxCalculation.query.count()
        print(f"   ✅ User table: {user_count} records")
        print(f"   ✅ TaxCalculation table: {tax_calc_count} records")
    except Exception as e:
        print(f"   ❌ Error verifying tables: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("MIGRATION COMPLETE")
print("=" * 60)
print("\n✅ Database is now ready. Try logging in again!")
