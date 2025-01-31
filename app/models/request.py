from datetime import datetime
from app import db

class OnboardingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    business_type = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    business_address = db.Column(db.Text, nullable=False)
    business_license = db.Column(db.String(255))
    tax_id = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    processed_at = db.Column(db.DateTime)
    comments = db.Column(db.Text) 