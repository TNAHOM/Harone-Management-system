from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.utils.email import send_verification_email, verify_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        business_name = request.form.get('business_name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.signup'))
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            business_name=business_name,
            role='business'
        )
        db.session.add(user)
        db.session.commit()
        
        send_verification_email(user)
        
        flash('Please check your email to verify your account')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_verified and user.role == 'business':
                flash('Please verify your email first')
                return redirect(url_for('auth.login'))
            
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid email or password')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    email = verify_token(token)
    if email is None:
        flash('Invalid or expired verification link')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User not found')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('Email already verified')
        return redirect(url_for('auth.login'))
    
    user.is_verified = True
    db.session.commit()
    flash('Your email has been verified. You can now log in.')
    return redirect(url_for('auth.login')) 