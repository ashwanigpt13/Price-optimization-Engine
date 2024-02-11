from argparse import ArgumentParser

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle
import os
import numpy as np
import requests 
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression
import time





URL = "https://m.indiamart.com/proddetail/white-chickpeas-kabuli-chana-23638370312.html" 
def get_price(URL):
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    price = soup.find('p', attrs = {"id":"Price"}) 
    price = str(price)
    price = float(price.split(">")[1].split("/")[0].split(" ")[1].strip())
    return price

def predict_for_today(base_price,lr_Model,Delta_in,inventory_in,NetPerProfit_MAX):
    price = lr_Model.predict([[base_price,Delta_in,inventory_in,NetPerProfit_MAX,Delta_in*Delta_in,inventory_in*inventory_in,inventory_in*Delta_in]])
    return price[0][0]

netPerProfit_AVG = 24
Volatility = 0.4

from sklearn.model_selection import train_test_split

def main(args):  
    
    netPerProfit_AVG = args.average_margin
    Volatility = args.volatility
    NetPerProfit_MAX=netPerProfit_AVG*(1+Volatility)
    NetPerProfit_MIN=netPerProfit_AVG*(1+Volatility)
    chana_act = pd.read_csv("./input/chana_act.csv")
    X = chana_act[["Prices","Delta","inventory","NetPerProfit"]]
    y = chana_act[["ChangedPrices"]]
    X["f1"] = X["Delta"]*X["Delta"]
    X["f2"] = X["inventory"]*X["inventory"]
    X["f3"] = X["inventory"]*X["Delta"]     
    X_train,X_test,y_train,y_test = train_test_split(X,y)
    lr_Model = LinearRegression()
    lr_Model = lr_Model.fit(X,y)
    print(lr_Model.coef_)
    # with open('project_chana_price_prediction/checkpoints/chana_price_lr_model.pkl', 'wb') as f:
    #     lr_Model = pickle.dump(lr_Model,f)
    Delta_in = float(args.Delta)
    inventory_in = float(args.inventory)

    # print(lr_Model.predict(X_test))
    X_test["NetPerProfit"] = NetPerProfit_MAX
    # print(y_test)
    #PREDICT TODAY Price
    base_price = float(get_price(URL))
    print(base_price)
    
    predicted_price=predict_for_today(base_price,lr_Model,Delta_in,inventory_in,NetPerProfit_MAX)
    print(predicted_price)
    cTime = args.ctime
    print(cTime)
    predicted_price_str = str(predicted_price)
    with open(f"output.txt","w") as f:
        f.write(predicted_price_str)
    return predicted_price



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--average_margin", default=10,help="average margin on product")
    parser.add_argument("--volatility", default=0.3,help="how much percent margin deviates from average margin")
    parser.add_argument("--Delta",default=10)
    parser.add_argument("--inventory",default=100)
    parser.add_argument("--ctime",help="currTime")
    args = parser.parse_args()
    main(args)