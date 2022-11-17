import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


ticker_symbols = []
with open("Data/Data_Collection/SnP500_list.txt", "r") as f:
    data = f.readlines()
    for i in data:
        ticker_symbols.append(i[:-1])

for t in ticker_symbols:

    # Import .csv file into DataFrame
    ticker = t
    ticker_data = pd.read_csv(f"Data/csv/{ticker}.csv")


    ticker_data.drop(columns="Close")


    training_data = ticker_data.iloc[:int(round(len(ticker_data) * .8 ,0))]
    training_set = ticker_data.iloc[:, 5:6].values

    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler(feature_range=(0,1))
    training_set_scaled = sc.fit_transform(training_set)

    X_train = []
    y_train = []

    for i in range(60, len(training_set)):
        X_train.append(training_set_scaled[i-60 : i, 0])
        y_train.append(training_set_scaled[i,0])

    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    import tensorflow as tf
    from tensorflow import keras
    from keras.models import Sequential
    from keras.layers import LSTM
    from keras.layers import Dropout
    from keras.layers import Dense

    model = Sequential()

    model.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50,return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50,return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    model.compile(optimizer='adam',loss='mean_squared_error')

    model.fit(X_train,y_train,epochs=2,batch_size=32)

    test_data = ticker_data.iloc[-(int(round(len(ticker_data) * .2 ,0))):]
    test_set = test_data.iloc[:, 5:6].values

    dataset_total = pd.concat((training_data['Adjusted Close'], test_data['Adjusted Close']), axis = 0)
    inputs = dataset_total[len(dataset_total) - len(test_data) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, len(inputs)):
        X_test.append(inputs[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = model.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    plt.plot(test_set, color = 'black', label = f"{ticker} Stock Price")
    plt.plot(predicted_stock_price, color = 'green', label = f"Predicted {ticker} Stock Price")
    plt.title(f"{ticker} Stock Price Prediction")
    plt.xlabel('Time')
    plt.ylabel(f"{ticker} Stock Price")
    plt.legend()
    plt.savefig(f"ML_Models/LSTM/LSTMimages/{ticker}.png")
    plt.close()