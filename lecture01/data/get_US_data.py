"""
Download US financial data:
- SP500 index
- USD/EUR and USD/GBP exchange rates
- US interest rates (Fed Funds, 1Y Treasury, 10Y Treasury)

Outputs:
- us_equity_data.csv: SP500, USD/EUR, USD/GBP
- us_interest_rates.csv: Fed Funds, US 1Y, US 10Y (filtered to 1975+, business days only)
"""

import pandas as pd
import requests
from datetime import datetime
import pandas_datareader as pdr
import warnings
warnings.filterwarnings('ignore')

# FRED API Key
FRED_API_KEY = '32cd7dae85ec69ede68b759475584d44'
FRED_BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'


def download_us_equity_fx():
    """
    Download US equity and FX data using pandas-datareader.
    Returns: DataFrame with SP500, USD/EUR, USD/GBP
    """
    print("Downloading US equity and FX data...")
    
    dataframes = []
    
    # Download SPY ETF (S&P 500 ETF) using yfinance (more reliable than index)
    print("  Downloading SP500 (SPY ETF)...")
    try:
        # Try yfinance download function
        import yfinance as yf
        sp500 = yf.download('SPY', start='1950-01-01', progress=False)
        if not sp500.empty:
            sp500 = sp500[['Close']].copy()
            sp500.columns = ['SP500']
            # Remove timezone info to match FRED data
            if sp500.index.tz is not None:
                sp500.index = sp500.index.tz_localize(None)
            dataframes.append(sp500)
            print(f"  ✓ SP500 (SPY ETF): {len(sp500)} rows from {sp500.index.min().date()} to {sp500.index.max().date()}")
        else:
            print(f"  ✗ Could not download SPY: No data returned")
    except Exception as e:
        print(f"  ✗ Error downloading SP500: {e}")
    
    if not dataframes:
        print("✗ No equity data downloaded")
        return pd.DataFrame()
    
    # Combine all series
    df = pd.concat(dataframes, axis=1)
    print(f"✓ Downloaded US equity data: {len(df)} rows")
    
    return df


def download_fred_series(series_id, series_name):
    """
    Download a single series from FRED API.
    
    Args:
        series_id: FRED series identifier
        series_name: Readable name for the series
    
    Returns: DataFrame with the series data
    """
    print(f"  Downloading {series_name} ({series_id})...")
    
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json'
    }
    
    try:
        response = requests.get(FRED_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'observations' not in data:
            print(f"  ✗ No data found for {series_name}")
            return pd.DataFrame()
        
        # Extract observations
        observations = data['observations']
        df = pd.DataFrame(observations)
        
        # Convert date and value
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Set date as index
        df = df.set_index('date')[['value']]
        df.columns = [series_name]
        
        print(f"  ✓ {series_name}: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error downloading {series_name}: {e}")
        return pd.DataFrame()


def download_us_interest_rates():
    """
    Download US interest rates from FRED.
    Returns: DataFrame with Fed Funds rate
    """
    print("Downloading US interest rates from FRED...")
    
    fred_series = {
        'DFF': 'FED_FUNDS'
    }
    
    dataframes = []
    
    for series_id, series_name in fred_series.items():
        df = download_fred_series(series_id, series_name)
        if not df.empty:
            dataframes.append(df)
    
    if not dataframes:
        print("✗ No interest rate data downloaded")
        return pd.DataFrame()
    
    # Merge all dataframes
    result = pd.concat(dataframes, axis=1)
    
    # Filter to dates >= 1975-01-01
    print("  Filtering to dates >= 1975-01-01...")
    result = result[result.index >= '1975-01-01']
    
    # Reindex to business days only
    print("  Reindexing to business days only...")
    business_days = pd.bdate_range(
        start=result.index.min(),
        end=result.index.max()
    )
    result = result.reindex(business_days)
    
    # Forward fill missing values
    result = result.ffill()
    
    print(f"✓ Downloaded US interest rates: {len(result)} business days")
    
    return result


def main():
    """
    Main function to download US data and save to CSV files.
    """
    print("=" * 60)
    print("US Financial Data Download Script")
    print("=" * 60)
    print()
    
    # Download equity and FX data
    equity_fx = download_us_equity_fx()
    
    if not equity_fx.empty:
        # Convert index to date only (remove time component)
        equity_fx.index = pd.to_datetime(equity_fx.index.date)
        # Filter to dates >= 1996-01-01
        equity_fx = equity_fx[equity_fx.index >= '1996-01-01']
        output_file = 'lecture01/data/us_equity_data.csv'
        equity_fx.to_csv(output_file)
        print(f"\n✓ Saved equity/FX data to {output_file}")
        print(f"  Columns: {', '.join(equity_fx.columns)}")
        print(f"  Date range: {equity_fx.index.min().date()} to {equity_fx.index.max().date()}")
        print(f"  Total rows: {len(equity_fx)}")
    else:
        print("\n✗ No equity/FX data to save")
    
    print()
    
    # Download interest rate data
    interest_rates = download_us_interest_rates()
    
    if not interest_rates.empty:
        # Convert index to date only (remove time component)
        interest_rates.index = pd.to_datetime(interest_rates.index.date)
        output_file = 'lecture01/data/us_interest_rates.csv'
        interest_rates.to_csv(output_file)
        print(f"\n✓ Saved interest rate data to {output_file}")
        print(f"  Columns: {', '.join(interest_rates.columns)}")
        print(f"  Date range: {interest_rates.index.min().date()} to {interest_rates.index.max().date()}")
        print(f"  Total business days: {len(interest_rates)}")
    else:
        print("\n✗ No interest rate data to save")
    
    print()
    print("=" * 60)
    print("Download complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
