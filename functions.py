from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import os.path
import datetime
from dateutil import parser


def access_html(ticker):
    """ Get html parsed to get the data
        Return: soup element"""

    url = f'https://www.marketwatch.com/investing/stock/{ticker}'
    # Get access to the webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(f"{ticker.upper()}: Access html,Successful")

    return soup


def get_key_data(soup):
    """ Get key data (Not the actual price of the stock) """
    key_data = soup.findAll('li', {'class': 'kv__item'})

    # Get Key_data (Price is missing
    list_keys = []
    list_values = []

    for element in key_data:
        key = element.find('small').text.strip()
        value = element.find('span').text.strip()
        list_keys.append(key)
        list_values.append(value)

    dictionary = dict(zip(list_keys, list_values))
    copy_dictionary = dictionary.copy()

    return copy_dictionary


def clean_garbage_data(copy_dictionary):
    # Clean garbage data (not necessary)
    del_items = ['52 Week Range',
                 'Market Cap',
                 'Public Float',
                 'P/E Ratio',
                 'Yield',
                 'Ex-Dividend Date',
                 'Short Interest',
                 '% of Float Shorted']

    for key in del_items:
        try:
            del copy_dictionary[key]
        except:
            print(f"{key}: Not remove > check")

    return copy_dictionary


def data_converter(copy_dictionary):
    """ Clean garbage key from a dictionary (key_data) """
    # Convert data to float (numbers)
    for key, value in copy_dictionary.items():
        list_string = value.split()
        # print(f"List of string: {list_string}")
        list_of_list = []

        for item in list_string:
            # print(f"item: {item}")

            if item[-1] == 'M':
                list_values = data_extract_number(item) * 1e6
            elif item[-1] == 'B':
                list_values = data_extract_number(item) * 1e9
            else:
                list_values = data_extract_number(item)

            if not list_values:
                pass
            else:
                try:
                    list_of_list.append(list_values)
                    copy_dictionary[key] = list_of_list
                except:
                    pass

    copy_dictionary["Day Range Low"] = [copy_dictionary['Day Range'][0]]
    copy_dictionary["Day Range High"] = [copy_dictionary['Day Range'][1]]
    del copy_dictionary["Day Range"]

    return copy_dictionary


def data_extract_number(item):
    """ Extract the numbers from a string
        If there is a conditional ['Million', Billion]
        use with other function ---"""
    list_of_list = []
    new_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in item)
    # print(f"New String: {new_string}")
    try:
        list_of_numbers = [float(i) for i in new_string.split()]
        # print('list of numbers', list_of_numbers)
        # list_of_list.append(list_of_numbers[0])
        # copy_dictionary[key] = list_of_list
        return list_of_numbers[0]
    except:
        pass


def get_price(ticker):
    """ Get the actual price of the stock and point variance[value / %]
        Return: dictionary{Price, Price change, Price change percentage}"""
    soup = access_html(ticker)
    price_data = soup.find('div', {"class": "intraday__data"})
    # print(price_data)

    try:
        price = float(price_data.find('bg-quote', {'class': "value"}).text)
        # print(price_data)

        p_chg = soup.find('span', {"class": "change--point--q"}).text
        p_chg_percent = soup.find('span', {"class": "change--percent--q"}).text
        price_change_data = [p_chg, p_chg_percent]
        # print(price_change_data)
        # price_change_data = price_data.find('td', {"class": "table__cell fixed-to-top negative"}).text.strip().split()

        new_list = []

        for element in price_change_data:
            new_list.append(data_extract_number(element))

        p_chg, p_chg_percent = new_list

        p_dictionary = {"Price": [price],
                        "Price Change": [p_chg],
                        "Price Percent Change": [p_chg_percent / 100]}

        print(f"{ticker.upper()}: Successful price gotten")
        return p_dictionary

    except:
        print(f"{ticker.upper()}: Error getting price changes")
        # Implement error message <<<<<<<<<<<<<<<<<<<<<<<<


def update_data_base(dictionary, ticker, current_time_format):
    """ Export the data to a csv file
        dictionary: A dictionary with the data"""
    data = pd.DataFrame(dictionary)

    if os.path.isfile(f"data_{ticker}_{current_time_format}.csv"):
        try:
            data_read = pd.read_csv(f"data_{ticker}_{current_time_format}.csv")
            data = pd.concat([data_read, data])
            data.to_csv(f"data_{ticker}_{current_time_format}.csv", index=False)
        except FileNotFoundError:
            pass
    else:
        data.to_csv(f"data_{ticker}_{current_time_format}.csv", index=False)
    print(f"{ticker.upper()}: Updated")
    print("--------------------")


def get_actual_time():
    """ Import the actual time at the execution of the function
        Return a dictionary {'Time': time}"""
    date = datetime.datetime.now()
    dictionary = {'Time': [datetime.datetime.now()]}

    return dictionary, date


def check_time(run):
    """ Check the correct interval time to run the script """

    timing = '%s:%s' % (datetime.datetime.now().hour, datetime.datetime.now().minute)
    start_time = parser.parse(run.start_time).hour * 60 + parser.parse(run.start_time).minute
    end_time = parser.parse(run.end_time).hour * 60 + parser.parse(run.end_time).minute
    current_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute

    if start_time <= current_time <= end_time:
        run.init_program = True
    else:
        run.init_program = False

    print(f"Estate of time: {run.init_program}\n"
          f"Actual Time: {timing}")