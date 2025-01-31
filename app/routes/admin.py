from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import User, OnboardingRequest
from app import db
from datetime import datetime
from functools import wraps
import secrets
import string
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

def admin_required(f):
    @wraps(f)  # This preserves the original function's name and metadata
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    email = request.form.get('email')
    role = request.form.get('role')
    
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return redirect(url_for('admin.users'))
    
    # Generate a random password for the internal user
    password = generate_random_password()
    
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        is_verified=True  # Internal users don't need email verification
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Display the generated password to the admin
        flash(f'User added successfully. Please provide these credentials to the user:', 'success')
        flash(f'Email: {email}', 'info')
        flash(f'Temporary Password: {password}', 'info')
        flash('Ask the user to change their password upon first login.', 'warning')
        
    except Exception as e:
        db.session.rollback()
        flash('Error creating user: ' + str(e), 'error')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/process_request/<int:request_id>', methods=['POST'])
@login_required
def process_request(request_id):
    if current_user.role not in ['processor', 'admin']:
        abort(403)
        
    onboarding_request = OnboardingRequest.query.get_or_404(request_id)
    status = request.form.get('status')
    comments = request.form.get('comments')
    
    onboarding_request.status = status
    onboarding_request.processed_by = current_user.id
    onboarding_request.processed_at = datetime.utcnow()
    onboarding_request.comments = comments
    
    db.session.commit()
    
    flash('Request processed successfully')
    return redirect(url_for('main.dashboard')) 