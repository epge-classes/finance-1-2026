"""
Download USD/BRL and USD/EUR daily exchange rate data since 1996.

Sources:
- USD/BRL: BCB SGS API (series 1, PTAX USD/BRL selling rate)
- USD/EUR: FRED CSV endpoint (DEXUSEU, inverted to EUR per USD)

Output: usd_fx_data.csv with columns USDBRL and USDEUR.
"""

import pandas as pd
import requests
import io
from datetime import datetime
import time


BCB_SGS_URL = "http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def download_bcb_series(series_id, series_name, start_year=1996):
    """
    Download a BCB SGS series with 10-year chunking for daily data.
    """
    print(f"Downloading {series_name} from BCB SGS (series {series_id})...")

    all_data = []
    end_year = datetime.today().year + 1

    for year_start in range(start_year, end_year, 10):
        year_end = min(year_start + 10, end_year)
        date_start = f"01/01/{year_start}"
        date_end = f"31/12/{year_end - 1}"

        url = f"{BCB_SGS_URL.format(series_id)}&dataInicial={date_start}&dataFinal={date_end}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            if data:
                all_data.extend(data)
            time.sleep(0.5)
        except requests.exceptions.RequestException:
            continue

    if not all_data:
        print(f"  ✗ No data returned for {series_name}")
        return pd.DataFrame()

    df = pd.DataFrame(all_data)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.rename(columns={"data": "date", "valor": series_name})
    df = df.drop_duplicates(subset="date").sort_values("date")
    df = df.set_index("date")[[series_name]]

    print(f"  ✓ {series_name}: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
    return df


def download_fred_usd_eur(start_date="1996-01-01"):
    """
    Download USD/EUR daily exchange rates from FRED (DEXUSEU inverted).
    """
    print("Downloading USDEUR from FRED (DEXUSEU inverted)...")

    params = {
        "id": "DEXUSEU",
    }

    try:
        response = requests.get(FRED_CSV_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("  ✗ No data returned for USDEUR")
        return pd.DataFrame()

    df = pd.read_csv(io.StringIO(response.text))
    df = df.rename(columns={"observation_date": "date", "DEXUSEU": "USD_PER_EUR"})
    df["date"] = pd.to_datetime(df["date"])
    df["USD_PER_EUR"] = pd.to_numeric(df["USD_PER_EUR"], errors="coerce")
    df["USDEUR"] = 1 / df["USD_PER_EUR"]
    df = df.set_index("date")[["USDEUR"]]
    df = df[df.index >= pd.to_datetime(start_date)]

    print(f"  ✓ USDEUR: {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")
    return df


def download_usd_fx(start_date="1996-01-01"):
    """
    Download USD/BRL and USD/EUR daily exchange rates from official sources.

    Args:
        start_date: YYYY-MM-DD start date

    Returns:
        DataFrame indexed by date with columns USDBRL and USDEUR.
    """
    # BCB series 1: USD/BRL PTAX selling rate
    usd_brl = download_bcb_series("1", "USDBRL", start_year=int(start_date[:4]))
    usd_eur = download_fred_usd_eur(start_date=start_date)

    if usd_brl.empty and usd_eur.empty:
        return pd.DataFrame()

    fx = pd.concat([usd_brl, usd_eur], axis=1)
    return fx


def main():
    print("=" * 60)
    print("USD FX Download Script")
    print("=" * 60)

    fx = download_usd_fx()

    if fx.empty:
        print("\n✗ No FX data to save")
        return

    fx.index = pd.to_datetime(fx.index.date)
    output_file = "lecture01/data/usd_fx_data.csv"
    fx.to_csv(output_file)

    print(f"\n✓ Saved FX data to {output_file}")
    print(f"  Columns: {', '.join(fx.columns)}")
    print(f"  Date range: {fx.index.min().date()} to {fx.index.max().date()}")
    print(f"  Total rows: {len(fx)}")

    print("=" * 60)
    print("Download complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
