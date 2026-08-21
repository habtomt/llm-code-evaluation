from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.jose import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Boolean, default=False)

# Best practice for modern Flask-SQLAlchemy: run inside application context
with app.app_context():
    db.create_all()

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='your_auth0_client_id',
    client_secret='your_auth0_client_secret',
    api_base_url='https://your_auth0_domain',
    access_token_url='https://your_auth0_domain/oauth/token',
    authorize_url='https://your_auth0_domain/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },  # <--- FIXED: Closed the dictionary and parenthesis here
)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': # Changed to POST to correctly handle form submission
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        token = serializer.dumps(email, salt='email-confirm')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        msg = Message('Confirm Email', sender='sender_email', recipients=[email])
        msg.body = f'Click the link to confirm your email: {confirm_url}'
        mail.send(msg)
        return 'Please check your email to confirm your email address.'
    
    return 'Render your signup HTML form here for GET requests.' # Added a fallback return for GET

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except:
        return 'The confirmation link is invalid or has expired.'
    
    user = User.query.filter_by(email=email).first_or_404()
    user.verified = True
    db.session.commit()
    return 'You have confirmed your email. You can now login.'