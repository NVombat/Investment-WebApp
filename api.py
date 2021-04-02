import configparser
from configparser import ConfigParser
import json
import requests


def apicall(key: int, symbol: str, date_from: str, date_to: str, limit: int = 1) -> dict:
    """

    :param key:
    :param symbol:
    :param date_from:
    :param date_to:
    :return json data:
    """
    url = f"http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}"

    params = {
        "date_from": date_from,
        "date_to": date_to,
        "limit": limit
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        raise ConnectionRefusedError("Entered symbol or key is wrong")
    else:
        pass

    data = json.loads(res.text)
    return data


def getdata(symbol: str, date_from: str = "2020-08-21",
            date_to: str = "2020-08-22", **kwargs) -> list:
    """

    :rtype: list
    :type date_to: object
    :param date_from: 
    :param symbol:
    :param kwargs:
    :return list of values:
    """
    values = []

    cfg: ConfigParser = configparser.ConfigParser()
    cfg.read('configuration.cfg')
    key = cfg.get("API KEY", "key")

    data_dict = apicall(key, symbol, date_from=date_from, date_to=date_to)["data"][0]

    for _, varg in kwargs.items():
        if varg in data_dict.keys():
            values.append(data_dict[varg])

    return values


if __name__ == '__main__':
    symbol = "GOOGL"
    print(getdata(low='low', high='high', symbol=symbol,
                  date_from="2020-09-25", date_to="2020-10-26", highadj="said"))
