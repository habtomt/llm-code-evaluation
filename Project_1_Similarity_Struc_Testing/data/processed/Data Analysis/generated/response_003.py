import pandas as pd
import numpy as np
from sklearn .model_selection import train_test_split
from sklearn .linear_model import LinearRegression
from sklearn .metrics import mean_squared_error ,r2_score
import matplotlib .pyplot as plt

np .random .seed (0 )
n_samples =100
price =np .random .uniform (10 ,100 ,size =n_samples )
demand =2000 -10 *price +np .random .normal (0 ,50 ,size =n_samples )
data =pd .DataFrame ({'Price':price ,'Demand':demand })

X =data [['Price']]
y =data ['Demand']

X_train ,X_test ,y_train ,y_test =train_test_split (X ,y ,test_size =0.2 ,random_state =42 )

model =LinearRegression ()
model .fit (X_train ,y_train )

y_pred =model .predict (X_test )

print (f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print (f"R-squared: {r2_score(y_test, y_pred)}")

test_prices =X_test ['Price']
actual_revenue =test_prices *y_test
predicted_revenue =test_prices *y_pred

plt .scatter (y_test ,y_pred )
plt .xlabel ('Actual Demand')
plt .ylabel ('Predicted Demand')
plt .title ('Actual vs Predicted Demand')
plt .show ()

plt .scatter (actual_revenue ,predicted_revenue )
plt .xlabel ('Actual Revenue')
plt .ylabel ('Predicted Revenue')
plt .title ('Actual vs Predicted Revenue')
plt .show ()

new_prices =np .array ([20 ,50 ,80 ]).reshape (-1 ,1 )
predicted_demand_for_new_prices =model .predict (new_prices )
predicted_revenue_for_new_prices =new_prices .flatten ()*predicted_demand_for_new_prices

for price ,demand ,revenue in zip (new_prices .flatten (),predicted_demand_for_new_prices ,predicted_revenue_for_new_prices ):
    print (f"Price: ${price:.2f}, Predicted Demand: {demand:.2f}, Predicted Revenue: ${revenue:.2f}")

seasonality =np .random .uniform (0.8 ,1.2 ,size =n_samples )
data ['Seasonality']=seasonality
X_seasonal =data [['Price','Seasonality']]
y =data ['Demand']

X_train_seasonal ,X_test_seasonal ,y_train ,y_test =train_test_split (X_seasonal ,y ,test_size =0.2 ,random_state =42 )

model_seasonal =LinearRegression ()
model_seasonal .fit (X_train_seasonal ,y_train )

y_pred_seasonal =model_seasonal .predict (X_test_seasonal )

print (f"Mean Squared Error (Seasonal): {mean_squared_error(y_test, y_pred_seasonal)}")
print (f"R-squared (Seasonal): {r2_score(y_test, y_pred_seasonal)}")

from sklearn .ensemble import RandomForestRegressor
model_rf =RandomForestRegressor (n_estimators =100 )
model_rf .fit (X_train ,y_train )

y_pred_rf =model_rf .predict (X_test )

print (f"Mean Squared Error (RF): {mean_squared_error(y_test, y_pred_rf)}")
print (f"R-squared (RF): {r2_score(y_test, y_pred_rf)}")

from sklearn .model_selection import cross_val_score
scores =cross_val_score (model ,X ,y ,cv =5 )
print (f"Cross-validation scores: {scores}")
print (f"Average cross-validation score: {np.mean(scores)}")

simulated_prices =np .linspace (10 ,100 ,1000 ).reshape (-1 ,1 )
simulated_demands =model .predict (simulated_prices )
simulated_revenues =simulated_prices .flatten ()*simulated_demands

plt .plot (simulated_prices ,simulated_demands )
plt .xlabel ('Price')
plt .ylabel ('Demand')
plt .title ('Simulated Demand')
plt .show ()

plt .plot (simulated_prices ,simulated_revenues )
plt .xlabel ('Price')
plt .ylabel ('Revenue')
plt .title ('Simulated Revenue')
plt .show ()

def real_time_pricing (current_price ,current_demand ):

    global model
    new_data =pd .DataFrame ({'Price':[current_price ],'Demand':[current_demand ]})
    model .fit (new_data [['Price']],new_data ['Demand'])

    next_price =current_price *1.1
    predicted_demand =model .predict (np .array ([[next_price ]]))

    return predicted_demand

current_price =50
current_demand =100
predicted_demand =real_time_pricing (current_price ,current_demand )
print (f"Predicted demand for the next time period: {predicted_demand:.2f}")

try :

    data =pd .read_csv ('price_demand_data.csv')
except Exception as e :
    print (f"Error loading data: {e}")

    np .random .seed (0 )
    n_samples =100
    price =np .random .uniform (10 ,100 ,size =n_samples )
    demand =2000 -10 *price +np .random .normal (0 ,50 ,size =n_samples )
    data =pd .DataFrame ({'Price':price ,'Demand':demand })