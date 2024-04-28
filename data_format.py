import requests
import pandas as pd
import numpy as np
from io import StringIO
from yahoo_fin import stock_info as si
from datetime import datetime
from datetime import timedelta
import calendar
import pandas as pd
import matplotlib.ticker
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datapane as dp
from plotly.io import write_image
import matplotlib.dates as mdates
import mplfinance as mpf
import time
import yfinance as yf

def get_coinmetrics_onchain(endpoint):
  url = f'https://raw.githubusercontent.com/coinmetrics/data/master/csv/{endpoint}'
  response = requests.get(url)
  data = pd.read_csv(StringIO(response.text), low_memory=False)
  data['time'] = pd.to_datetime(data['time'])
  print("Coinmetrics Data Call Completed")
  return data

def get_fear_and_greed_index():
  url = "https://api.alternative.me/fng/?limit=0"
  response = requests.get(url)
  data = response.json()
  df = pd.DataFrame(data['data'])
  df['time'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')  # convert unix timestamp to datetime
  df = df[['value', 'value_classification',
           'time']]  # select only the required columns
  print("Fear & Greed Data Call Completed")
  return df

def get_bitcoin_dominance():
  url = "https://api.coingecko.com/api/v3/global"
  response = requests.get(url)
  data = response.json()
  bitcoin_dominance = data['data']['market_cap_percentage']['btc']
  # Assuming that the 'updated_at' is the relevant timestamp for dominance data
  timestamp = pd.to_datetime(data['data']['updated_at'], unit='s')
  df = pd.DataFrame({'bitcoin_dominance': [bitcoin_dominance], 'time': [timestamp]})
  print("Bitcoin Dominance Data Call Completed")
  return df

def get_kraken_ohlc(pair, interval, since):
  url = 'https://api.kraken.com/0/public/OHLC'
  params = {
      'pair': pair,
      'interval': interval,
      'since': since
  }
  response = requests.get(url, params=params)

  if response.status_code != 200:
      print("Error fetching Kraken data")
      print("Status Code:", response.status_code)
      print("Response:", response.text)
      return pd.DataFrame()

  data = response.json()

  if 'error' in data and data['error']:
      print("Error in response data:", data['error'])
      return pd.DataFrame()

  # Extracting the relevant pair data (assuming the first key in 'result')
  pair_key = list(data['result'].keys())[0]
  ohlc_data = data['result'][pair_key]

  # Create a DataFrame from the response
  df = pd.DataFrame(ohlc_data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Volume', 'Count'])
  df['Time'] = pd.to_datetime(df['Time'], unit='s')

  # Convert 'Open', 'High', 'Low', 'Close', 'VWAP', 'Volume' to float
  float_cols = ['Open', 'High', 'Low', 'Close', 'VWAP', 'Volume']
  df[float_cols] = df[float_cols].astype(float)

  print("Kraken OHLC Data Call Completed")

  return df

def get_btc_trade_volume_14d():
  url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
  params = {
      'vs_currency': 'usd',
      'days': '14',
      'interval': 'daily'
  }
  response = requests.get(url, params=params)
  data = response.json()
  # The volume data is a list of [timestamp, value] lists
  volume_data = data['total_volumes']
  # Convert to DataFrame
  df = pd.DataFrame(volume_data, columns=['time', 'btc_trading_volume'])
  df['time'] = pd.to_datetime(df['time'], unit='ms')  # convert milliseconds timestamp to datetime
  print("BTC Trade Volume Data Call Completed")
  return df

def get_crypto_data(ticker_list):
  data = pd.DataFrame()
  for ticker in ticker_list:
      success = False
      retries = 0
      max_retries = 5  # Max number of retries
      retry_delay = 60  # Initial delay in seconds (1 minute)

      while not success and retries < max_retries:
          try:
              # CoinGecko endpoint to get historical data for a coin
              url = f'https://api.coingecko.com/api/v3/coins/{ticker}/market_chart'
              params = {
                  'vs_currency': 'usd',
                  'days': '365',
                  'interval': 'daily'
              }
              response = requests.get(url, params=params)
              response.raise_for_status()

              # Parse the JSON data
              json_data = response.json()
              prices = pd.DataFrame(json_data['prices'], columns=['time', f'{ticker}_close'])
              volumes = pd.DataFrame(json_data['total_volumes'], columns=['time', f'{ticker}_volume'])
              market_caps = pd.DataFrame(json_data['market_caps'], columns=['time', f'{ticker}_market_cap'])

              # Convert the timestamp to datetime
              prices['time'] = pd.to_datetime(prices['time'], unit='ms')
              volumes['time'] = pd.to_datetime(volumes['time'], unit='ms')
              market_caps['time'] = pd.to_datetime(market_caps['time'], unit='ms')

              # Merge the dataframes on the 'time' column
              merged_data = pd.merge(prices, volumes, on='time')
              merged_data = pd.merge(merged_data, market_caps, on='time')

              # Append to the main dataframe
              if data.empty:
                  data = merged_data
              else:
                  data = pd.merge(data, merged_data, on='time', how='outer')

              success = True

          except requests.HTTPError as http_err:
              if http_err.response.status_code == 429:
                  print(f"Rate limit exceeded, retrying in {retry_delay} seconds...")
                  time.sleep(retry_delay)
                  retry_delay *= 2  # Exponential backoff
                  retries += 1
              else:
                  print(f"HTTP error occurred: {http_err}")
                  break  # Break the loop for non-429 HTTP errors
          except Exception as err:
              print(f"An error occurred: {err}")
              break

      if not success:
          print(f"Failed to fetch data for {ticker} after {max_retries} retries.")
          continue

      # Delay between successful requests
      time.sleep(1)  # Wait for 1 second before the next API call

  # Set 'time' as the index and resample to fill missing days
  data.set_index('time', inplace=True)
  data = data.resample('D').ffill()
  data.reset_index(inplace=True)

  print("CoinGecko Crypto Data Call Completed")
  return data

def get_price(tickers, start_date):
    data = pd.DataFrame()
    for category, ticker_list in tickers.items():
      if category == 'crypto':
      # Skip the 'crypto' category
        continue
      for ticker in ticker_list:
            try:
                stock = si.get_data(ticker, start_date=start_date)
                stock = stock[['close']]  # Keep only the 'close' column
                stock.columns = [ticker + '_close']  # Rename the column
                stock = stock.resample('D').ffill()  # Resample to fill missing days
                if data.empty:
                    data = stock
                else:
                    data = data.join(stock)
            except Exception as e:
                print(f"Could not fetch data for {ticker} in category {category}. Reason: {str(e)}")
    data.reset_index(inplace=True)
    data.rename(columns={'index': 'time'}, inplace=True)  # rename 'date' to 'time'
    data['time'] = pd.to_datetime(data['time'])  # convert to datetime type
    print("Yahoo Finance Price Data Call Completed")
    return data

def get_marketcap(tickers, start_date):
  data = pd.DataFrame()
  end_date = pd.to_datetime('today') - pd.Timedelta(days=1)  # Adjust to 'yesterday' to ensure data availability

    for ticker in tickers['stocks']:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        market_cap = stock.info['marketCap']

        # Create a DataFrame for the market cap data
        mc_data = pd.DataFrame({
            'time': pd.date_range(start=start_date, end=end_date),
            f'{ticker}_MarketCap': [market_cap] * len(pd.date_range(start=start_date, end=end_date))
        })

        if data.empty:
            data = mc_data
        else:
            data = pd.merge(data, mc_data, on='time', how='outer')

    return data

def calculate_custom_on_chain_metrics(data):
# New Metrics Based On Coinmetrics Data
    data['mvrv_ratio'] = data['CapMrktCurUSD'] / data['CapRealUSD']
    data['realised_price'] = data['CapRealUSD'] / data['SplyCur']
    data['nupl'] = (data['CapMrktCurUSD'] - data['CapRealUSD']) / data['CapMrktCurUSD']
    data['nvt_price'] = (data['NVTAdj'].rolling(window=365*2).median() * data['TxTfrValAdjUSD']) / data['SplyCur']
    data['nvt_price_adj'] = (data['NVTAdj90'].rolling(window=365).median() * data['TxTfrValAdjUSD']) / data['SplyCur']
    data['nvt_price_multiple'] = data['PriceUSD'] / data['nvt_price']

    # Price Moving Averages
    data['7_day_ma_priceUSD'] = data['PriceUSD'].rolling(window=7).mean()
    data['50_day_ma_priceUSD'] = data['PriceUSD'].rolling(window=50).mean()
    data['100_day_ma_priceUSD'] = data['PriceUSD'].rolling(window=100).mean()
    data['200_day_ma_priceUSD'] = data['PriceUSD'].rolling(window=200).mean()
    data['200_week_ma_priceUSD'] = data['PriceUSD'].rolling(window=200 * 7).mean()

    # Price Multiple
    data['200_day_multiple'] = data['PriceUSD'] / data['200_day_ma_priceUSD']

    # Thermocap Multiple
    data['thermocap_multiple'] = data['CapMrktCurUSD'] / data['RevAllTimeUSD']
    data['thermocap_multiple_4'] = (4 * data['RevAllTimeUSD']) / data['SplyCur']
    data['thermocap_multiple_8'] = (8 * data['RevAllTimeUSD']) / data['SplyCur']
    data['thermocap_multiple_16'] = (16 * data['RevAllTimeUSD']) / data['SplyCur']
    data['thermocap_multiple_32'] = (32 *data['RevAllTimeUSD']) / data['SplyCur']
    data['thermocap_price'] = data['RevAllTimeUSD'] / data['SplyCur']

    # Realized Cap Multiple
    data['realizedcap_multiple_3'] = (3 * data['CapRealUSD']) / data['SplyCur']
    data['realizedcap_multiple_5'] = (5 * data['CapRealUSD']) / data['SplyCur']
    data['realizedcap_multiple_7'] = (7 * data['CapRealUSD']) / data['SplyCur']

    # 1+ Year Supply %
    data['supply_pct_1_year_plus'] = (100 - data['SplyActPct1yr'])
    data['illiquid_supply'] = ((data['supply_pct_1_year_plus'] / 100) *data['SplyCur'])
    data['liquid_supply'] = (data['SplyCur'] - data['illiquid_supply'])
    data['pct_supply_issued'] = (data['SplyCur'] /21000000)
    data['pct_fee_of_reward'] = (data['FeeTotUSD'] / (data['RevUSD']))

    print("Custom Metrics Created")
    return data

def calculate_moving_averages(data, metrics):
    # Calculate moving averages for each metric
    for metric in metrics:
        data[f'7_day_ma_{metric}'] = data[metric].rolling(window=7).mean()
        data[f'30_day_ma_{metric}'] = data[metric].rolling(window=30).mean()
        data[f'365_day_ma_{metric}'] = data[metric].rolling(window=365).mean()

    return data

def calculate_statistics(data, start_date):
    # Convert start_date to datetime
    start_date = pd.to_datetime(start_date)

    # Convert index to datetime
    data.index = pd.to_datetime(data.index)

    # Filter data to only include rows after start_date
    data = data[data.index >= start_date]

    # Calculate percentiles and z-scores
    numeric_data = data.select_dtypes(include=[np.number])
    percentiles = numeric_data.apply(lambda x: x.rank(pct=True))
    percentiles.columns = [str(col) + '_percentile' for col in percentiles.columns]
    z_scores = numeric_data.apply(lambda x: (x - x.mean()) / x.std())
    z_scores.columns = [str(col) + '_zscore' for col in z_scores.columns]
    return percentiles, z_scores

def calculate_rolling_correlations(data, periods):
  correlations = {}
  for period in periods:
    correlations[period] = data.rolling(window=period).corr()
  return correlations

def rolling_cagr_for_all_columns(data, years):
    # Convert index to datetime
    data.index = pd.to_datetime(data.index)

    # Calculate percentiles and z-scores
    data = data.select_dtypes(include=[np.number])

    days_per_year = 365  # Hard-coded value
    series_list = []

    for column in data.columns:
        start_value = data[column].shift(int(years * days_per_year))
        end_value = data[column]
        cagr = ((end_value / start_value) ** (1/years)) - 1
        series_list.append(cagr.rename(f"{column}_{years}_Year_CAGR"))

    cagr_data = pd.concat(series_list, axis=1)
    return cagr_data

def calculate_rolling_cagr_for_all_metrics(data):
    cagr_4yr = rolling_cagr_for_all_columns(data, 4)
    cagr_2yr = rolling_cagr_for_all_columns(data, 2)

    return pd.concat([cagr_4yr, cagr_2yr], axis=1)

def calculate_ytd_change(data):
  # Get the first day of the year for each date in the index
  start_of_year = data.index.to_series().apply(lambda x: pd.Timestamp(year=x.year, month=1, day=1))

  # Initialize an empty DataFrame for YTD change
  ytd_change = pd.DataFrame(index=data.index)

  # Get numeric columns
  numeric_cols = data.select_dtypes(include=[np.number]).columns

  # Calculate the YTD change only if the start of the year is in the index
  for date in data.index:
    if start_of_year[date] in data.index:
      ytd_change.loc[date, numeric_cols] = data.loc[date, numeric_cols] / data.loc[start_of_year[date], numeric_cols] - 1
    else:
      ytd_change.loc[date, numeric_cols] = np.nan

  # Rename columns
  ytd_change.columns = [f"{col}_YTD_change" for col in ytd_change.columns]
  return ytd_change

def calculate_mtd_change(data):
  # Get the first day of the month for each date in the index
  start_of_month = data.index.to_series().apply(lambda x: pd.Timestamp(year=x.year, month=x.month, day=1))

  # Initialize an empty DataFrame for MTD change
  mtd_change = pd.DataFrame(index=data.index)

  # Get numeric columns
  numeric_cols = data.select_dtypes(include=[np.number]).columns

  # Calculate the MTD change only if the start of the month is in the index
  for date in data.index:
    if start_of_month[date] in data.index:
      mtd_change.loc[date, numeric_cols] = data.loc[date, numeric_cols] / data.loc[start_of_month[date], numeric_cols] - 1
    else:
      mtd_change.loc[date, numeric_cols] = np.nan

  # Rename columns
  mtd_change.columns = [f"{col}_MTD_change" for col in mtd_change.columns]
  return mtd_change

def calculate_trading_week_change(data):
  # Determine the Monday of the week for each date
  start_of_week = data.index - pd.to_timedelta(data.index.dayofweek, unit='d')

  # Map each date to the Monday of its week
  monday_map = {date: start_of_week_date for date, start_of_week_date in zip(data.index, start_of_week)}

  # Initialize an empty DataFrame for trading week change
  trading_week_change = pd.DataFrame(index=data.index)

  # Get numeric columns
  numeric_cols = data.select_dtypes(include=[np.number]).columns

  # Calculate the trading week change for each day
  for date in data.index:
      monday_of_week = monday_map[date]
      for col in numeric_cols:
          if monday_of_week in data.index:
              monday_value = data.at[monday_of_week, col]
              current_value = data.at[date, col]
              if pd.notnull(monday_value) and pd.notnull(current_value):
                  trading_week_change.at[date, col] = (current_value / monday_value) - 1

  # Forward fill the NaN values with the last valid trading week change
  trading_week_change.ffill(inplace=True)

  # Rename columns
  trading_week_change.columns = [f"{col}_trading_week_change" for col in trading_week_change.columns]

  return trading_week_change
  
def calculate_yoy_change(data):
  # Calculate the year-over-year change for each date in the index
  yoy_change = data.pct_change(periods=365)  # Assuming data is daily

  # Rename columns
  yoy_change.columns = [f"{col}_YOY_change" for col in yoy_change.columns]

  return yoy_change

def calculate_time_changes(data, periods):
  changes = pd.DataFrame(index=data.index)
  numeric_data = data.select_dtypes(include=[np.number])  # only include numeric columns
  for period in periods:
    for column in numeric_data.columns:
      changes_temp = numeric_data[column].pct_change(periods=period)
      changes_temp.name = column + f'_{period}_change'
      changes = pd.concat([changes, changes_temp], axis=1)
  return changes

def get_data(tickers, start_date):
  coindata = get_coinmetrics_onchain('btc.csv')
  coindata['time'] = pd.to_datetime(coindata['time'])  # convert to datetime type
  prices = get_price(tickers, start_date)
  marketcaps = get_marketcap(tickers, start_date)
  fear_greed_index = get_fear_and_greed_index()
  bitcoin_dominance = get_bitcoin_dominance()
  btc_trade_volume_14d = get_btc_trade_volume_14d()
  crypto_data = get_crypto_data(tickers['crypto'])


  data = pd.merge(coindata, prices, on='time', how='left')
  data = pd.merge(data, marketcaps, on='time', how='left')
  data = pd.merge(data, fear_greed_index, on='time', how='left')
  data = pd.merge_asof(data.sort_index(), bitcoin_dominance.sort_index(), on='time', direction='nearest')
  data = pd.merge(data, btc_trade_volume_14d, on='time', how='left')
  data = pd.merge(data, crypto_data, on='time', how='left')


  # Set the index to 'time'
  data.set_index('time', inplace=True)

  print("All Raw Data Has Been Fetched & Mergered")
  return data

def calculate_all_changes(data):
  # Define the periods for which we want to calculate changes
  periods = [1,7, 30, 90, 365, 2 * 365, 3 * 365, 4 * 365, 5 * 365]

  # Get the original columns
  original_columns = list(data.columns)

  # Calculate changes for these periods
  changes = calculate_time_changes(data, periods)

  # Calculate YTD changes
  ytd_change = calculate_ytd_change(data[original_columns])

  # Calculate MTD changes
  mtd_change = calculate_mtd_change(data[original_columns])

  tw_change = calculate_trading_week_change(data[original_columns])

  # Concatenate all changes at once to avoid DataFrame fragmentation
  changes = pd.concat([changes, ytd_change, mtd_change, tw_change], axis=1)
  return changes

def run_data_analysis(data, start_date):
  # Calculate changes
  changes = calculate_all_changes(data)

  # Calculate statistics
  percentiles, z_scores = calculate_statistics(data, start_date)

  # Merge changes and statistics into data
  data = pd.concat([data, changes, percentiles, z_scores], axis=1)

  print("Data Analysis Complete")
  return data

def calculate_metrics_change(difficulty_report, df):
    # Ensure the DataFrame is sorted by date
    df = df.sort_index()

    # Convert the Unix timestamps to datetime format
    last_difficulty_change_time = pd.to_datetime(difficulty_report['last_difficulty_change']['timestamp'], unit='s')
    previous_difficulty_change_time = pd.to_datetime(difficulty_report['previous_difficulty_change']['timestamp'], unit='s')

    # Filter the DataFrame for the time period between the last two difficulty adjustments
    df_filtered = df.loc[previous_difficulty_change_time:last_difficulty_change_time]

    # Calculate the percentage change in metrics
    percentage_changes = ((df_filtered.iloc[-1] - df_filtered.iloc[0]) / df_filtered.iloc[0] * 100).round(2)
    return percentage_changes

def create_btc_correlation_tables(report_date, tickers, correlations_data):
    # Combine all tickers across categories
    all_tickers = [ticker for ticker_list in tickers.values() for ticker in ticker_list]

    # Add the '_close' suffix and include 'PriceUSD'
    ticker_list_with_suffix = ['PriceUSD'] + [f"{ticker}_close" for ticker in all_tickers]

    # Filter the correlation data for the tickers
    filtered_data = correlations_data[ticker_list_with_suffix]

    # Drop NA values
    filtered_data = filtered_data.dropna()

    # Calculate the correlations
    correlations = calculate_rolling_correlations(filtered_data, periods=[7, 30, 90, 365])

    # Extract only the 'PriceUSD' row from each correlation matrix
    btc_correlations = {
        "priceusd_7_days": correlations[7].loc[report_date].loc[['PriceUSD']],
        "priceusd_30_days": correlations[30].loc[report_date].loc[['PriceUSD']],
        "priceusd_90_days": correlations[90].loc[report_date].loc[['PriceUSD']],
        "priceusd_365_days": correlations[365].loc[report_date].loc[['PriceUSD']]
    }

    return btc_correlations

def calculate_price_buckets(data, bucket_size):
  # Ensure the data index (presumed to be time) is sorted
  data = data.sort_index(ascending=True)

  # Define the bucket ranges for price intervals
  bucket_ranges = pd.interval_range(start=0, end=(data['PriceUSD'].max() // bucket_size + 1) * bucket_size, freq=bucket_size)

  # Assign each price to a bucket
  data['PriceBucket'] = pd.cut(data['PriceUSD'], bins=bucket_ranges)

  # Calculate the number of unique index values (dates) in each bucket
  bucket_days_count = data.groupby('PriceBucket').apply(lambda x: x.index.nunique())

  # Getting the current price and its bucket
  current_price = data['PriceUSD'].iloc[-1]
  current_bucket = pd.cut([current_price], bins=bucket_ranges)[0]

  # Extracting the count of days for the current price bucket
  current_bucket_days = bucket_days_count[current_bucket]

  # Create DataFrame for current price data with bucket and days count
  current_price_data = pd.DataFrame({
      'Current Bitcoin Price (USD)': [current_price],
      f'Current {bucket_size} Price Bucket': [f"${int(current_bucket.left/1000)}K-${int(current_bucket.right/1000)}K"],
      'Days in Current Bucket': [current_bucket_days]
  })

  # Saving the current price data to a CSV file
  current_price_data.to_csv(f'supplemental_trading_range_data_{bucket_size}.csv', index=False)

  # Count the number of entries in each bucket (not days)
  bucket_counts = data['PriceBucket'].value_counts().sort_index()

  # Create a DataFrame for the bucket counts
  bucket_counts_df = bucket_counts.reset_index()
  bucket_counts_df.columns = ['Price Range ($)', 'Count']
  bucket_counts_df['Price Range ($)'] = bucket_counts_df['Price Range ($)'].apply(
      lambda x: f"${int(x.left/1000)}K-${int(x.right/1000)}K"
  )

  return bucket_counts_df


def style_bucket_counts_table(bucket_counts_df):
  # Define the style for the table: smaller font size
  table_style = [
      {
          'selector': 'th',
          'props': 'font-size: 12px;'  # Adjust header font size
      },
      {
          'selector': 'td',
          'props': 'font-size: 12px;'  # Adjust cell font size
      }
  ]

  # Apply the style to the table and hide the index
  styled_table = (
      bucket_counts_df.style
      .set_table_styles(table_style)
      .hide_index()
  )

  return styled_table

def create_price_buckets_chart(bucket_counts_df):
    # Exclude the 0-1K range from the plotting data
    plot_data = bucket_counts_df[bucket_counts_df['Price Range ($)'] != '$0K-$1K'].copy()

    # Convert the 'Price Range ($)' to a sortable numeric value
    plot_data['Sort Key'] = plot_data['Price Range ($)'].apply(lambda x: int(x.split('-')[0][1:-1]))

    # Sort the DataFrame by 'Sort Key' in descending order
    plot_data = plot_data.sort_values(by='Sort Key', ascending=False)

    # Create the bar chart using Plotly
    fig = px.bar(plot_data, y='Price Range ($)', x='Count',  # Change 'Days Count' to 'Count'
                 orientation='h',  # Makes the bars horizontal
                 color='Count',  # Use 'Count' as the color scale
                 color_continuous_scale='Viridis',  # Choose a color scale
                 title='Number of Days Bitcoin Traded within 1K Price Ranges')

    # Update figure layout
    fig.update_layout(
        height=500,
        width=800,
        margin=dict(l=5, r=5, t=50, b=5)
    )

    # Create a Datapane Plot object
    dp_chart = dp.Plot(fig)

    # Return the Datapane object
    return dp_chart

def monthly_heatmap(data):
  # Filter data to start from 2011
  data = data[data.index >= pd.to_datetime('2010-12-01')]
  # Calculate monthly returns
  monthly_returns = data['PriceUSD'].resample('M').last().pct_change()
  # Calculate yearly returns
  yearly_returns = data['PriceUSD'].resample('A').last().pct_change()

  # Prepare the data for the heatmap (years as rows, months as columns)
  heatmap_data = monthly_returns.groupby([monthly_returns.index.year, monthly_returns.index.month]).mean().unstack()

  # Add the yearly returns as an additional '13th' month for each year
  heatmap_data[13] = yearly_returns.groupby(yearly_returns.index.year).mean()

  # Add the average return for each month at the bottom
  heatmap_data.loc['Average'] = heatmap_data.mean(axis=0)

  # Replace month numbers with names for better readability
  month_names = [calendar.month_abbr[i] for i in range(1, 13)] + ['Yearly']
  heatmap_data.columns = month_names
  heatmap_data.index = heatmap_data.index.astype(str)  # Convert index to string for Plotly
  heatmap_data.to_csv('monthly_heatmap_data.csv')

  # Flatten the heatmap data for text annotations
  text_values = heatmap_data.applymap(lambda x: f"{x:.2%}" if pd.notnull(x) else '').values
  # Define the traditional red-yellow-green colorscale

  # Create Plotly figure
  fig = go.Figure(data=go.Heatmap(
      z=heatmap_data.values,
      x=heatmap_data.columns,
      y=heatmap_data.index,
      colorscale='RdYlGn',
      zmin=-1,  # Set the minimum value for the colorscale
      zmax=1,
      zmid=0,  # Set the midpoint for the colorscale to 0
      text=text_values,
      hoverinfo="text",
      texttemplate="%{text}"
  ))

  # Update layout
  fig.update_layout(
      title="Bitcoin Monthly & Yearly Returns Heatmap",
      xaxis_nticks=36,
      yaxis_nticks=24,
      autosize=False,  # This can be set to False if you want to define custom width and height
      width=1200,  # Custom width (in pixels)
      height=600,  # Custom height (in pixels)
  )

  dp_chart = dp.Plot(fig)

  # Return the Plotly figure
  return dp_chart

def weekly_heatmap(data, last_n_years=5):
  # Filter the data for the last N years
  start_date = datetime.now() - pd.DateOffset(years=last_n_years)
  data_last_n_years = data.loc[start_date:]

  # Calculate weekly returns including the current partial week
  weekly_returns = data_last_n_years['PriceUSD'].resample('W').ffill().pct_change()

  # Group by week and year
  grouped = weekly_returns.groupby([weekly_returns.index.isocalendar().week, weekly_returns.index.isocalendar().year])

  # Exclude the 53rd week if not present in all years
  if len(grouped.get_group((53, )) if (53, ) in grouped.groups else []) < last_n_years:
      weekly_returns = weekly_returns[weekly_returns.index.isocalendar().week != 53]

  # Heatmap data
  heatmap_data = weekly_returns.groupby([weekly_returns.index.isocalendar().week, weekly_returns.index.isocalendar().year]).mean().unstack()

  # Calculate the average return for each week
  heatmap_data['Average'] = heatmap_data.mean(axis=1)
  
  # Current and past week number
  current_week = datetime.now().isocalendar()[1]
  past_week = current_week - 1 if current_week > 1 else 52

  # Next week number
  next_week = current_week + 1 if current_week < 52 else 1

  # Prepare supplemental data
  supplemental_data = {
      'Todays Date': data.index[-1],
      'Current Week Number': current_week,
      'Next Week Number': next_week,
      'Next Week Avg Return': heatmap_data['Average'].get(next_week, float('nan')),
      'Past Week 5-Year Avg Return': heatmap_data['Average'].get(past_week, float('nan')),
      'Current Week 5-Year Avg Return': heatmap_data['Average'].get(current_week, float('nan'))
  }

  # Convert supplemental data to DataFrame and save to CSV
  supplemental_df = pd.DataFrame([supplemental_data])
  supplemental_df.to_csv('supplemental_data_weekly_heatmap.csv', index=False)
  
  # Convert indices and columns to strings for Plotly
  heatmap_data.columns = heatmap_data.columns.astype(str)
  heatmap_data.index = heatmap_data.index.astype(str)
  heatmap_data.to_csv('weekly_heatmap_data.csv')

  # Flatten the heatmap data for text annotations
  text_values = heatmap_data.applymap(lambda x: f"{x:.2%}" if pd.notnull(x) else '').values

  # Create Plotly figure
  fig = go.Figure(data=go.Heatmap(
      z=heatmap_data.values,  # Do not transpose values here
      y=heatmap_data.index,   # Weeks are now on the y-axis
      x=heatmap_data.columns, # Years are now on the x-axis
      colorscale='RdYlGn',
      zmin=-0.1,  # Set the minimum value for the colorscale
      zmax=0.1,   # Set the maximum value for the colorscale
      zmid=0,     # Set the midpoint for the colorscale to 0
      text=text_values,
      hoverinfo="text",
      texttemplate="%{text}"
  ))

  # Update layout
  fig.update_layout(
      title="Bitcoin Weekly Returns Heatmap (Last {} Years)".format(last_n_years),
      xaxis_title="Years",
      yaxis_title="Weeks",
      xaxis_nticks=10,
      yaxis_nticks=50,  # Adjust to the number of weeks in a year
      autosize=False,
      width=800,
      height=800,
      margin=dict(l=10, r=10, t=50, b=50)  # Adjust the margin values as needed
  )
  dp_chart = dp.Plot(fig)
  # Return the Plotly figure
  return dp_chart

def plot_yoy_change(data, column_name):
  # Filter the data from 2012 onwards
  data_since_2012 = data[data.index.year >= 2012]

  # Create the figure and first axis
  fig, ax1 = plt.subplots(figsize=(14, 7))

  # Get the most recent YOY change and Bitcoin price
  latest_yoy_change = data_since_2012[column_name].iloc[-1]
  latest_bitcoin_price = data_since_2012['PriceUSD'].iloc[-1]

  # Format the latest YOY change and Bitcoin price for the legend
  yoy_legend_label = f'YOY Change (latest: {latest_yoy_change:.0%})'
  btc_price_legend_label = f'Bitcoin Price (latest: ${latest_bitcoin_price:,.2f})'


  # Plot the YOY data on ax1
  ax1.plot(data_since_2012.index, data_since_2012[column_name], label=yoy_legend_label, color='tab:blue')
  ax1.set_yscale('symlog', linthresh=1)  # Set the y-axis to symlog scale
  ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))  # Format as percentages
  ax1.set_xlabel('Year')
  ax1.set_ylabel('Percent Change', color='tab:blue')
  ax1.tick_params(axis='y', labelcolor='tab:blue')
  ax1.grid(True, which="both", ls="--", linewidth=0.5)
  ax1.set_title('Bitcoin Year-Over-Year Change and Price on Log Scale')

  # Create a second y-axis for the bitcoin price with log scale
  ax2 = ax1.twinx()
  ax2.plot(data_since_2012.index, data_since_2012['PriceUSD'], label=btc_price_legend_label, color='tab:orange')
  ax2.set_yscale('log')  # Set the y-axis to log scale
  # Custom formatter to convert log scale back to original scale and format as currency


  # Add legends
  lines, labels = ax1.get_legend_handles_labels()
  lines2, labels2 = ax2.get_legend_handles_labels()
  ax1.legend(lines + lines2, labels + labels2, loc='upper left')

  #plt.tight_layout()  # Adjust the plot to ensure a tight fit
  # Save the plot as a PNG file
  png_filename = 'log_return_yoy.png'
  fig.savefig(png_filename)

  dp.Plot(fig)

  return fig

def calculate_roi_table(data, report_date, price_column='PriceUSD'):
  if price_column not in data.columns:
      raise ValueError(f"The price column '{price_column}' does not exist in the data.")

  if data.empty:
      raise ValueError("The input data is empty.")

  periods = {
      '1 day': 1,
      '3 day': 3,
      '7 day': 7,
      '30 day': 30,
      '90 day': 90,
      '1 Year': 365,
      '2 Year': 730,
      '4 Year': 1460,
      '5 Year': 1825,
      '10 Year': 3650
  }

  today = pd.to_datetime(report_date).normalize()

  # Pre-compute the 'Start Date' and 'BTC Price' for each period
  start_dates = {period: today - pd.Timedelta(days=days) for period, days in periods.items()}
  btc_prices = {period: data.loc[start_dates[period], price_column] if start_dates[period] in data.index else None for period in periods}

  roi_data = {period: data[price_column].pct_change(days).iloc[-1] * 100 for period, days in periods.items()}

  # Combine the ROI, Start Dates, and BTC Prices into a DataFrame
  roi_table = pd.DataFrame({
      'Time Frame': periods.keys(),
      'ROI': roi_data.values(),
      'Start Date': start_dates.values(),
      'BTC Price': btc_prices.values()
  })
  roi_table.to_csv("roi_table.csv")
  return roi_table.set_index('Time Frame')

def calculate_ma_table(data, price_column='PriceUSD'):
  periods = {
      '3 Day MA': 3,
      '7 Day MA': 7,
      '30 Day MA': 30,
      '50 Day MA': 50,
      '100 Day MA': 100,
      '200 Day MA': 200,
      '50 Week MA': 50*7,
      '200 Week MA': 200*7,
      '50 Month MA': 50*30,
  }

  ma_data = {
      period: {
          'Price': data[price_column].rolling(window=days).mean().iloc[-1],
          '7 Day % Change': ((data[price_column].rolling(window=days).mean().iloc[-1] /
                                  data[price_column].rolling(window=days).mean().iloc[-8]) - 1) * 100
      } for period, days in periods.items()
  }
  ma_data['Current Price'] = {
      'Price': data[price_column].iloc[-1],
      '7 Day % Change': ((data[price_column].iloc[-1] / data[price_column].iloc[-8]) - 1) * 100
  }
  ma_table = pd.DataFrame.from_dict(ma_data, orient='index')
  ma_table.index.name = 'Moving Average'
  ma_table.to_csv("ma_table.csv")
  return ma_table[['Price', '7 Day % Change']]

def style_roi_table(roi_table):
# Function to color ROI values
  def color_roi(val):
      color = 'green' if val > 0 else ('red' if val < 0 else 'black')
      return 'color: %s' % color

  # Function to format BTC Price as currency
  def format_currency(val):
      return "${:,.2f}".format(val)

  return (roi_table.style
        .applymap(color_roi, subset=['ROI'])
        .format({"ROI": "{:.2f}%",  # Format ROI as percentage with 2 decimal places
                 "BTC Price": format_currency})  # Format BTC Price as currency
        .set_properties(**{'font-size': '10pt'}))

def style_ma_table(ma_table):
  # Function to color percentage values
  def color_percentage(val):
    color = 'green' if val > 0 else ('red' if val < 0 else 'black')
    return 'color: %s' % color

    # Apply the specific formatting and coloring

  return (ma_table.style
        .format({
            "Price": "${:,.2f}",  # Format 'Bitcoin Price' as currency with two decimal places
            "7 Day % Change": "{:.2f}%",  # Format '7 Day Avg % Change' as percentage with two decimal places
        })
        .applymap(color_percentage, subset=['7 Day % Change'])  # Color the '7 Day Avg % Change' based on value
        .set_properties(**{'font-size': '10pt'}))  # Set font size to 10pt

def calculate_weekly_values(df, column_name, start_of_week, latest_date):
    weekly_values = []
    for i in range(5):  # For Monday to Friday
        day_date = start_of_week + timedelta(days=i)
        if day_date <= latest_date:
            daily_value = df.loc[df.index.date == day_date.date(), column_name].mean()
            weekly_values.append(daily_value)
        else:
            weekly_values.append(None)  # Empty if the day has not yet occurred
    week_total = df.loc[(df.index.date >= start_of_week.date()) & (df.index.date <= latest_date.date()), column_name].sum()
    return weekly_values, week_total

def create_metrics_table(df, metrics_template):
  # Formatting functions for different data types
  def format_number(value):
      return f"{value:,.0f}" if pd.notnull(value) else ''
    
  def format_number2(value):
    return f"{value:,.2f}" if pd.notnull(value) else ''

  def format_currency(value):
      return f"${value:,.2f}" if pd.notnull(value) else ''

  def format_percent(value):
      return f"{value:.2f}%" if pd.notnull(value) else ''

  def format_percent_change(value):
      color = 'red' if value < 0 else 'green'
      return f"<span style='color:{color};'>{value:.2f}%</span>"

  # Apply formatting based on the data type
  def apply_formatting(column, format_type):
      if format_type == 'number':
          return column.apply(format_number)
      elif format_type == 'number2':
        return column.apply(format_number2)
      elif format_type == 'currency':
          return column.apply(format_currency)
      elif format_type == 'percent':
          return column.apply(format_percent)
      elif format_type == 'percent_change':
          return column.apply(format_percent)

  # Initialize a list to hold the calculated values
  table_data = []

  # Get the most recent date in the DataFrame for current week calculations
  latest_date = df.index.max()
  start_of_week = latest_date - timedelta(days=latest_date.weekday())  # Monday
  # Loop through each section and metric
  header_style_indices = []  # List to store the indices of header rows
  index_counter = 0  # Counter to keep track of the row index
  # Loop through each section and metric
  for section, metrics in metrics_template.items():
      # Add the section header
      table_data.append({
          'Metric': f"<strong'>{section}</strong>",
          '7 Day Avg': '-',
          '7 Day Avg % Change': '-',
          'Monday': '-',
          'Tuesday': '-',
          'Wednesday': '-',
          'Thursday': '-',
          'Friday': '-',
      })
      header_style_indices.append(index_counter)  # Add the current index to the list
      index_counter += 1  # Increment the counter after adding the header

      for metric_display_name, (column_name, format_type) in metrics.items():
          # Calculate the metrics
          week_avg = df[column_name].tail(7).mean()
          prev_week_avg = df[column_name].tail(14).head(7).mean()
          pct_change = ((week_avg - prev_week_avg) / prev_week_avg) * 100 if prev_week_avg != 0 else np.nan
          weekly_values = df[column_name][start_of_week:latest_date].tolist()

          # Add the metric data with formatting
          table_data.append({
              'Metric': metric_display_name,
              '7 Day Avg': apply_formatting(pd.Series([week_avg]), format_type)[0],
              '7 Day Avg % Change': apply_formatting(pd.Series([pct_change]), 'percent_change')[0],
              'Monday': apply_formatting(pd.Series([weekly_values[0] if weekly_values else None]), format_type)[0],
              'Tuesday': apply_formatting(pd.Series([weekly_values[1] if len(weekly_values) > 1 else None]), format_type)[0],
              'Wednesday': apply_formatting(pd.Series([weekly_values[2] if len(weekly_values) > 2 else None]), format_type)[0],
              'Thursday': apply_formatting(pd.Series([weekly_values[3] if len(weekly_values) > 3 else None]), format_type)[0],
              'Friday': apply_formatting(pd.Series([weekly_values[4] if len(weekly_values) > 4 else None]), format_type)[0]
          })
          index_counter += 1  # Increment the counter after adding the header


  # Create DataFrame
  table_df = pd.DataFrame(table_data)

  # Apply a style to the DataFrame to hide index and set text size
  styled_table = table_df.style.hide_index().set_properties(**{
      'font-size': '10pt',
      'white-space': 'nowrap'
  })

  # Define styles for the header rows
  header_styles = [{
      'selector': f'.row{row_index}',
      'props': [('border-top', '1px solid black'), ('border-bottom', '1px solid black')]
  } for row_index in header_style_indices]

  # Apply the styles for the header rows
  styled_table = styled_table.set_table_styles(header_styles, overwrite=False)

  return styled_table

def create_ohlc_chart(ohlc_data, report_data, chart_template):
  # Unpack variables from the chart template
    title = chart_template['title']
    x_label = chart_template['x_label']
    y_label = chart_template['y1_label']
    filename = chart_template['filename']

    # Create an OHLC chart
    fig = go.Figure(data=[go.Candlestick(x=ohlc_data['Time'],
                                         open=ohlc_data['Open'],
                                         high=ohlc_data['High'],
                                         low=ohlc_data['Low'],
                                         close=ohlc_data['Close'],
                                         name=f'Weekly Price')])
    # Add the Moving Average to the chart
    report_data = report_data[(report_data.index >= '2017-09-01')]
    fig.add_trace(go.Scatter(x=report_data.index, y=report_data['200_week_ma_priceUSD'], mode='lines', name=f'200 Week MA'))
    # Add additional traces for each metric
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['realised_price'], 
        mode='lines', 
        name='Realized Price'
    ))
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['realizedcap_multiple_3'], 
        mode='lines', 
        name='3x Realized Price'
    ))
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['realizedcap_multiple_5'], 
        mode='lines', 
        name='5x Realized Price'
    ))
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['thermocap_multiple_8'], 
        mode='lines', 
        name='8x Thermocap Price'
    ))
  
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['thermocap_multiple_16'], 
        mode='lines', 
        name='16x Thermocap Price'
    ))
    fig.add_trace(go.Scatter(
        x=report_data.index, 
        y=report_data['thermocap_multiple_32'], 
        mode='lines', 
        name='32x Thermocap Price'
    ))
  
    # Update the layout of the figure with various styling options
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', y=0.95),
        xaxis_title=x_label,
        yaxis_title=y_label,
        yaxis=dict(showgrid=False, type='log', autorange=True),
        plot_bgcolor='rgba(255, 255, 255, 1)',
        xaxis=dict(showgrid=False,
                  tickformat='%B-%d-%Y',
                  rangeslider_visible=False,
                  rangeselector=dict(buttons=list([
                       dict(count=1, label="1m", step="month", stepmode="backward"),
                       dict(count=6, label="6m", step="month", stepmode="backward"),
                       dict(count=1, label="YTD", step="year", stepmode="todate"),
                       dict(count=1, label="1y", step="year", stepmode="backward"),
                       dict(count=2, label="2y", step="year", stepmode="backward"),
                       dict(count=3, label="3y", step="year", stepmode="backward"),
                       dict(count=5, label="5y", step="year", stepmode="backward"),
                       dict(step="all")
                   ])),
                  autorange=True),
        hovermode='x',
        autosize=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.23, xanchor='center', x=0.5),
        template='plotly_white',
        updatemenus=[
            go.layout.Updatemenu(buttons=list([
                dict(label="Y1-axis: Linear", method="relayout", args=["yaxis.type", "linear"]),
                dict(label="Y1-axis: Log", method="relayout", args=["yaxis.type", "log"]),
            ]), showactive=False, type="buttons", direction="right", x=-0.1, xanchor="left", y=-0.25, yanchor="top")
        ],
        width=1400,
        height=700,
        margin=dict(l=50, r=50, b=50, t=50, pad=50),
        font=dict(family="PT Sans Narrow", size=14, color="black")
    )

    # Add event annotations and lines, similar to line chart template
    if 'events' in chart_template:
        for event in chart_template['events']:
            event_dates = pd.to_datetime(event['dates'])
            for date in event_dates:
                fig.add_vline(x=date.timestamp() * 1000, line=dict(color="black", width=1, dash="dash"))
                fig.add_annotation(x=date, y=0.5, text=event['name'], showarrow=False, yref="paper")

    # Add watermark
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=0.5, text="SecretSatoshis.com",
                       showarrow=False, font=dict(size=50, color="rgba(128, 128, 128, 0.5)"), align="center")
    # Extract the latest data point for each metric
    latest_data = report_data.iloc[-1]
    latest_ohlc = ohlc_data.iloc[-1]

    annotation_text_price = (
        f"Latest Weekly Candle:<br>"
        f"Open: ${latest_ohlc['Open']:.2f}<br>"
        f"High: ${latest_ohlc['High']:.2f}<br>"
        f"Low: ${latest_ohlc['Low']:.2f}<br>"
        f"Close: ${latest_ohlc['Close']:.2f}"
    )
    annotation_text_support = (
        f"Support Levels:<br>"
        f"Realized Price: ${latest_data['realised_price']:.2f}<br>"
        f"16x Thermocap Price: ${latest_data['thermocap_multiple_16']:.2f}<br>"
        f"200 Week MA: ${latest_data['200_week_ma_priceUSD']:.2f}"
    )
    annotation_text_resistance = (
        f"Resistance Levels:<br>"
        f"16x Thermocap Price: ${latest_data['thermocap_multiple_16']:.2f}<br>"
        f"3x Realized Price: ${latest_data['realizedcap_multiple_3']:.2f}<br>"
        f"32x Thermocap Price: ${latest_data['thermocap_multiple_32']:.2f}<br>"
        f"5x Realized Price: ${latest_data['realizedcap_multiple_5']:.2f}"
    )
    
    # Define the annotation properties
    annotation_props_price = dict(
        xref="paper", yref="paper",
        x=0.02, y=0.98,  # Position (top left corner)
        xanchor="left", yanchor="top",
        text=annotation_text_price,
        showarrow=False,
        align="left",
        bordercolor="#c7c7c7",
        borderwidth=2,
        bgcolor="lightgrey",
        opacity=0.5,  # Set opacity to 0.5
        font=dict(family="Arial", size=11)
    )

    annotation_props_support = dict(
        xref="paper", yref="paper",
        x=0.15, y=0.98,  # Position (top left corner)
        xanchor="left", yanchor="top",
        text=annotation_text_support,
        showarrow=False,
        align="left",
        bordercolor="#c7c7c7",
        borderwidth=2,
        bgcolor="lightgrey",
        opacity=0.5,  # Set opacity to 0.5
        font=dict(family="Arial", size=11)
    )

    annotation_props_resistance = dict(
        xref="paper", yref="paper",
        x=0.33, y=0.98,  # Position (top left corner)
        xanchor="left", yanchor="top",
        text=annotation_text_resistance,
        showarrow=False,
        align="left",
        bordercolor="#c7c7c7",
        borderwidth=2,
        bgcolor="lightgrey",
        opacity=0.5,  # Set opacity to 0.5
        font=dict(family="Arial", size=11)
    )

    # Add the annotation to the figure
    fig.add_annotation(annotation_props_price)
    fig.add_annotation(annotation_props_support)
    fig.add_annotation(annotation_props_resistance)
    # Save the chart as an HTML file
    dp_chart = dp.Plot(fig)
    
    # Return the figure
    return dp_chart
  
def create_ohlc_chart_matplotlib(ohlc_data, report_data, chart_template):
    # Convert 'Time' to a format suitable for Matplotlib
    ohlc_data['Time'] = pd.to_datetime(ohlc_data['Time'])
    ohlc_data.set_index('Time', inplace=True)
  
    # Prepare the OHLC data for mplfinance
    ohlc = ohlc_data[['Open', 'High', 'Low', 'Close']]
  
    # Create a new figure and axes
    fig, ax = plt.subplots(figsize=(16, 9))
    report_data = report_data[(report_data.index >= '2017-09-01')]
    # Plot candlestick chart using mplfinance
    mpf.plot(ohlc, type='candle', ax=ax, style='charles', show_nontrading=True)
    # Set y-axis to logarithmic scaled
    ax.set_yscale('log')
    # Get the latest data point
    latest_data = report_data.iloc[-1]
  
    # Plot additional data like moving averages with dynamic labels
    ax.plot(report_data.index, report_data['200_week_ma_priceUSD'], label=f'200 Week MA: {latest_data["200_week_ma_priceUSD"]:.2f}')
    ax.plot(report_data.index, report_data['realised_price'], label=f'Realized Price: {latest_data["realised_price"]:.2f}')
    ax.plot(report_data.index, report_data['realizedcap_multiple_3'], label=f'3x Realized Price: {latest_data["realizedcap_multiple_3"]:.2f}')
    ax.plot(report_data.index, report_data['realizedcap_multiple_5'], label=f'5x Realized Price: {latest_data["realizedcap_multiple_5"]:.2f}')
    ax.plot(report_data.index, report_data['thermocap_multiple_8'], label=f'8x Thermocap Price: {latest_data["thermocap_multiple_8"]:.2f}')
    ax.plot(report_data.index, report_data['thermocap_multiple_16'], label=f'16x Thermocap Price: {latest_data["thermocap_multiple_16"]:.2f}')
    ax.plot(report_data.index, report_data['thermocap_multiple_32'], label=f'32x Thermocap Price: {latest_data["thermocap_multiple_32"]:.2f}')
  
    # Add event annotations and lines
    if 'events' in chart_template:
        for event in chart_template['events']:
            event_dates = pd.to_datetime(event['dates'])
            for date in event_dates:
                ax.axvline(x=date, color="black", linestyle="--")
                ax.annotate(event['name'], xy=(mdates.date2num(date), ax.get_ylim()[0]), xytext=(10,0), 
                            textcoords='offset points', arrowprops=dict(arrowstyle='->'))
  
    # Customize the chart
    ax.set_title(chart_template['title'])
    ax.set_xlabel(chart_template['x_label'])
    ax.set_ylabel(chart_template['y1_label'])
    ax.legend()
    ax.xaxis_date()  # Set x-axis to display dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.grid(True)
  
    # Save the chart
    plt.savefig("ohlc_chart.png",dpi=300)
  
