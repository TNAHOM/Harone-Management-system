from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, current_app, jsonify, send_file
from flask_login import login_required, current_user
from app.models import OnboardingRequest, User
from sqlalchemy import func
from datetime import datetime
from app import db
from flask_wtf import FlaskForm
import os

main_bp = Blueprint('main', __name__)

def save_file(file, prefix):
    _, ext = os.path.splitext(file.filename)
    filename = f"{prefix}_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
    upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])

    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)
    return filename

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'business':
        requests = OnboardingRequest.query.filter_by(user_id=current_user.id).all()
        form = FlaskForm()
        return render_template('business_dashboard.html', requests=requests, form=form)
    elif current_user.role in ['processor', 'admin', 'auditor']:
        requests = OnboardingRequest.query.all()
        
        # Calculate statistics
        stats = {
            'pending_count': OnboardingRequest.query.filter_by(status='pending').count(),
            'business_count': User.query.filter_by(role='business').count(),
            'avg_processing_time': '0 days'
        }
        
        # Calculate average processing timeh
        completed_requests = OnboardingRequest.query.filter(
            OnboardingRequest.status.in_(['approved', 'rejected']),
            OnboardingRequest.processed_at.isnot(None)
        ).all()
        
        if completed_requests:
            total_time = sum(
                (request.processed_at - request.submitted_at).total_seconds()
                for request in completed_requests
            )
            avg_time = total_time / len(completed_requests)
            avg_days = round(avg_time / (24 * 3600), 1)
            stats['avg_processing_time'] = f"{avg_days} days"
        
        return render_template('crm_dashboard.html', requests=requests, stats=stats)

@main_bp.route('/request/<int:request_id>')
@login_required
def view_request(request_id):
    onboarding_request = OnboardingRequest.query.get_or_404(request_id)
    if current_user.role == 'business' and onboarding_request.user_id != current_user.id:
        abort(403)
    

    if request.headers.get('Accept') == 'application/json':
        return jsonify({
            'id': onboarding_request.id,
            'status': onboarding_request.status,
            'submitted_at': onboarding_request.submitted_at.isoformat(),
            'processed_at': onboarding_request.processed_at.isoformat() if onboarding_request.processed_at else None,
            'business_name': onboarding_request.business_name,
            'business_type': onboarding_request.business_type,
            'contact_number': onboarding_request.contact_number,
            'business_address': onboarding_request.business_address,
            'business_license': onboarding_request.business_license,
            'tax_id': onboarding_request.tax_id,
            'comments': onboarding_request.comments
        })
    
    return render_template('request_details.html', request=onboarding_request)

@main_bp.route('/submit_request', methods=['POST'])
@login_required
def submit_request():
    if current_user.role != 'business':
        abort(403)
    
    # validations
    required_fields = ['business_name', 'business_type', 'contact_number', 'business_address']
    for field in required_fields:
        if not request.form.get(field):
            flash(f'{field.replace("_", " ").title()} is required.', 'error')
            return redirect(url_for('main.dashboard'))
    

    business_license_file = request.files.get('business_license')
    tax_id_file = request.files.get('tax_id')
    
    if not business_license_file or not tax_id_file:
        flash('Please upload all required documents.', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        business_license_filename = save_file(business_license_file, 'license')
        tax_id_filename = save_file(tax_id_file, 'tax')
        
        # Creating ' onboarding request
        new_request = OnboardingRequest(
            user_id=current_user.id,
            business_name=request.form['business_name'],
            business_type=request.form['business_type'],
            contact_number=request.form['contact_number'],
            business_address=request.form['business_address'],
            business_license=business_license_filename,
            tax_id=tax_id_filename,
            status='pending',
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        flash('Your onboarding request has been submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        print("Error creating request:", str(e))
        db.session.rollback()
        flash('An error occurred while submitting your request. Please try again.', 'error')
        return redirect(url_for('main.dashboard'))

@main_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    try:
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(upload_folder, filename)
        
        if not os.path.exists(filepath):
            flash('File not found.', 'error')
            return redirect(url_for('main.dashboard'))
        
        _, ext = os.path.splitext(filename)
        mime_types = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png'
        }
        mime_type = mime_types.get(ext.lower(), 'application/octet-stream')
        
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=False
        )
    except Exception as e:
        print("Error downloading file:", str(e))
        flash('Error accessing file.', 'error')
        return redirect(url_for('main.dashboard')) 