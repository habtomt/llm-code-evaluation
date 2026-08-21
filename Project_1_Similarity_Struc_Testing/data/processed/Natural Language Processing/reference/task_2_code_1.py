from google .cloud import language_v1

client =language_v1 .LanguageServiceClient ()

document ={
"content":"Google, headquartered in Mountain View, unveiled the new Android phone",
"type":language_v1 .Document .Type .PLAIN_TEXT ,
}

response =client .analyze_entities (
document =document ,
encoding_type =language_v1 .EncodingType .UTF8
)

for entity in response .entities :
    print ("Entity name: {}".format (entity .name ))
    print ("Entity type: {}".format (language_v1 .Entity .Type (entity .type ).name ))
    print ("Salience score: {}".format (entity .salience ))