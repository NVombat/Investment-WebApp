import torch
from torch.utils.data import Dataset
import pandas_datareader as pdr
import configparser
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class CustomData(Dataset):
    def __init__(self, symbol: str, args: str):
        super(CustomData, self).__init__()
        key = self.getkey('../configuration.cfg')
        self.all_data = pdr.get_data_tiingo(symbol, api_key=key)
        self.close = self.all_data[args].values

        self.close = self.close.reshape(-1, 1)

        scaler = MinMaxScaler(feature_range=(0,1))
        self.close = scaler.fit_transform(np.array(self.close))

        training_size, test_size = self._getsize(self.close)
        self.x_train, self.y_train = self._make_dataset(self.close[0:training_size, :], 100)
        self.x_test, self.y_test = self._make_dataset(self.close[training_size:len(self.close), :1], 100)

    @staticmethod
    def _getsize(arr):
        training_size = int(len(arr) * 0.80)
        test_size = int(len(arr) * 0.10)

        return training_size, test_size

    @staticmethod
    def getkey(path: str):
        """

        :param path:
        :return API KEY:
        """
        cfg: configparser.ConfigParser = configparser.ConfigParser()
        cfg.read(path)
        key = cfg.get('TIINGO API', "key")
        return key

    @staticmethod
    def _make_dataset(dataset, time_step):
        """

        :param dataset:
        :param time_step:
        :return returns dependent and independent features :
        """
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def __getitem__(self, xid):
        pass

data = CustomData('GOOGL', 'close')
