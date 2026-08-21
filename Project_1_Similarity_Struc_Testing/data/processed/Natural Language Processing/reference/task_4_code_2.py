def text_summarization (text_content ):

    client =language_v1 .LanguageServiceClient ()

    type_ =language_v1 .Document .Type .PLAIN_TEXT

    language ="en"

    document ={"content":text_content ,"type":type_ ,"language":language }

    response =client .analyze_text (request ={'document':document ,'features':{'extract_syntax':False ,'extract_entities':False ,'extract_document_sentiment':False ,'extract_entity_sentiment':False ,'classify_text':False ,'extract_relationships':False ,'summarize_text':True }})

    return response .document_sentiment .score

summary_score =text_summarization (text_to_summarize )

print (summary_score )