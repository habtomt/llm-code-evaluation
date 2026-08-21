import pandas as pd
import matplotlib .pyplot as plt
import seaborn as sns

def load_data (file_path ):

    try :
        data =pd .read_csv (file_path )
        return data
    except Exception as e :
        print (f"Error loading data: {e}")
        return None

def clean_data (data ):

    if data is not None :

        cleaned_data =data .dropna ()

        if 'start_time'in cleaned_data .columns and 'end_time'in cleaned_data .columns :
            cleaned_data ['start_time']=pd .to_datetime (cleaned_data ['start_time'])
            cleaned_data ['end_time']=pd .to_datetime (cleaned_data ['end_time'])
        return cleaned_data
    return None

def detect_bottlenecks (data ):

    if 'start_time'in data .columns and 'end_time'in data .columns :
        data ['duration']=(data ['end_time']-data ['start_time']).dt .total_seconds ()

        bottlenecks =data .groupby ('process_step')['duration'].mean ().sort_values (ascending =False )
    else :
        bottlenecks =None
    return bottlenecks

def suggest_improvements (bottlenecks ,threshold =100 ):

    if bottlenecks is not None :
        suggestions =bottlenecks [bottlenecks >threshold ]
    else :
        suggestions =None
    return suggestions

def visualize_data (bottlenecks ):

    if bottlenecks is not None :
        plt .figure (figsize =(10 ,6 ))
        sns .barplot (x =bottlenecks .index ,y =bottlenecks .values )
        plt .title ("Average Process Duration by Step")
        plt .xlabel ("Process Step")
        plt .ylabel ("Average Duration (seconds)")
        plt .xticks (rotation =90 )
        plt .tight_layout ()
        plt .show ()

def main (file_path ):
    data =load_data (file_path )
    if data is not None :
        cleaned_data =clean_data (data )
        if cleaned_data is not None :
            bottlenecks =detect_bottlenecks (cleaned_data )
            suggestions =suggest_improvements (bottlenecks )
            print ("Bottleneck Analysis:")
            print (bottlenecks )
            print ("\nProcess Improvement Suggestions:")
            print (suggestions )
            visualize_data (bottlenecks )

file_path ='operational_data.csv'
main (file_path )