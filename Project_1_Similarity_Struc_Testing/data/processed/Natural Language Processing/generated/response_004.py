from transformers import pipeline

def summarize_text (document ,max_length =150 ,min_length =25 ):

    try :

        summarizer =pipeline ("summarization")
    except Exception as e :

        print (f"Failed to load summarization pipeline: {e}")
        return None

    try :

        summary =summarizer (document ,max_length =max_length ,min_length =min_length ,do_sample =False )
    except Exception as e :

        print (f"Failed to generate summary: {e}")
        return None

    return summary [0 ]['summary_text']

if __name__ =="__main__":

    text_document ="""
    Natural language processing (NLP) is a subfield of linguistics, computer science,
    information engineering, and artificial intelligence concerned with the
    interactions between computers and human (natural) languages, in particular how to
    program computers to process and analyze large amounts of natural language data.
    The result is a computer capable of "understanding" the contents of documents,
    including the contextual nuances of the language within them. The technology can
    then accurately extract information and insights contained in the documents as
    well as categorize and organize the documents themselves.
    """

    summary =summarize_text (text_document )

    print ("Summary:")
    print (summary )