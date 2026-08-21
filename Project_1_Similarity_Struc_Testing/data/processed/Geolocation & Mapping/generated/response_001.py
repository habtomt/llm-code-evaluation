from ortools .constraint_solver import routing_enums_pb2
from ortools .constraint_solver import pywrapcp
import requests
import json
from datetime import datetime

def get_traffic_data (api_key ,origin ,destination ):

    url =f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&mode=driving&traffic_model=pessimistic&key={api_key}"
    response =requests .get (url )
    data =json .loads (response .text )
    return data ['rows'][0 ]['elements'][0 ]['duration_in_traffic']['value']

def create_data_model (api_key ,locations ):

    distance_matrix =[]
    for i in range (len (locations )):
        row =[]
        for j in range (len (locations )):
            if i ==j :
                row .append (0 )
            else :

                row .append (get_traffic_data (api_key ,locations [i ],locations [j ]))
        distance_matrix .append (row )

    data ={
    'distance_matrix':distance_matrix ,
    'num_vehicles':1 ,
    'depot':0 ,
    }
    return data

def print_solution (manager ,routing ,solution ):

    print ('Objective: {}'.format (solution .ObjectiveValue ()))
    index =routing .Start (0 )
    plan_output = 'Route :
'
    route_distance =0
    while not routing .IsEnd (index ):
        plan_output +=' {} ->'.format (manager .IndexToNode (index ))
        previous_index =index
        index =solution .Value (routing .NextVar (index ))
        route_distance +=routing .GetArcCostForVehicle (previous_index ,index ,0 )
    plan_output += '{}
'.format (manager .IndexToNode (index ))
    plan_output += 'Route distance :{}seconds
'.format (route_distance )
    print (plan_output )

def main ():
    api_key ='YOUR_API_KEY'
    locations =['New York, NY','Los Angeles, CA','Chicago, IL','Houston, TX']

    data =create_data_model (api_key ,locations )

    manager =pywrapcp .RoutingIndexManager (len (data ['distance_matrix']),
    data ['num_vehicles'],data ['depot'])

    routing =pywrapcp .RoutingModel (manager )

    def distance_callback (from_index ,to_index ):

        from_node =manager .IndexToNode (from_index )
        to_node =manager .IndexToNode (to_index )
        return data ['distance_matrix'][from_node ][to_node ]

    transit_callback_index =routing .RegisterTransitCallback (distance_callback )

    routing .SetArcCostEvaluatorOfAllVehicles (transit_callback_index )

    search_parameters =pywrapcp .DefaultRoutingSearchParameters ()
    search_parameters .first_solution_strategy =(
    routing_enums_pb2 .FirstSolutionStrategy .PATH_CHEAPEST_ARC )

    solution =routing .SolveWithParameters (search_parameters )

    if solution :
        print_solution (manager ,routing ,solution )
    else :
        print ("No solution found!")

if __name__ =='__main__':
    try :
        main ()
    except Exception as e :
        print (f"An error occurred: {e}")