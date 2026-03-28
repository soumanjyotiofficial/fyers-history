# fyers-history

A lightweight Python utility for downloading **historical candle data from the Fyers API** while automatically handling large date ranges.

The Fyers API restricts the number of days that can be requested in a single call.  
`fyers-history` solves this limitation by **automatically splitting long date ranges into smaller chunks**, fetching the data sequentially, and merging it into a single dataset.

---

## Features

- Automatically handles **large date ranges**
- Splits requests into **100-day chunks**
- Merges results into a **single pandas DataFrame**
- Removes **duplicate timestamps**
- Optional **automatic CSV saving**
- Clean and simple API

---

## Installation

### Install from local package

Download the source distribution:

```
dist/fyers_history-0.1.0.tar.gz
```

Then open the command prompt in the downloaded folder and run:

```bash
pip install fyers_history-0.1.0.tar.gz
```

---

## Requirements

- Python >= 3.8

### Dependencies

- pandas
- fyers-apiv3

Install dependencies if needed:

```bash
pip install pandas fyers-apiv3
```

---

## Quick Example

```python
import datetime as dt
from fyers_apiv3 import fyersModel
from fyers_history import HistoricalDataManager

# Initialize fyers client
fyers = fyersModel.FyersModel(
    client_id="YOUR_CLIENT_ID",
    token="ACCESS_TOKEN"
)

# Create historical data manager
history = HistoricalDataManager(
    fyers=fyers,
    symbol="NSE:NIFTY50-INDEX",
    start_date=dt.datetime(2024, 1, 1),
    end_date=dt.datetime(2024, 6, 1),
    timeframe="1",
    save_path="data"
)

# Fetch data
df = history.fetch_long_duration()

print(df.head())
```

---

## Parameters

### `HistoricalDataManager`

| Parameter | Type | Description |
|-----------|------|-------------|
| `fyers` | object | Initialized Fyers API client |
| `symbol` | str | Trading symbol |
| `start_date` | datetime | Start date |
| `end_date` | datetime | End date |
| `timeframe` | str | Candle timeframe |
| `save_path` | str (optional) | Directory where CSV will be saved |

---

## Supported Timeframes

```
5S 10S 15S 30S 45S
1 2 3 5 10 15 20 30 60 120 240
1D
```

Meaning:

- `S` → Seconds
- Numbers → Minutes
- `D` → Daily

---

## Output

The function returns a **pandas DataFrame** with the following columns:

| Column | Description |
|------|-------------|
| Date | Timestamp |
| Open | Opening price |
| High | Highest price |
| Low | Lowest price |
| Close | Closing price |
| Volume | Trading volume |
| Symbol | Trading symbol |

Example output:

```
Date                Open   High   Low    Close   Volume   Symbol
2024-01-01 09:15    200    205    198    203     50000    NSE:NIFTY50-INDEX
```

---

## Automatic Range Handling

If the requested range exceeds **100 days**, the library will automatically:

1. Split the request into **100-day chunks**
2. Fetch data sequentially
3. Merge the results
4. Remove duplicate timestamps

This ensures smooth and uninterrupted downloads.

---

## Automatic File Saving

If `save_path` is provided, the data will automatically be stored as CSV.

Example directory structure:

```
data/
│
├── 1/
│   └── NIFTY50-INDEX.csv
│
├── 5/
│   └── RELIANCE-EQ.csv
```

Each **timeframe gets its own folder**.

---

## Example Symbols

```
NSE:HDFCAMC-EQ
NSE:NIFTY50-INDEX
NSE:RELIANCE-EQ
```

---

## Author

**Souman Jyoti**

---

## License

This project is licensed under the **MIT License**.
