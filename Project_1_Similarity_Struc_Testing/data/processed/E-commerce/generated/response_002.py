from flask import Flask ,render_template ,request ,redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug .security import generate_password_hash ,check_password_hash
import stripe

app =Flask (__name__ )
app .config ['SECRET_KEY']='YOUR_SECRET_KEY'
app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///checkout.db'
db =SQLAlchemy (app )

class User (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    name =db .Column (db .String (100 ),nullable =False )
    address =db .Column (db .String (200 ),nullable =False )
    card_number =db .Column (db .String (20 ),nullable =False )
    expiry_date =db .Column (db .String (10 ),nullable =False )
    cvv =db .Column (db .String (4 ),nullable =False )

stripe .api_key ='YOUR_STRIPE_API_KEY'

@app .route ('/step1',methods =['GET','POST'])
def step1 ():
    if request .method =='POST':
        name =request .form ['name']
        address =request .form ['address']
        if not name or not address :
            return render_template ('step1.html',error ='Please fill in all fields.')
        else :
            return redirect (url_for ('step2'))
    return render_template ('step1.html')

@app .route ('/step2',methods =['GET','POST'])
def step2 ():
    if request .method =='POST':
        card_number =request .form ['card_number']
        expiry_date =request .form ['expiry_date']
        cvv =request .form ['cvv']
        if not card_number or not expiry_date or not cvv :
            return render_template ('step2.html',error ='Please fill in all fields.')
        else :
            return redirect (url_for ('step3'))
    return render_template ('step2.html')

@app .route ('/step3',methods =['GET','POST'])
def step3 ():
    if request .method =='POST':
        try :

            charge =stripe .Charge .create (
            amount =1000 ,
            currency ='usd',
            source ='YOUR_STRIPE_SOURCE',
            description ='Test charge'
            )
            if charge .status =='succeeded':
                return redirect (url_for ('completed'))
            else :
                return render_template ('step3.html',error ='Payment processing failed.')
        except Exception as e :
            return render_template ('step3.html',error =str (e ))
    return render_template ('step3.html')

@app .route ('/completed')
def completed ():
    return render_template ('completed.html')

if __name__ =='__main__':
    app .run (debug =True )