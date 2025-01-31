from flask import current_app, url_for
from app import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

def get_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification')

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification', max_age=expiration)
        return email
    except:
        return None

def send_verification_email(user):
    token = get_token(user.email)
    msg = Message('Verify Your Email',
                  recipients=[user.email])
    msg.body = f'''To verify your email, visit the following link:
{url_for('auth.verify_email', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)

def send_status_update_email(request):
    msg = Message('Onboarding Request Status Update',
                  recipients=[request.user.email])
    msg.body = f'''Your onboarding request status has been updated to: {request.status.upper()}

Comments: {request.comments if request.comments else 'No comments provided'}

Please log in to your account to view more details.
'''
    mail.send(msg) 