from azure .core .credentials import AzureKeyCredential

from azure .ai .formrecognizer import FormRecognizerClient

import os

endpoint ="https://<your-api-endpoint>.cognitiveservices.azure.com/"

credential =AzureKeyCredential ("<your-api-key>")

form_recognizer_client =FormRecognizerClient (endpoint ,credential )

invoice_path ="path_to_invoice/invoice.pdf"

with open (invoice_path ,"rb")as invoice :

    invoices =poller .result ()

for idx ,invoice in enumerate (invoices ):

    print ("--------Recognizing invoice #{}--------".format (idx +1 ))

    vendor_name =invoice .vendor_name .value

    invoice_date =invoice .invoice_date

    invoice_number =invoice .invoice_number

    total_amount =invoice .total_amount .value

    print ("Vendor Name: {}".format (vendor_name ))

    print ("Invoice Number: {}".format (invoice_number ))

    print ("Total Amount: {}".format (total_amount ))