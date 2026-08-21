`python

from datetime import datetime

from apscheduler .schedulers .blocking import BlockingScheduler

import os

import psycopg2

from docx import Document

def generate_report ():

    conn =psycopg2 .connect (database ="your_db_name",user ="your_username",password ="your_password",host ="your_host",port ="your_port")

    cursor =conn .cursor ()

    data =cursor .fetchall ()

    conn .close ()

    doc =Document ()

    doc .add_heading ('Generated Report',0 )

    for row in data :

        doc .add_paragraph (str (row ))

    doc .save ('generated_report.docx')

sched =BlockingScheduler ()

sched .add_job (generate_report ,'cron',day_of_week ='mon-fri',hour =9 )

sched .start ()