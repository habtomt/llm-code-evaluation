from flask import Flask ,redirect ,url_for ,session ,render_template
from flask_dance .contrib .google import make_google_blueprint ,google
from flask_dance .consumer import OAuth2ConsumerBlueprint
from flask_dance .consumer .storage .sqla import SQLAlchemyStorage
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager ,UserMixin ,login_user ,logout_user ,login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms .validators import DataRequired
from werkzeug .security import generate_password_hash ,check_password_hash
import os

app =Flask (__name__ )

app .config ['SECRET_KEY']=os .urandom (32 )

app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app .config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db =SQLAlchemy (app )

login_manager =LoginManager ()
login_manager .init_app (app )

class User (UserMixin ,db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    name =db .Column (db .String (64 ))
    email =db .Column (db .String (120 ),unique =True )
    password =db .Column (db .String (128 ))
    authenticated =db .Column (db .Boolean ,default =False )

class RegistrationForm (FlaskForm ):
    email =StringField ('Email',validators =[DataRequired ()])
    password =StringField ('Password',validators =[DataRequired ()])
    name =StringField ('Name',validators =[DataRequired ()])

class LoginForm (FlaskForm ):
    email =StringField ('Email',validators =[DataRequired ()])
    password =StringField ('Password',validators =[DataRequired ()])

google_blueprint =make_google_blueprint (
client_id ="YOUR_CLIENT_ID",
client_secret ="YOUR_CLIENT_SECRET",
storage =SQLAlchemyStorage (User ,db .session ,user_key ='email')
)

app .register_blueprint (google_blueprint ,url_prefix ="/login")

@app .route ('/')
def index ():
    return render_template ('index.html')

@app .route ('/login/google')
def login ():
    return google .login ()

@app .route ('/login/google/authorized')
def authorized ():
    google .login ()
    resp =google .get ("/oauth2/v2/userinfo")
    assert resp .ok ,resp .text

    user_info =resp .json ()
    user_email =user_info ["email"]
    user_name =user_info .get ("name","Anonymous")

    user =User .query .filter_by (email =user_email ).first ()
    if user :

        login_user (user )
        return redirect (url_for ('after_login'))
    else :

        new_user =User (email =user_email ,name =user_name )
        new_user .password =generate_password_hash (new_user .password )
        db .session .add (new_user )
        db .session .commit ()
        login_user (new_user )
        return redirect (url_for ('after_login'))

@app .route ('/after_login')
@login_required
def after_login ():
    return f"Logged in as: {current_user.email} (Name: {current_user.name})"

@app .route ('/logout')
@login_required
def logout ():
    logout_user ()
    return redirect (url_for ('index'))

@login_manager .user_loader
def load_user (user_id ):
    return User .query .get (int (user_id ))

if __name__ =='__main__':
    app .run (debug =True )