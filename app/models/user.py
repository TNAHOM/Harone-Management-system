from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    business_name = db.Column(db.String(100))
    role = db.Column(db.String(20))  # 'business', 'processor', 'admin', 'auditor'
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    requests = db.relationship('OnboardingRequest', backref='user', lazy=True, foreign_keys='OnboardingRequest.user_id')
    processed_requests = db.relationship('OnboardingRequest', backref='processor', lazy=True, foreign_keys='OnboardingRequest.processed_by') 