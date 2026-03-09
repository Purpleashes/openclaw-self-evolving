#!/usr/bin/env python3
"""
Check current international oil price and send reminder if >= $80/barrel
"""

import re
import sys
import json
import subprocess
from pathlib import Path

# Add OpenClaw's Python tools path if needed (adjust as necessary)
sys.path.insert(0, str(Path.home() / ".openclaw" / "python"))

try:
    from openclaw import message
except ImportError:
    message = None

def get_oil_price():
    """Fetch current Brent crude oil price using EIA API (free, requires API key)"""
    import requests

    # Get your free API key from https://www.eia.gov/opendata/register.php
    EIA_API_KEY = "vPeYltn20JaHwTcSXGSYRcgZEMhbwUQHmzEvLh9C"

    if EIA_API_KEY == "YOUR_API_KEY_HERE":
        print("Please set your EIA API key in the script")
        return None

    try:
        # EIA API endpoint for Brent crude oil price
        url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={EIA_API_KEY}&frequency=daily&data[0]=value&facets[series][]=RBRTE&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract the latest price
        if "response" in data and "data" in data["response"] and len(data["response"]["data"]) > 0:
            latest_data = data["response"]["data"][0]
            price = latest_data["value"]
            return float(price)
        return None
    except Exception as e:
        print("Error fetching oil price from EIA:", e)
        return None

def main():
    price = get_oil_price()
    if price is None:
        print("Failed to fetch oil price")
        return 1

    print(f"Current Brent crude price: ${price}/barrel")

    if price >= 80:
        alert_msg = f"⚠️ 油价提醒：布伦特原油价格已达到 ${price}/桶，超过 80 美元阈值！"
        print(alert_msg)

        # Try to send message via OpenClaw's message tool if available
        if message:
            try:
                message.send(
                    channel="webchat",  # Adjust channel as needed
                    message=alert_msg
                )
                print("Reminder sent successfully")
            except Exception as e:
                print(f"Failed to send reminder: {e}")
        else:
            print("OpenClaw message tool not available, reminder not sent")
    else:
        print(f"Price ${price} is below $80 threshold")

    return 0

if __name__ == "__main__":
    sys.exit(main())
