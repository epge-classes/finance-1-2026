"""
Download Brazilian financial data:
- IBOV index (Brazilian stock market main index)
- Brazilian treasury interest rates (short and long-term)

Outputs:
- brazil_equity_data.csv: IBOV
- brazil_interest_rates.csv: SELIC (short-term), Long-term rate (filtered to 1975+, business days only)
"""

import pandas as pd
import yfinance as yf
import requests
from datetime import datetime
import time

# BCB API URL template
BCB_SGS_URL = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'


def download_brazil_equity():
    """
    Download Brazilian equity index (IBOV) using yfinance.
    Returns: DataFrame with IBOV
    """
    print("Downloading Brazilian equity data from Yahoo Finance...")
    
    ticker_symbol = '^BVSP'
    name = 'IBOV'
    
    try:
        print(f"  Downloading {name} ({ticker_symbol})...")
        
        # Use yf.download for better rate limit handling
        data = yf.download(ticker_symbol, start='1990-01-01', progress=False)
        
        if data.empty:
            print(f"  ✗ No data returned for {name}")
            return pd.DataFrame()
        
        # Extract close prices
        df = data[['Close']].copy()
        df.columns = [name]
        
        # Remove timezone if present
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        
        print(f"  ✓ {name}: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
        
        return df
        
    except Exception as e:
        print(f"  ✗ Error downloading {name}: {e}")
        return pd.DataFrame()


def download_bcb_series(series_id, series_name):
    """
    Download a series from BCB API with date range chunking.
    BCB API requires date ranges and has max 10-year window for daily data.
    
    Args:
        series_id: BCB series identifier
        series_name: Readable name for the series
    
    Returns: DataFrame with the series data
    """
    print(f"  Downloading {series_name} (series {series_id})...")
    
    all_data = []
    start_year = 1986
    end_year = datetime.today().year + 1
    
    for year_start in range(start_year, end_year, 10):
        year_end = min(year_start + 10, end_year)
        date_start = f'01/01/{year_start}'
        date_end = f'31/12/{year_end - 1}'
        
        url = f'{BCB_SGS_URL.format(series_id)}&dataInicial={date_start}&dataFinal={date_end}'
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                all_data.extend(data)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            # Skip periods with errors (like 404 for unavailable data)
            continue
    
    if not all_data:
        print(f"    ✗ No data downloaded for {series_name}")
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # BCB returns dates in DD/MM/YYYY format
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.rename(columns={'data': 'date', 'valor': series_name})
    
    # Remove duplicates and sort
    df = df.drop_duplicates(subset='date').sort_values('date')
    df = df.set_index('date')[[series_name]]
    
    print(f"    ✓ {series_name}: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
    
    return df


def download_brazil_interest_rates():
    """
    Download Brazilian interest rates from BCB.
    Returns: DataFrame with realized daily DI rate
    """
    print("Downloading Brazilian interest rates from BCB...")
    
    # BCB series codes:
    # 4389 = CDI (Taxa DI - Over/Selic) - realized daily DI rate
    bcb_series = {
        '4389': 'DI_DAILY'       # Realized daily DI rate
    }
    
    dataframes = []
    
    for series_id, series_name in bcb_series.items():
        df = download_bcb_series(series_id, series_name)
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
    
    print(f"✓ Downloaded Brazilian interest rates: {len(result)} business days")
    
    return result


def main():
    """
    Main function to download Brazilian data and save to CSV files.
    """
    print("=" * 60)
    print("Brazilian Financial Data Download Script")
    print("=" * 60)
    print()
    
    # Download equity data
    equity = download_brazil_equity()
    
    if not equity.empty:
        # Convert index to date only (remove time component)
        equity.index = pd.to_datetime(equity.index.date)
        output_file = 'lecture01/data/brazil_equity_data.csv'
        equity.to_csv(output_file)
        print(f"\n✓ Saved equity data to {output_file}")
        print(f"  Columns: {', '.join(equity.columns)}")
        print(f"  Date range: {equity.index.min().date()} to {equity.index.max().date()}")
        print(f"  Total rows: {len(equity)}")
    else:
        print("\n✗ No equity data to save")
    
    print()
    
    # Download interest rate data
    interest_rates = download_brazil_interest_rates()
    
    if not interest_rates.empty:
        # Convert index to date only (remove time component)
        interest_rates.index = pd.to_datetime(interest_rates.index.date)
        output_file = 'lecture01/data/brazil_interest_rates.csv'
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
