from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject
import cbpro #  useuful to get detailed historic data
#   used for Simple Mving Average
import pandas as pd
import btalib

#  Add Coinbase API Key and API secret
coinbase_API_key = 'GiPQ4zWIHD7WDxxq'
coinbase_API_secret = 'YM22PWHbdhmRDfQbIcRyiY8wJ784SjC5'
#   This authenticates the client with the provided API key and API secret
client = Client(coinbase_API_key, coinbase_API_secret)


def retrieve_acc_balance():

    #  Specify the starting account balance upon which the summation process will begin
    total = 0
    message = []
    #   We'll get our accounts and for each wallet in our accounts data we'll append the wallet name and the native balance
    accounts = client.get_accounts()
    for wallet in accounts.data:
        message.append(str(wallet['name']) + ' ' + str(wallet['native_balance']))
        #   We took off the PAB from the native balance so we can make the total sum
        value = str(wallet['native_balance']).replace('PAB', '')
        total += float(value)
    message.append(' Total Balance: ' + 'USD ' + str(total))
    print('\n'.join(message))

def real_time_price():
    #   Select currency
    currency_code = 'USD'
    #   Specify currency code we want to obtain
    price = client.get_spot_price(currency_pair='BTC-USD')
    print('Current Bitcoin price in %s: %s'%(currency_code, price.amount))
    price = client.get_spot_price(currency_pair='ETH-USD')
    print('Current Ethereum price in %s: %s'%(currency_code, price.amount))

#   Not working properly. Find it use anyways
def spot_historic_data():
    price = client.get_spot_price(currency_pair='BTC-USD', date ='2022-27-01')

def get_historical_data():
    print(client._make_api_object(client._get('v2', 'prices', 'BTC-USD', 'historic'), APIObject))

def cbpro_historic_data():
    public_client = cbpro.PublicClient()
    #   Remember to print those things
    #  ticker on the product we'll working on
    public_client.get_product_ticker(product_id='ETH-USD')
    data = public_client.get_product_historic_rates('ETH-USD')

    #  SMA logic
    #   Clean the data so we will work with the first 5 items.
    for line in data:
        del line[5:]
    #   Create pandas data frame and name the columns
    dataframe = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])
    dataframe.set_index('date', inplace=True)
    #   Save the data frame to a CSV file
    dataframe.to_csv('HistoricRates')

    #   Calculate the 20SMA with pandas
    dataframe['20sma'] = dataframe.close.rolling(20).mean()
    print(dataframe.tail(5))

    #   Calculate sma with btalib
    #  Here we are comparing the two 20sma. The first sma (from left to right) is from pandas. The 2nd one is from btalib
    dataframe['sma'] = btalib.sma(dataframe.close, period=20).df
    print(dataframe.tail())
cbpro_historic_data()





