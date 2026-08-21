import os
import yaml
import requests
from datetime import datetime

def read_config (file_path ):

    with open (file_path ,'r')as file :
        return yaml .safe_load (file )

def scrape_metrics (prometheus_url ,job_name ):

    try :
        response =requests .get (f"{prometheus_url}/api/v1/query",params ={"query":f"up{{job='{job_name}'}}"})
        response .raise_for_status ()
        return response .json ()
    except requests .RequestException as e :
        print (f"Error scraping metrics: {e}")
        return None

def send_alert (alertmanager_url ,alert ):

    try :
        response =requests .post (f"{alertmanager_url}/api/v1/alerts",json =alert )
        response .raise_for_status ()
        return response .json ()
    except requests .RequestException as e :
        print (f"Error sending alert: {e}")
        return None

def optimize_database (database_url ,query ):

    try :

        print (f"Optimized database performance: {query}")
    except Exception as e :
        print (f"Error optimizing database: {e}")

def main ():

    config =read_config ("config.yaml")

    prometheus_url =config ["prometheus"]["url"]
    job_name =config ["prometheus"]["job_name"]
    metrics =scrape_metrics (prometheus_url ,job_name )

    alertmanager_url =config ["alertmanager"]["url"]
    for metric in metrics ["data"]["result"]:
        if metric ["value"][1 ]>0.8 :
            alert ={
            "labels":{"alertname":"HighCPUUsage","severity":"warning"},
            "annotations":{"summary":"High CPU usage detected"}
            }
            send_alert (alertmanager_url ,alert )

    database_url =config ["database"]["url"]
    query =config ["database"]["query"]
    optimize_database (database_url ,query )

if __name__ =="__main__":
    main ()