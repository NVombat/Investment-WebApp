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
    import pandas_datareader as pdr
    key = getkey('../configuration.cfg')
    all_data = pdr.get_data_tiingo(sym, api_key=key)
    all_data.to_csv(f'{sym}.csv')


class Data:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)
        data = self.df.reset_index()['close']
        data = np.array(data)

        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler.fit(np.array(data).reshape(-1, 1))
        self.data = self.scaler.transform(data.reshape(-1, 1))

    @staticmethod
    def _make_dataset(dataset, time_step):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def get_data(self):
        x_train, y_train = self._make_dataset(self.data, 100)
        return x_train, y_train


def Model():
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
    data = Data('AAPL.csv')
    x_train, y_train = data.get_data()
    x_train = x_train.reshape(1156, 100, 1)
    model = Model()
    model.fit(x_train, y_train, epochs=6)
    model.save('AAPL.h5')

    # load_t('TSLA')