`python

from vercel.serverless import scheduled



@scheduled("0 0 * * *")  # Run the function at midnight every day

def generate_report():

    # Pull data from the database

    data = pull_data_from_database()



    # Format data into a report using a suitable library

    formatted_report = format_data_into_document(data)



    # Save the report or send it via email

    save_or_send_report(formatted_report)



def pull_data_from_database():

    # Implement logic to pull data from the database



def format_data_into_document(data):

    # Implement logic to format data into a document using a suitable library

    pass



def save_or_send_report(report):

    # Implement logic to save the report or send it via email

    pass