from sendgrid .helpers .mail import Mail ,Email ,Content ,Substitution ,Personalization

sg =sendgrid .SendGridAPIClient (api_key ='YOUR_API_KEY')

SUBJECT ='Welcome to our Newsletter!'

FROM_EMAIL =Email ("example@example.com")

TO_EMAIL =Email ("recipient@example.com")

content =Content ("text/plain","Welcome to our newsletter! Stay tuned for exciting updates and offers.")

mail =Mail (FROM_EMAIL ,SUBJECT ,TO_EMAIL ,content )

mail .template_id ="YOUR_TEMPLATE_ID"

response =sg .client .mail .send .post (request_body =mail .get ())

print (response .body )

print (response .headers )