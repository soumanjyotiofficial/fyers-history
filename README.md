# fyers-history

A simple Python utility to download historical candle data from the Fyers API while automatically handling large date ranges.

The Fyers API limits the number of days that can be fetched in a single request.  
This library solves that limitation by automatically splitting long ranges into smaller requests and combining the results into a single dataset.

---

## Installation

Install the package using pip.

pip install fyers-history

---

## Requirements

Python >= 3.8

Dependencies:
- pandas
- fyers-apiv3

---

## Quick Example

import datetime as dt
from fyers_apiv3 import fyersModel
from fyers_history import HistoricalDataManager

# Initialize fyers client
fyers = fyersModel.FyersModel(
    client_id="YOUR_CLIENT_ID",
    token="ACCESS_TOKEN"
)

# Create history manager
history = HistoricalDataManager(
    fyers=fyers,
    symbol="NSE:NIFTY50-INDEX",
    start_date=dt.datetime(2024,1,1),
    end_date=dt.datetime(2024,6,1),
    timeframe="1",
    save_path="data"
)

df = history.fetch_long_duration()

print(df.head())

---

## Parameters

HistoricalDataManager

fyers  
Fyers API client instance.

symbol  
Trading symbol.  
Example:
NSE:HDFCAMC-EQ  
NSE:NIFTY50-INDEX

start_date  
Start date as datetime object.

end_date  
End date as datetime object.

timeframe  
Supported values:

5S 10S 15S 30S 45S  
1 2 3 5 10 15 20 30 60 120 240  
1D

Meaning:

S → seconds  
numbers → minutes  
D → daily

save_path (optional)  
Directory where the CSV file will be stored.

---

## Output

The function returns a pandas DataFrame with the following columns:

Date  
Open  
High  
Low  
Close  
Volume  
Symbol

Example structure:

Date                Open   High   Low    Close  Volume  Symbol
2024-01-01 09:15    200    205    198    203    50000   NSE:NIFTY50-INDEX

---

## Automatic Range Handling

If the requested date range exceeds 100 days, the library will:

1. Split the request into 100 day chunks
2. Fetch data sequentially
3. Merge the results
4. Remove duplicate timestamps

This ensures uninterrupted historical downloads.

---

## Automatic File Saving

If save_path is provided, data will be saved automatically.

Example directory structure:

data/
    ├── 1/
    │   └── NIFTY50-INDEX.csv
    ├── 5/
    │   └── RELIANCE-EQ.csv

Each timeframe is stored in its own folder.

---

## Example Symbols

NSE:HDFCAMC-EQ  
NSE:NIFTY50-INDEX  
NSE:RELIANCE-EQ  

---

## Author

Souman Jyoti

---

## License

MIT License
