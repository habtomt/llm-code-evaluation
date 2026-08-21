from flask import Flask ,render_template ,request ,redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail ,Message
from datetime import datetime ,timedelta
import os

app =Flask (__name__ )

app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///events.db'
app .config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app .config .update (
MAIL_SERVER ='smtp.example.com',
MAIL_PORT =465 ,
MAIL_USE_SSL =True ,
MAIL_USERNAME ='you@example.com',
MAIL_PASSWORD ='password'
)

db =SQLAlchemy (app )
mail =Mail (app )

class Attendee (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    name =db .Column (db .String (100 ))
    email =db .Column (db .String (100 ),unique =True )
    rsvp_status =db .Column (db .String (20 ))

class Event (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    name =db .Column (db .String (100 ))
    date =db .Column (db .DateTime )
    attendees =db .relationship ('Attendee',backref ='event',lazy =True )

event =Event (name ="Sample Event",date =datetime (2022 ,12 ,25 ))

@app .route ('/')
def index ():
    return "Welcome to the Event Invitation System!"

@app .route ('/send_invitations')
def send_invitations ():

    attendees =Attendee .query .all ()

    for attendee in attendees :
        try :
            msg =Message (subject ="You're Invited to an Event!",
            sender ='you@example.com',
            recipients =[attendee .email ],
            body =f"Dear {attendee.name},\n\nYou are invited to {event.name} on {event.date}.\nPlease RSVP by clicking here.")
            mail .send (msg )
        except Exception as e :

            print (f"Error sending email to {attendee.email}: {str(e)}")

    return "Invitations sent!"

@app .route ('/rsvp/<attendee_id>/<status>')
def rsvp (attendee_id ,status ):

    attendee =Attendee .query .get (attendee_id )
    if not attendee :
        return "Attendee not found",404

    attendee .rsvp_status =status
    db .session .commit ()
    return f"RSVP updated for {attendee.name} to {status}"

@app .route ('/send_reminders')
def send_reminders ():

    attendees =Attendee .query .filter_by (rsvp_status ='Accepted').all ()

    for attendee in attendees :
        if event .date -datetime .now ()<timedelta (days =3 ):
            try :
                msg =Message (subject ="Reminder for the Upcoming Event",
                sender ='you@example.com',
                recipients =[attendee .email ],
                body =f"Dear {attendee.name},\n\nThis is a reminder that {event.name} is happening soon on {event.date}.")
                mail .send (msg )
            except Exception as e :

                print (f"Error sending email to {attendee.email}: {str(e)}")

    return "Reminders sent!"

if __name__ =='__main__':

    db .create_all ()

    app .run (debug =True )