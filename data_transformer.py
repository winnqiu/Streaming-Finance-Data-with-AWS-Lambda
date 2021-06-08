import json
import boto3
import random
import datetime
import pandas as pd
import yfinance as yf

kinesis = boto3.client('kinesis', "us-east-2")

def lambda_handler(event, context):
    
    df = pd.DataFrame(columns=['high','low','ts','name'])
    tickers_list=['FB','SHOP','BYND','NFLX','PINS','SQ','TTD','OKTA','SNAP','DDOG']
    for i in range(0,10):
        temp=tickers_list[i]
        ticker=yf.Ticker(temp)
        hist = ticker.history(period="1d",interval='5m',start='2021-5-11',end='2021-5-12')
        hist.reset_index(inplace=True)
        record=hist[[ "High", "Low","Datetime"]]
        record.columns =['high','low','ts']
        record['name']=temp
        record['ts']=record['ts'].apply(lambda x: x.strftime("%m-%d-%Y %H:%M:%S%z"))
        record['high']=record['high'].apply(lambda x: round(float(x),2))
        record['low']=record['low'].apply(lambda x: round(float(x),2))
        df = df.append(record,ignore_index=True)
    
    for index, row in df.iterrows():
        data=row.to_json()+'\n'
        kinesis.put_record(
                StreamName="STA9760_stream1",
                Data=data,
                PartitionKey="partitionkey")
