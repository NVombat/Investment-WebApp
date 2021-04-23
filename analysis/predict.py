from tensorflow.keras.models import load_model
import numpy as np
from .train import Data


class Predict(Data):
    def __init__(self, symbol: str, path_aap: str,
                 path_goog: str, path_tsla: str):
        super(Predict, self).__init__(path_aap, path_goog, path_tsla)
        self.model_aap = None
        self.model_tsla = None
        self.model_goog = None
        self.symbol = symbol

        self.load()

    def load(self) -> object:
        """

        :param symbol:
        :return:
        """
        if self.symbol == 'GOOGL' and not self.model_goog:
            print("LOADING GOOGLE MODEL")
            self.model_goog = load_model('analysis/google.h5')

        elif self.symbol == 'TSLA' and not self.model_tsla:
            print("LOADING TESLA MODEL")
            self.model_tsla = load_model('analysis/TSLA.h5')

        elif self.symbol == 'AAPL' and not self.model_aap:
            print("LOADING AAPLE MODEL")
            self.model_aap = load_model('analysis/AAPL.h5')

    def result(self, inputs: list):
        """

        :param inputs:
        :return:
        """
        assert len(inputs) == 100, "Model accepts input of size 100"

        model_input = np.array(inputs)
        model_input = model_input.reshape(len(model_input), 1)

        if self.symbol == 'GOOGL':
            model_input = self.scaler_goog.transform(model_input).reshape(1, len(model_input), 1)
            return self.scaler_goog.inverse_transform(self.model_goog(model_input))[0][0]

        elif self.symbol == 'TSLA':
            model_input = self.scaler_tsla.transform(model_input).reshape(1, len(model_input), 1)
            return self.scaler_tsla.inverse_transform(self.model_tsla(model_input))[0][0]

        else:
            model_input = self.scaler_aap.transform(model_input).reshape(1, len(model_input), 1)
            return self.scaler_aap.inverse_transform(self.model_aap(model_input))[0][0]


if __name__ == '__main__':
    predict_goog = Predict(symbol='GOOGL', path_aap='AAPL.csv',
                      path_goog='google.csv', path_tsla='TSLA.csv')

    random = np.random.randint(low=1000, high=2000, size=100)
    print(predict_goog.result(random))

    random = np.random.randint(low=1000, high=2000, size=100)
    print(predict_goog.result(random))

