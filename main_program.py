from functions import *
from Initiatialize import Initialize
from time import sleep


def loop_tickers(tickers):

    for ticker in tickers:
        try:
            # Access html file from ticker to (Market Watch)
            soup = access_html(ticker)

            # Get a dictionary with Key_data (Not actual price and price change)
            key_data_dictionary = get_key_data(soup)
            # print(copy_dictionary)

            # delete data that is not necessary
            key_data_dictionary = clean_garbage_data(key_data_dictionary)

            # print(copy_dictionary)
            key_data_dictionary = data_converter(key_data_dictionary)

            # get price and chg chg_percentage
            p_dictionary = get_price(ticker)

            # Get actual time
            time_get, date = get_actual_time()
            current_time_format = date.strftime("%Y-%m-%d")

            # Join two dictionaries with the data
            data_dict = {**p_dictionary, **key_data_dictionary, **time_get}

            update_data_base(data_dict, ticker, current_time_format)
        except:
            run_program()


def run_program():
    """" Run program at specific time"""
    tickers = ['aapl', 'tsla', 'fb', 'nflx', 'amd', 'ge']
    run = Initialize()

    while True:
        print("--------------------")
        print("Checking Current Time")
        check_time(run)
        print("--------------------")
        if run.init_program:
            loop_tickers(tickers)

        sleep(15)


run_program()
