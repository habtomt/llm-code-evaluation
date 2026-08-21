`python

from http import server

import json

from urllib .parse import urlparse ,parse_qs

class WebhookHandler (server .BaseHTTPRequestHandler ):

    def do_POST (self ):

        content_length =int (self .headers ['Content-Length'])

        post_data =self .rfile .read (content_length )

        payload =json .loads (post_data )

def run_webhook_server ():

    server_address =('',8000 )

    webhook_server =server .HTTPServer (server_address ,WebhookHandler )

if __name__ =='__main__':

    run_webhook_server ()