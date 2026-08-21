from flask import Flask ,request ,jsonify
import joblib
import numpy as np
import pickle
import logging

logging .basicConfig (level =logging .INFO )
logger =logging .getLogger (__name__ )

app =Flask (__name__ )

def load_model ():
    try :
        with open ('model.pkl','rb')as f :
            model =pickle .load (f )
        return model
    except Exception as e :
        logger .error (f"Error loading model: {e}")
        return None

model =load_model ()

def generate_response (user_input ):
    try :

        input_array =np .array ([user_input ])

        response =model .predict (input_array )
        return response [0 ]
    except Exception as e :
        logger .error (f"Error generating response: {e}")
        return "An error occurred while generating the response."

@app .route ('/chatbot',methods =['POST'])
def chatbot ():

    data =request .json
    if 'user_input'not in data :
        return jsonify ({'error':'Invalid input'}),400

    user_input =data ['user_input']

    response =generate_response (user_input )

    return jsonify ({'response':response })

if __name__ =='__main__':
    app .run (debug =True )