import requests
import json

def fetch_product_details (product_id ):
    headers ={
    'X-Shopify-Storefront-Access-Token':'your-access-token',
    'Content-Type':'application/json'
    }
    url ='https://your-store.myshopify.com/api/2026-07/graphql.json'

    query ='''
    query ($id: ID!) {
      product(id: $id) {
        title
        description
        priceRange {
          maxVariantPrice {
            amount
            currencyCode
          }
          minVariantPrice {
            amount
            currencyCode
          }
        }
        images(first: 3) {
          edges {
            node {
              url
            }
          }
        }
      }
    }
    '''

    variables ={
    "id":f"gid://shopify/Product/{product_id}"
    }

    data ={'query':query ,'variables':variables }
    response =requests .post (url ,headers =headers ,data =json .dumps (data ))

    if response .status_code ==200 :
        product_details =json .loads (response .text )
        if 'errors'in product_details :
            print ("GraphQL Errors:",product_details ['errors'])
            return None
        return product_details ['data']['product']
    else :
        print (f"Request failed with status code {response.status_code}")
        return None

def render_product_details (product_details ):

    pass

product_id ='your-product-id'
product_details =fetch_product_details (product_id )
if product_details :
    render_product_details (product_details )