from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
import configparser
import pandas as pd
import numpy as np


def getkey(path: str):
    """
        :param path:
        :return API KEY:
    """
    cfg: configparser.ConfigParser = configparser.ConfigParser()
    cfg.read(path)
    key = cfg.get('TIINGO API', "key")
    return key


def load_t(sym: str):
    from pandas import pandas_datareader as pdr
    key = getkey('../configuration.cfg')
    all_data = pdr.get_data_tiingo(sym, api_key=key)
    all_data.to_csv(f'{sym}.csv')


class Data:
    def __init__(self, path_aap: str, path_goog: str,
                 path_tsla: str):
        """
        loading in the data from csv files for each,
        of the stock files.

        """

        self.df_google = pd.read_csv(path_goog)
        self.df_tsla = pd.read_csv(path_tsla)
        self.df_aap = pd.read_csv(path_aap)

        data_aap = self.df_aap.reset_index()['close']
        data_aap = np.array(data_aap)

        data_tsla = self.df_tsla.reset_index()['close']
        data_tsla = np.array(data_tsla)

        data_goog = self.df_google.reset_index()['close']
        data_goog = np.array(data_goog)
        """
            Standardizing the data fetched from the 
            csv files.
             
        """
        self.scaler_aap = MinMaxScaler(feature_range=(0, 1))
        self.scaler_aap.fit(np.array(data_aap).reshape(-1, 1))
        self.data_aap = self.scaler_aap.transform(data_aap.reshape(-1, 1))

        self.scaler_goog = MinMaxScaler(feature_range=(0, 1))
        self.scaler_goog.fit(np.array(data_goog).reshape(-1, 1))
        self.data_goog = self.scaler_aap.transform(data_goog.reshape(-1, 1))

        self.scaler_tsla = MinMaxScaler(feature_range=(0, 1))
        self.scaler_tsla.fit(np.array(data_tsla).reshape(-1, 1))
        self.data_tsla = self.scaler_aap.transform(data_tsla.reshape(-1, 1))

    @staticmethod
    def _make_dataset(dataset, time_step):
        """
        using the step of the given amount
        making the input features.
        """
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def get_data(self, train_on: str):
        """
        calling the make_dataset function to get the
        features and the labels.
        """
        if train_on == 'GOOGL':
            x_train, y_train = self._make_dataset(self.data_goog, 100)
            return x_train, y_train

        elif train_on == 'TSLA':
            x_train, y_train = self._make_dataset(self.data_tsla, 100)
            return x_train, y_train

        else:
            x_train, y_train = self._make_dataset(self.data_aap, 100)
            return x_train, y_train


def Model():
    """
    Initializing a sequential model
    with 3 lstm layers and a dense layer.
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(150))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam',
                  loss='mse',
                  metrics='mse')

    return model


if __name__ == '__main__':
    """
    fitting the models on the respective 
    dataset.
    """

    data = Data('AAPL.csv', 'google.csv', 'TSLA.csv')
    x_train, y_train = data.get_data()
    x_train = x_train.reshape(1156, 100, 1)
    model = Model()
    model.fit(x_train, y_train, epochs=6)
    model.save('AAPL.h5')

    # load_t('TSLA')
