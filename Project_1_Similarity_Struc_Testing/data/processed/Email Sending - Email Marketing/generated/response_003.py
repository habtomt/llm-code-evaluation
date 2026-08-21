from flask import Flask ,request ,render_template_string ,send_file
from flask_mail import Mail ,Message
import logging

app =Flask (__name__ )

app .config ['MAIL_SERVER']='smtp.gmail.com'
app .config ['MAIL_PORT']=465
app .config ['MAIL_USE_TLS']=False
app .config ['MAIL_USE_SSL']=True
app .config ['MAIL_USERNAME']='YOUR_EMAIL@gmail.com'
app .config ['MAIL_PASSWORD']='YOUR_EMAIL_PASSWORD'

mail =Mail (app )

subscribers =[]

subscription_html ='''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Newsletter Subscription</title>
</head>
<body>
  <h1>Subscribe to our Newsletter</h1>
  <form action="/subscribe" method="POST">
    <input type="email" name="email" required placeholder="Enter your email" />
    <button type="submit">Subscribe</button>
  </form>
</body>
</html>
'''

manage_html ='''
<h1>Manage Preferences</h1>
<p>Your email: {{ email }}</p>
<button onclick="unsubscribe()">Unsubscribe</button>
<script>
  function unsubscribe() {
    fetch('/unsubscribe?email={{ email | urlencode }}', { method: 'POST' })
      .then(response => response.text())
      .then(data => alert(data))
      .catch(error => console.error('Error:', error));
  }
</script>
'''

@app .route ('/',methods =['GET'])
def index ():
    return render_template_string (subscription_html )

@app .route ('/subscribe',methods =['POST'])
def subscribe ():
    try :
        email =request .form ['email']
        if email not in subscribers :
            subscribers .append (email )

            msg =Message ("Thanks for subscribing!",sender ="YOUR_EMAIL@gmail.com",recipients =[email ])
            msg .body =f"You have subscribed to our newsletter. Manage your preferences here: http://localhost:5000/manage?email={email}"
            mail .send (msg )
            return 'Subscription successful, confirmation email sent'
        else :
            return 'This email is already subscribed'
    except Exception as e :
        logging .error (f"Error: {e}")
        return 'Error subscribing'

@app .route ('/manage',methods =['GET'])
def manage ():
    try :
        email =request .args .get ('email')
        if email in subscribers :
            return render_template_string (manage_html ,email =email )
        else :
            return 'Email not found'
    except Exception as e :
        logging .error (f"Error: {e}")
        return 'Error managing preferences'

@app .route ('/unsubscribe',methods =['POST'])
def unsubscribe ():
    try :
        email =request .args .get ('email')
        subscribers .remove (email )
        return 'Successfully unsubscribed'
    except Exception as e :
        logging .error (f"Error: {e}")
        return 'Error unsubscribing'

if __name__ =='__main__':
    app .run (debug =True ,port =5000 )