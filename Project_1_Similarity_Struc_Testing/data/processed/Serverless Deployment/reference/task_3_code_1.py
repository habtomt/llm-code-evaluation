`python

from http import HTTPStatus

from typing import Optional

from fastapi import FastAPI ,Request

from pydantic import BaseModel

import uvicorn

import sqlite3

app =FastAPI ()

class WebhookPayload (BaseModel ):

    data :str

def store_payload (payload :str )->None :

    conn =sqlite3 .connect ('webhook.db')

    cursor =conn .cursor ()

    cursor .execute ('INSERT INTO webhooks (payload) VALUES (?)',(payload ,))

    conn .commit ()

    conn .close ()

@app .post ("/webhook_receiver")

async def receive_webhook (payload :WebhookPayload ,request :Request ):

    secret =request .headers .get ('X-Secret')

    if secret !="my_secret_key":

    store_payload (payload .data )

    return {"message":"Webhook received and processed"}

if __name__ =="__main__":

    uvicorn .run (app ,host ="0.0.0.0",port =8000 )