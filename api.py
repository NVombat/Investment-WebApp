import configparser
import json
import requests
import datetime as d


def apicall(key: int, symbol: str, date_from: str, date_to: str, limit: int = 1) -> dict:
    """


    :param key:
    :param symbol:
    :param date_from:
    :param date_to:
    :return json data:
    """
    url = f'http://api.marketstack.com/v1/eod?access_key={key}&symbols={symbol}'

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


# UPDATE DATES TO GET NEW VALUES
# CURRENT DATE -
date = d.datetime.now()
date = date.strftime("%Y-%m-%d")
# print("Today the date is:", date)

#Closing Date
# today = d.date.today()
# close_date = today - d.timedelta(days=1)
# close_date = close_date.strftime("%Y-%m-%d")
# print("One day ago the date was CLOSE DATE:", close_date)

#Opening Date
# open_date = today - d.timedelta(days=2)
# open_date = open_date.strftime("%Y-%m-%d")
# print("Two days ago the date was OPEN DATE:", open_date)

#Safe Values
open_date = "2021-04-01"
close_date = "2021-04-02"
# format - yyyy-mm-dd --- eg -> 2021-04-17

def getdata(symbol: str, date_from: str = open_date,
            date_to: str = close_date, **kwargs) -> list:
    """

    :rtype: list
    :type date_to: object
    :param date_from: 
    :param symbol:
    :param kwargs:
    :return list of values:
    """
    values = []

    cfg: configparser.ConfigParser = configparser.ConfigParser()
    cfg.read('configuration.cfg')
    key = cfg.get("API KEY", "key")

    data_list: list = apicall(key, symbol, date_from=date_from, date_to=date_to)["data"]
    # print(data_list)
    if data_list:
        data_dict = data_list[0]

    else:
        raise ValueError("Entered dates are not correct")

    for _, varg in kwargs.items():
        if varg in data_dict.keys():
            values.append(data_dict[varg])

    return values


if __name__ == '__main__':
    symbol = "GOOGL"
    print(open_date, close_date)
    print(getdata(close='close', symbol=symbol,
                  date_from=open_date, date_to=close_date))
