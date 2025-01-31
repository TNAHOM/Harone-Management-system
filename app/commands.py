import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app.models import User
from app import db

@click.command('create-admin')
@click.option('--email', prompt='Admin email', help='Email address for the admin user')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the admin user')
@with_appcontext
def create_admin(email, password):
    """Create an admin user."""
    try:
        admin = User(
            email=email,
            password_hash=generate_password_hash(password),
            role='admin',
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        click.echo(f'Admin user {email} created successfully!')
    except Exception as e:
        click.echo(f'Failed to create admin user: {e}') 