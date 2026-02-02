
import pandas as pd
import logging
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import precision_score
import numpy as np

sp500 = yf.Ticker("^GSPC")

history = sp500.history(period = "max")

index = history.index

del history['Stock Splits']

del history['Dividends']



#graph closing price against the index

def close_v_user():
    x = history.index
    y = history['Close']
    plt.plot(x,y)
    plt.xlabel('Date')
    plt.ylabel('Closing price')
    plt.show()


df_sp500 = history

#Create column tomorrow and set it as the closing price from the day before

df_sp500["Tomorrow"] = df_sp500['Close'].shift(-1)

# if tomorrows price is greater than the closing price return 1 else return 0

df_sp500['Target'] = (df_sp500['Tomorrow']>df_sp500['Close']).astype(int)

#Get rid of anything before 2008

df_sp500 = df_sp500.loc['2008-01-01':].copy()

def learning_and_precision():
    
    model = RandomForestClassifier(n_estimators=300,min_samples_split=100,random_state=1)
    train = df_sp500.iloc[:-100]
    test = df_sp500.iloc[-100:]

    predictors = ['High','Low','Open','Close','Volume']
    model.fit(train[predictors],train['Target'])

    #create prediction
    pred = model.predict(test[predictors]) 
    pred = pd.Series(pred,index= test.index)

    #generate a precision score
    precision = precision_score(test['Target'],pred)

    combined = pd.concat(test['Target'],pred, axis=1)

    return model, precision, combined


def backtesting(data, model, predictors, start= 2500, step= 2):
    
    model = RandomForestClassifier(n_estimators=300, min_samples_split=100, random_state=1)
    predictors = ['High', 'Low', 'Open', 'Close', 'Volume']

    total_predictions = []

    
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)


    for i in range(start,data.shape[0],step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        current_predictions = predictors(train, test, current_predictions, model)
        total_predictions.append(current_predictions)

    predictions = backtesting(df_sp500, model, predictors)
    precision = precision_score(predictions['Target'],predictions['Predictions'])
    print(precision)

    return pd.concat(total_predictions), predictions
    
backtesting()
        



   
    








        

           


