import datetime as dt
import os
from time import sleep
import pandas as pd
from fyers_apiv3 import fyersModel
import math
class HistoricalDataManager:
    def __init__(self,fyers:fyersModel, symbol:str, start_date,end_date, timeframe, save_path=None):
        """"
        symbol:str      | Example: "NSE:HDFCAMC-EQ" ; "NSE:NIFTY50-INDEX"
        start_date:str  | Example: "2025-1-1" Format: YYYY-MM-DD
        start_date:str  | Example: "2025-12-31" Format: YYYY-MM-DD
        timeframe:str   | Anyone among this list ["10S","15S","30S","45S",'5S', "240","120","60","30","20","15","10","5","3","2","1","1D"]
                        | with S it represent the second, with D it represent Daily Data and other represent minute data
        """
        self.fyers = fyers
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.save_to = save_path
        self.df = pd.DataFrame()
        self.validate()
    def validate(self):
    
        timeframe_ = ["10S","15S","30S","45S",'5S', "240","120","60","30","20","15","10","5","3","2","1","1D","1M"]
        
        if self.timeframe not in timeframe_:
            x = ",".join(timeframe_)
            raise ValueError(f"Invalid timeframe\nChoose among the following:\n {x}")
        
    def Historical(self):
        sleep(1)

        """
        This function is used to extract historical data from Fyers Server
        parameter:
            symbol: ticker name eg:TCS datatype:string
        """
        data = {
            "symbol": self.symbol.upper(),
            "resolution": f"{self.timeframe}",
            "date_format": "1",
            "range_from": str(self.start_date),
            "range_to": str(self.end_date),
            "cont_flag": "1"
        }
        response = self.fyers.history(data=data)
        try:
            response = self.fyers.history(data=data)
            data = pd.DataFrame(response['candles'], columns=["Date", "Open", "High", "Low", "Close", "Volume"])
            data['Date'] = pd.to_datetime(data["Date"], unit='s')
            data['Date'] = data['Date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
            data['Symbol'] = self.symbol.upper()
            return data
        except:
            raise RuntimeError(f"{response}")

    def Long_duration(self):

        """
        This will return the df when the days count between start and end date is more then equal to 100
        """
        number_of_day = abs((self.start_date - self.end_date).days)
        start__ = self.start_date
        endeing = self.end_date
        
        limitday_ = 100
        if number_of_day > limitday_:
            no_loop = math.ceil(number_of_day / limitday_)
            count = 0
            for a in range(0, no_loop):
                end__ = start__ + dt.timedelta(limitday_)
                self.end_date = end__ if end__ < endeing else endeing
                self.start_date = start__
                
                if count <= no_loop:
                    data = self.Historical()
                    if len(self.df) != 0:
                        self.df = pd.concat([self.df, data], axis=0)
                        self.df = self.df[self.df['Date'].duplicated()==False]
                    else:
                        self.df = data
                        self.df = self.df[self.df['Date'].duplicated()==False]
                    count += 1
                start__ += dt.timedelta(limitday_)
        self.df = self.df[self.df['Date'].duplicated()==False]

        if self.save_to:
            self.df.to_csv(f"{self.save_to}\\{self.timeframe}\\{self.symbol.replace("NSE:",'')}.csv", index=False)
        return self.df
   