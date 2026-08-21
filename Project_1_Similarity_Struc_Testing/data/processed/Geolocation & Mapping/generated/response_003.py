import tkinter as tk
from tkinter import messagebox
import datetime
import math
import requests
import json

class FitnessApp :
    def __init__ (self ,root ):

        self .root =root
        self .root .title ("Fitness App")
        self .latitude =0
        self .longitude =0
        self .distance =0
        self .speed =0
        self .tracking =False
        self .route =[]
        self .api_key ="YOUR_API_KEY"

        self .location_label =tk .Label (root ,text ="Current Location: ")
        self .location_label .pack ()
        self .distance_label =tk .Label (root ,text ="Distance: ")
        self .distance_label .pack ()
        self .speed_label =tk .Label (root ,text ="Speed: ")
        self .speed_label .pack ()
        self .start_button =tk .Button (root ,text ="Start Tracking",command =self .start_tracking )
        self .start_button .pack ()
        self .stop_button =tk .Button (root ,text ="Stop Tracking",command =self .stop_tracking ,state ="disabled")
        self .stop_button .pack ()
        self .save_button =tk .Button (root ,text ="Save Activity",command =self .save_activity )
        self .save_button .pack ()

        self .get_location ()

    def get_location (self ):

        self .latitude =37.7749
        self .longitude =-122.4194
        self .location_label .config (text =f"Current Location: {self.latitude}, {self.longitude}")
        self .root .after (1000 ,self .get_location )

    def start_tracking (self ):

        self .tracking =True
        self .start_button .config (state ="disabled")
        self .stop_button .config (state ="normal")
        self .route .append ((self .latitude ,self .longitude ))
        self .calculate_distance ()
        self .calculate_speed ()
        self .distance_label .config (text =f"Distance: {self.distance} km")
        self .speed_label .config (text =f"Speed: {self.speed} km/h")
        self .root .after (1000 ,self .update_tracking )

    def stop_tracking (self ):

        self .tracking =False
        self .start_button .config (state ="normal")
        self .stop_button .config (state ="disabled")

    def update_tracking (self ):

        if self .tracking :
            self .get_location ()
            self .route .append ((self .latitude ,self .longitude ))
            self .calculate_distance ()
            self .calculate_speed ()
            self .distance_label .config (text =f"Distance: {self.distance} km")
            self .speed_label .config (text =f"Speed: {self.speed} km/h")
            self .root .after (1000 ,self .update_tracking )

    def calculate_distance (self ):

        if len (self .route )>1 :
            lat1 ,lon1 =self .route [-2 ]
            lat2 ,lon2 =self .route [-1 ]
            lat1 ,lon1 ,lat2 ,lon2 =map (math .radians ,[lat1 ,lon1 ,lat2 ,lon2 ])
            dlat =lat2 -lat1
            dlon =lon2 -lon1
            a =math .sin (dlat /2 )**2 +math .cos (lat1 )*math .cos (lat2 )*math .sin (dlon /2 )**2
            c =2 *math .atan2 (math .sqrt (a ),math .sqrt (1 -a ))
            distance =6371 *c
            self .distance +=distance

    def calculate_speed (self ):

        if len (self .route )>1 :
            time_diff =(datetime .datetime .now ()-datetime .datetime .now ()).total_seconds ()/3600
            self .speed =self .distance /time_diff

    def save_activity (self ):

        activity_data ={
        "latitude":self .latitude ,
        "longitude":self .longitude ,
        "distance":self .distance ,
        "speed":self .speed ,
        "route":self .route
        }
        try :
            response =requests .post (f"https://api.example.com/activities?api_key={self.api_key}",json =activity_data )
            if response .status_code ==201 :
                messagebox .showinfo ("Activity Saved","Activity data has been saved successfully.")
            else :
                messagebox .showerror ("Error","Failed to save activity data.")
        except requests .exceptions .RequestException as e :
            messagebox .showerror ("Error","Failed to save activity data.")

if __name__ =="__main__":
    root =tk .Tk ()
    app =FitnessApp (root )
    root .mainloop ()