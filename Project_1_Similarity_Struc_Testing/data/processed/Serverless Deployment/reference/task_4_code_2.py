`python

from http import server

from http .server import BaseHTTPRequestHandler

from urllib .parse import parse_qs

class ChatbotHandler (BaseHTTPRequestHandler ):

    def do_POST (self ):

        post_data =self .rfile .read (content_length )

        params =parse_qs (post_data .decode ('utf-8'))

        user_input =params .get ('user_input',[''])[0 ]

        chatbot_response =generate_chatbot_response (user_input )

        self .send_response (200 )

        self .send_header ('Content-type','application/json')

        self .end_headers ()

        self .wfile .write (chatbot_response .encode ('utf-8'))

def generate_chatbot_response (user_input ):

    return f'Chatbot response to "{user_input}"'

if __name__ =='__main__':

    server_address =('',8000 )

    httpd =server .HTTPServer (server_address ,ChatbotHandler )

        print ('Starting server...')

        httpd .serve_forever ()

    except KeyboardInterrupt :

        httpd .server_close ()