from steemdata import SteemData
import datetime
import pandas as pd
import requests
import sys
s = SteemData()


name = sys.argv[1]
print(name)
def get_prices():
    
    r = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=STEEM&tsym=USD&limit=2000')
    adat= (r.json()) 
    price_data =pd.DataFrame(adat["Data"])
    price_data['time'] = pd.to_datetime(price_data['time'],unit='s')
    price_data.head()
    price_data['steem_price'] = price_data[["high", "low"]].mean(axis=1)
    my_prices = price_data[['steem_price', 'time']]

    r = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=SBD&tsym=USD&limit=2000')
    adat_sbd= (r.json()) 
    price_sbd=pd.DataFrame(adat_sbd["Data"])
    price_sbd['time'] = pd.to_datetime(price_sbd['time'],unit='s')

    my_prices["sbd_price"]= price_sbd[["high", "low"]].mean(axis=1)
    my_prices= my_prices[['steem_price', "sbd_price", "time"]]
    return(my_prices)


def get_all_transfer(name):
    
    all_df = pd.DataFrame()
    hosz = s.Operations.find({"type": "transfer", "to": name})
    eddig=hosz.count()
    for i in range(0,eddig,1000):
        print(i)
        adat = s.Operations.find({"type": "transfer", "to": name},
                                 {"_id":0,"from":1,"timestamp":1, 'amount':1}

                                ).limit(1000).skip(i)

        df = pd.DataFrame(list(adat))
        df["money"]= list(map(lambda x: x['amount'], df['amount']))
        df["asset"]= list(map(lambda x: x['asset'], df['amount']))
        df = df[["from", "timestamp", "money", "asset"]]

        all_df = all_df.append(df, ignore_index=True)
    return(all_df)
    
    

all_transfer = get_all_transfer(name)
all_transfer['timestamp'] = all_transfer['timestamp'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour))

price_data = get_prices()

eredemeny_df = all_transfer.merge(price_data, left_on='timestamp', right_on='time', how='left')
blacklist= ['cuttie1979', "blocktrades"]
eredmeny_df = eredemeny_df[eredemeny_df["from"].isin(blacklist)==False]
eredmeny_df["to"]= name

eredmeny_df.to_csv("/home/misrori/R_kodok/steembot_revenu_calculator/tmp.csv", index=False)
