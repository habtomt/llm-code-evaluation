import schedule
import time
from sqlalchemy import create_engine
import pandas as pd
from reportlab .lib .pagesizes import letter
from reportlab .pdfgen import canvas
from sqlalchemy import text

DATABASE_URI ='postgresql://YOUR_USER:YOUR_PASSWORD@localhost/YOUR_DBNAME'
engine =create_engine (DATABASE_URI )

def fetch_data ():
    query ="SELECT * FROM your_table"
    with engine .connect ()as connection :

        data =connection .execute (text (query )).fetchall ()

        df =pd .DataFrame ([dict (row )for row in data ])
    return df

def generate_report (data ):

    report_file ='report.pdf'

    c =canvas .Canvas (report_file ,pagesize =letter )
    c .setFont ("Helvetica",12 )

    text =c .beginText (50 ,750 )
    text .setFont ("Helvetica",12 )
    text .setLeading (14 )

    text .textLine ('Report')
    text .textLine ('--------------')

    for index ,row in data .iterrows ():
        line =', '.join ([f'{col}: {row[col]}'for col in data .columns ])
        text .textLine (line )

    c .drawText (text )
    c .showPage ()
    c .save ()

    print (f"Report generated: {report_file}")

def scheduled_job ():
    print ("Fetching data and generating report...")
    try :
        data =fetch_data ()
        generate_report (data )
    except Exception as e :
        print ("Error generating report:",str (e ))

schedule .every ().day .at ("09:00").do (scheduled_job )

while True :
    schedule .run_pending ()
    time .sleep (60 )