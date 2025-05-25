import os
from datetime import timedelta # Import timedelta

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:yourpassword@taxdb/taxdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Recommended to set to False to save resources

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-very-secure-secret-key")
    # Set a default token expiration time (e.g., 30 minutes)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    # You can also set a refresh token expiration if you implement refresh tokens
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # Flask Environment (for debugging and production settings)
    FLASK_ENV = os.getenv("FLASK_ENV", "development") # 'development' or 'production'
    DEBUG = (FLASK_ENV == 'development')

    # Logging Configuration (optional, can be more detailed)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")