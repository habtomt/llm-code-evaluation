import flask
from flask import render_template ,request ,jsonify
import json

app =flask .Flask (__name__ )

translations ={
"en":{
"headline":"Welcome to Our Website",
"welcome-message":"This is a multilingual website example."
},
"es":{
"headline":"Bienvenido a Nuestro Sitio Web",
"welcome-message":"Este es un ejemplo de sitio web multilingüe."
},
"fr":{
"headline":"Bienvenue sur Notre Site Web",
"welcome-message":"Ceci est un exemple de site Web multilingue."
}
}

@app .route ('/')
def index ():
    return render_template ('index.html')

@app .route ('/translate',methods =['POST'])
def translate ():
    try :

        language =request .json ['language']

        if language not in translations :
            return jsonify ({'error':'Unsupported language'}),400

        headline =translations [language ]['headline']
        welcome_message =translations [language ]['welcome-message']

        return jsonify ({'headline':headline ,'welcome-message':welcome_message })

    except KeyError :

        return jsonify ({'error':'Missing language key'}),400

if __name__ =='__main__':
    app .run (debug =True )

"""index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Multilingual Website</title>
</head>
<body>
    <div>
        <label for="language-select">Choose your language:</label>
        <select id="language-select">
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
        </select>
    </div>

    <h1 id="headline"></h1>
    <p id="welcome-message"></p>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const languageSelect = document.getElementById('language-select');

            languageSelect.addEventListener('change', function () {
                const selectedLanguage = this.value;
                fetch('/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ language: selectedLanguage })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('headline').textContent = data.headline;
                    document.getElementById('welcome-message').textContent = data['welcome-message'];
                })
                .catch(error => console.error('Error fetching translations:', error));
            });
        });
    </script>
</body>
</html>
"""