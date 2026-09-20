import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import zoneinfo
import json
import pandas as pd
import mplfinance as mpf

# Lấy thông tin của key và secret
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Đưa folder local vào trong module để search
sdk_path = Path(__file__).resolve().parent / "openapi-sdk" / "python"
if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))

# Chuyển ngày thành UNIX
def date_to_unix(date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S", tz_name: str = "Asia/Ho_Chi_Minh") -> int:    
    dt = datetime.strptime(date_str, date_format)    
    tz = zoneinfo.ZoneInfo(tz_name)
    dt_with_tz = dt.replace(tzinfo=tz)    
    return int(dt_with_tz.timestamp())

# Chuyển unix thành ngày
def unix_to_dates(ts_list: list[int], tz_name: str = "Asia/Ho_Chi_Minh", date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]: 
    tz = zoneinfo.ZoneInfo(tz_name)    
    return [
        datetime.fromtimestamp(ts, tz=tz).strftime(date_format)
        for ts in ts_list
    ]

# Nhập ngày
start_date = input("Nhập ngày bắt đầu theo định dạng (YYYY-MM-DD): ")
end_date = input("Nhập ngày kết thúc theo định dạng (YYYY-MM-DD): ")
start_date = date_to_unix(start_date, date_format="%Y-%m-%d")
end_date = date_to_unix(end_date, date_format="%Y-%m-%d")

# Tận dụng code của DNSE và vẽ chart cổ phiếu
from dnse import DNSEClient

def main():
    client = DNSEClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        base_url="https://openapi.dnse.com.vn",
    )

    status, body = client.get_ohlc(
        bar_type="STOCK",
        query={
            "symbol": "VIC",
            "resolution": "1D",
            "from": start_date,
            "to": end_date
        },
        dry_run=False,
    )

    body = json.loads(body)
    date_list = unix_to_dates(body['t'], date_format="%Y-%m-%d")

    daily = pd.DataFrame(
        {'Date': date_list, 
        'Open': body['o'],
        'High': body['h'],
        'Low': body['l'],
        'Close': body['c'],
        'Volume': body['v']}
    )

    daily['Date'] =  pd.to_datetime(daily['Date'])
    daily = daily.set_index('Date')

    mpf.plot(daily, type='candle')

if __name__ == "__main__":
    main()