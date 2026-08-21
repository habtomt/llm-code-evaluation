from flask import Flask ,jsonify ,render_template
import random
import time

app =Flask (__name__ )

products =[
{"id":1 ,"name":"Product 1","price":100 },
{"id":2 ,"name":"Product 2","price":200 },
]

product_details ={
1 :{"description":"Description for Product 1","stock":20 },
2 :{"description":"Description for Product 2","stock":10 },
}

@app .route ("/")
def index ():
    return render_template ("index.html")

@app .route ("/api/products")
def get_products ():
    return jsonify (products )

@app .route ("/api/product/<int:product_id>/details")
def get_product_details (product_id ):

    time .sleep (0.5 )
    return jsonify (product_details .get (product_id ,{}))

@app .route ("/api/product/<int:product_id>/price",methods =["PUT"])
def update_product_price (product_id ):

    new_price =random .randint (100 ,200 )

    return jsonify ({"price":new_price })

if __name__ =="__main__":
    app .run (debug =True )