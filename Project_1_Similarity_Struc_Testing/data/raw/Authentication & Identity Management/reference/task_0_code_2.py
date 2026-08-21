from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from itsdangerous import URLSafeSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

db = SQLAlchemy(app)
mail = Mail(app)

oauth = OAuth(app)

okta = oauth.register(
    name='okta',
    client_id='your_okta_client_id',
    client_secret='your_okta_client_secret',
    authorize_url='https://your_okta_domain.com/oauth2/authorize',
    authorize_params=None,
    access_token_url='https://your_okta_domain.com/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    refresh_token_params=None,
    redirect_uri='http://localhost:5000/callback',
    client_kwargs={'scope': 'openid profile email'},
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, confirmed=False):
        self.email = email
        self.password = generate_password_hash(password)
        self.confirmed = confirmed

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit() # <--- FIXED: Added commit so the user is saved before the email goes out

    token = generate_confirmation_token(email)
    confirmation_link = f'http://localhost:5000/confirm_email/{token}'
    send_confirmation_email(email, confirmation_link)

    return jsonify({'message': 'User registered successfully. Please check your email to confirm account'})

def generate_confirmation_token(email):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirmation-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        # Note: URLSafeSerializer doesn't natively support max_age inside loads unless using URLSafeTimedSerializer
        email = serializer.loads(token, salt='email-confirmation-salt')
    except:
        return False
    return email

def send_confirmation_email(email, confirmation_link):
    msg = Message('Confirm Your Email', sender='your_email@example.com', recipients=[email])
    msg.body = f'Please click the following link to confirm your email: {confirmation_link}'
    mail.send(msg)

@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    email = confirm_token(token)
    
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            user.confirmed = True
            db.session.commit()
            return 'Email confirmed successfully'
    return 'Email confirmation link is invalid or has expired'


# --- FIXED: Moved execution logic outside the function scope ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Safely build tables within application context
    app.run(debug=True)