from database import db
from datetime import datetime

class User(db.Model):
    """User model for authentication and account management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tax_calculations = db.relationship('TaxCalculation', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        """String representation of User object."""
        return f'<User {self.username}>'


class TaxCalculation(db.Model):
    """Model to store user's tax calculation history."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gross_income = db.Column(db.Float, nullable=False)
    deductions = db.Column(db.Float, default=0)
    taxable_income = db.Column(db.Float, nullable=False)
    base_tax = db.Column(db.Float, nullable=False)
    surcharge = db.Column(db.Float, default=0)
    health_education_cess = db.Column(db.Float, default=0)
    total_tax = db.Column(db.Float, nullable=False)
    effective_tax_rate = db.Column(db.Float, default=0)
    regime = db.Column(db.String(20), nullable=False)  # 'old' or 'new'
    take_home_annual = db.Column(db.Float, nullable=False)
    take_home_monthly = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation of TaxCalculation object."""
        return f'<TaxCalculation user_id={self.user_id} income={self.gross_income}>'

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'gross_income': self.gross_income,
            'deductions': self.deductions,
            'taxable_income': self.taxable_income,
            'base_tax': self.base_tax,
            'surcharge': self.surcharge,
            'health_education_cess': self.health_education_cess,
            'total_tax': self.total_tax,
            'effective_tax_rate': self.effective_tax_rate,
            'regime': self.regime,
            'take_home_annual': self.take_home_annual,
            'take_home_monthly': self.take_home_monthly,
            'created_at': self.created_at.isoformat()
        }