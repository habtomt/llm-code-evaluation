`python

from vercel .serverless import scheduled

@scheduled ("0 0 * * *")

def generate_report ():

    data =pull_data_from_database ()

    formatted_report =format_data_into_document (data )

    save_or_send_report (formatted_report )

def pull_data_from_database ():

def format_data_into_document (data ):

    pass

def save_or_send_report (report ):

    pass