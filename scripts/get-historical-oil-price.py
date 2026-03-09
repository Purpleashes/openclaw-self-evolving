
#!/usr/bin/env python3
"""
Get historical oil prices from EIA API
"""

import requests

EIA_API_KEY = "vPeYltn20JaHwTcSXGSYRcgZEMhbwUQHmzEvLh9C"

url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={EIA_API_KEY}&frequency=daily&data[0]=value&facets[series][]=RBRTE&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=15"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    if "response" in data and "data" in data["response"]:
        for item in data["response"]["data"]:
            print(f"{item['period']}: ${item['value']}/barrel")
except Exception as e:
    print("Error:", e)
