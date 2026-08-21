import pandas as pd
import numpy as np
import matplotlib .pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data (file_path ):

    try :
        data =pd .read_csv (file_path )
        return data
    except Exception as e :
        print (f"Error loading data: {e}")
        return None

def convert_timestamp (data ):

    try :
        data ['timestamp']=pd .to_datetime (data ['timestamp'])
        return data
    except Exception as e :
        print (f"Error converting timestamp: {e}")
        return None

def extract_hour (data ):

    try :
        data ['hour']=data ['timestamp'].dt .hour
        return data
    except Exception as e :
        print (f"Error extracting hour: {e}")
        return None

def find_peak_traffic_times (data ):

    try :
        traffic_by_hour =data .groupby ('hour').size ()
        return traffic_by_hour
    except Exception as e :
        print (f"Error finding peak traffic times: {e}")
        return None

def plot_traffic_by_hour (traffic_by_hour ):

    try :
        plt .figure (figsize =(10 ,6 ))
        plt .plot (traffic_by_hour .index ,traffic_by_hour .values ,marker ='o')
        plt .title ('Website Traffic by Hour')
        plt .xlabel ('Hour of Day')
        plt .ylabel ('Number of Visitors')
        plt .grid (True )
        plt .show ()
    except Exception as e :
        print (f"Error plotting traffic by hour: {e}")

def analyze_user_demographics (data ):

    try :
        age_distribution =data ['age'].value_counts ()
        gender_distribution =data ['gender'].value_counts ()
        return age_distribution ,gender_distribution
    except Exception as e :
        print (f"Error analyzing user demographics: {e}")
        return None ,None

def plot_user_demographics (age_distribution ,gender_distribution ):

    try :
        plt .figure (figsize =(12 ,5 ))
        plt .subplot (1 ,2 ,1 )
        age_distribution .plot (kind ='bar',color ='skyblue')
        plt .title ('Age Distribution')
        plt .xlabel ('Age')
        plt .ylabel ('Number of Users')

        plt .subplot (1 ,2 ,2 )
        gender_distribution .plot (kind ='bar',color ='lightgreen')
        plt .title ('Gender Distribution')
        plt .xlabel ('Gender')
        plt .ylabel ('Number of Users')

        plt .tight_layout ()
        plt .show ()
    except Exception as e :
        print (f"Error plotting user demographics: {e}")

def calculate_engagement_metrics (data ):

    try :
        avg_pages_viewed =data ['pages_viewed'].mean ()
        avg_session_duration =data ['session_duration'].mean ()
        return avg_pages_viewed ,avg_session_duration
    except Exception as e :
        print (f"Error calculating engagement metrics: {e}")
        return None ,None

def plot_session_duration (data ):

    try :
        plt .figure (figsize =(8 ,6 ))
        sns .histplot (data ['session_duration'],bins =30 ,kde =True ,color ='orange')
        plt .title ('Session Duration Distribution')
        plt .xlabel ('Session Duration (minutes)')
        plt .ylabel ('Frequency')
        plt .grid (True )
        plt .show ()
    except Exception as e :
        print (f"Error plotting session duration: {e}")

def main ():
    file_path ='web_traffic_data.csv'
    data =load_data (file_path )
    if data is not None :
        data =convert_timestamp (data )
        if data is not None :
            data =extract_hour (data )
            if data is not None :
                traffic_by_hour =find_peak_traffic_times (data )
                if traffic_by_hour is not None :
                    plot_traffic_by_hour (traffic_by_hour )
                age_distribution ,gender_distribution =analyze_user_demographics (data )
                if age_distribution is not None and gender_distribution is not None :
                    plot_user_demographics (age_distribution ,gender_distribution )
                avg_pages_viewed ,avg_session_duration =calculate_engagement_metrics (data )
                if avg_pages_viewed is not None and avg_session_duration is not None :
                    print (f"Average Pages Viewed: {avg_pages_viewed:.2f}")
                    print (f"Average Session Duration: {avg_session_duration:.2f} minutes")
                    plot_session_duration (data )

if __name__ =="__main__":
    main ()