# past_date_calculator.py

from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta
import sys


def get_past_date(time_str):
    # Regular expression to parse the input string
    pattern = re.compile(r'(\d+)\s*(days?|hours?|months?|years?)\s*ago')
    match = pattern.match(time_str)
    
    if not match:
        raise ValueError("Input string is not in the correct format")
    
    # Extract the quantity and unit from the input string
    quantity = int(match.group(1))
    unit = match.group(2).lower()
    
    # Get the current date and time
    now = datetime.now()
    
    if 'day' in unit:
        past_date = now - timedelta(days=quantity)
    elif 'hour' in unit:
        past_date = now - timedelta(hours=quantity)
    elif 'month' in unit:
        past_date = now - relativedelta(months=quantity)
    elif 'year' in unit:
        past_date = now - relativedelta(years=quantity)
    else:
        raise ValueError("Unknown time unit")
    
    return past_date

# Examples
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        lines = sys.stdin.readlines()

        for line in lines:
            print(get_past_date(line))
        sys.exit(0)

    print(get_past_date(sys.argv[1]))
