`python

from google .cloud import translate_v2 as translate

    client =translate .Client ()

    with open (document_path ,'r',encoding ='utf-8')as file :

        text =file .read ()

    result =client .translate (text ,source_language =source_language ,target_language =target_language )

    with open ('translated_document.txt','w',encoding ='utf-8')as file :

        file .write (translated_text )