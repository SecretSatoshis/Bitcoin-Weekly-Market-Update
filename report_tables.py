import datapane as dp
import pandas as pd
import seaborn as sns
from datetime import date

# Create Summary Table
def create_weekly_summary_table(report_data, report_date):
  # Extract data from report_data for the specific date
  report_date_data = report_data.loc[report_date].name
  bitcoin_supply = report_data.loc[report_date, 'SplyCur']
  HashRate = report_data.loc[report_date, '7_day_ma_HashRate']
  PriceUSD = report_data.loc[report_date, 'PriceUSD']
  Marketcap = report_data.loc[report_date, 'CapMrktCurUSD']
  sats_per_dollar = 100000000 / report_data.loc[report_date, 'PriceUSD']
  btc_dominance = report_data.loc[report_date, 'bitcoin_dominance']
  btc_volume = report_data.loc[report_date, 'btc_trading_volume']
  fear_greed = report_data.loc[report_date, 'value_classification']
  bitcoin_trend = "Bullish"
  bitcoin_valuation = "Fair Value"

  # Create a dictionary with the extracted values
  weekly_update_data = {
      "Bitcoin Price USD": PriceUSD,
      "Report Date": report_date_data,
      "Bitcoin Marketcap": Marketcap,
      "Sats Per Dollar": sats_per_dollar,
      "Bitcoin Dominance": btc_dominance,
      "24HR Bitcoin Trading Volume": btc_volume,
      "Bitcoin Market Sentiment": fear_greed,
      "Bitcoin Market Trend": bitcoin_trend,
      "Bitcoin Valuation": bitcoin_valuation,
  }

  # Create and return the "Difficulty Update" DataFrame
  weekly_summary_df = pd.DataFrame([weekly_update_data])
  return weekly_summary_df

#Style Table
def format_value(value, format_type):
  """Helper function to format a value based on the format_type"""
  if format_type == "percentage":
    return f"{value:.2f}%"
  elif format_type == "integer":
    return f"{int(value):,}"
  elif format_type == "float":
    return f"{value:,.0f}"
  elif format_type == "currency":
    return f"${value:,.0f}"
  elif format_type == "date":
    return value.strftime('%Y-%m-%d')
  else:
    return str(value)

# Create Big Numbers
def create_weekly_summary_big_numbers(weekly_summary_df):
  # Define a dictionary for formatting rules
  format_rules = {
      "Bitcoin Price USD": "currency",
      "Report Date": "string",  
      "Bitcoin Marketcap": "currency",
      "Sats Per Dollar": "float",
      "Bitcoin Dominance": "percentage",
      "24HR Bitcoin Trading Volume": "currency", 
      "Bitcoin Market Sentiment": "string",  
      "Bitcoin Market Trend": "string",
      "Bitcoin Valuation": "string"
  }

  # Create a series of BigNumbers for each metric in the table
  big_numbers = []

  for column, value in weekly_summary_df.iloc[0].items():
    if column == "Bitcoin Price Change Difficulty Period":
      continue  # Skip this entry
    formatted_value = format_value(value, format_rules.get(column, ""))
    if column == "Difficulty Change":
      # Assuming positive change is upward, negative is downward
      is_upward = value >= 0
      big_numbers.append(
          dp.BigNumber(
              heading=column,
              value=formatted_value,
              is_upward_change=is_upward,
          ))
    else:
      big_numbers.append(dp.BigNumber(
          heading=column,
          value=formatted_value,
      ))

  # Combine the BigNumbers into a Group with 3 columns and return
  return dp.Group(*big_numbers, columns=3)

# Create Performance Tables
def create_crypto_performance_table(report_data, data, report_date, correlation_results):
  # Define the structure for performance metrics
  performance_metrics_dict = {
    "Bitcoin": {
            "Asset": "BTC",
            "Price": report_data.loc[report_date, 'PriceUSD'],
            "Market Cap": report_data.loc[report_date, 'CapMrktCurUSD'],
            "Week To Date Return": report_data.loc[report_date, 'PriceUSD_trading_week_change'],
            "MTD": report_data.loc[report_date, 'PriceUSD_MTD_change'],
            "YTD": report_data.loc[report_date, 'PriceUSD_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'PriceUSD'],
        },
      "Ethereum": {
            "Asset": "ETH",
            "Price": report_data.loc[report_date, 'ethereum_close'],
            "Market Cap": report_data.loc[report_date, 'ethereum_market_cap'],
            "Week To Date Return": report_data.loc[report_date, 'ethereum_close_trading_week_change'],
            "MTD": report_data.loc[report_date, 'ethereum_close_MTD_change'],
            "YTD": report_data.loc[report_date, 'ethereum_close_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'ethereum_close'],
        },
      "Ripple": {
            "Asset": "XRP",
            "Price": report_data.loc[report_date, 'ripple_close'],
            "Market Cap": report_data.loc[report_date, 'ripple_market_cap'],
            "Week To Date Return": report_data.loc[report_date, 'ripple_close_trading_week_change'],
            "MTD": report_data.loc[report_date, 'ripple_close_MTD_change'],
            "YTD": report_data.loc[report_date, 'ripple_close_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'ripple_close'],
        },
      "Dogecoin": {
            "Asset": "DOGE",
            "Price": report_data.loc[report_date, 'dogecoin_close'],
            "Market Cap": report_data.loc[report_date, 'dogecoin_market_cap'],
            "Week To Date Return": report_data.loc[report_date, 'dogecoin_close_trading_week_change'],
            "MTD": report_data.loc[report_date, 'dogecoin_close_MTD_change'],
            "YTD": report_data.loc[report_date, 'dogecoin_close_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'dogecoin_close'],
        },
      "Binance Coin": {
            "Asset": "BNB",
            "Price": report_data.loc[report_date, 'binancecoin_close'],
            "Market Cap": report_data.loc[report_date, 'binancecoin_market_cap'],
            "Week To Date Return": report_data.loc[report_date, 'binancecoin_close_trading_week_change'],
            "MTD": report_data.loc[report_date, 'binancecoin_close_MTD_change'],
            "YTD": report_data.loc[report_date, 'binancecoin_close_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'binancecoin_close'],
        },
      "Tether": {
            "Asset": "USDT",
            "Price": report_data.loc[report_date, 'tether_close'],
            "Market Cap": report_data.loc[report_date, 'tether_market_cap'],
            "Week To Date Return": report_data.loc[report_date, 'tether_close_trading_week_change'],
            "MTD": report_data.loc[report_date, 'tether_close_MTD_change'],
            "YTD": report_data.loc[report_date, 'tether_close_YTD_change'],
            "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'tether_close'],
        },
    }

  # Convert the dictionary to a DataFrame
  performance_table_df = pd.DataFrame(list(performance_metrics_dict.values()))

  return performance_table_df

def create_index_performance_table(report_data, data, report_date, correlation_results):
  # Define the structure for performance metrics
  performance_metrics_dict = {
      "Bitcoin": {
          "Asset":
          "Bitcoin",
          "Price":
          report_data.loc[report_date, 'PriceUSD'],
          #"Market Cap": report_data.loc[report_date, 'CapMrktCurUSD'],
          "Week To Date Return":
          report_data.loc[report_date, 'PriceUSD_trading_week_change'],
          "MTD":
          report_data.loc[report_date, 'PriceUSD_MTD_change'],
          "YTD":
          report_data.loc[report_date, 'PriceUSD_YTD_change'],
          "90 Day BTC Correlation":
          correlation_results['priceusd_90_days'].loc['PriceUSD', 'PriceUSD'],
      },
      "Nasdaq": {
          "Asset":
          "Nasdaq",
          "Price": report_data.loc[report_date, '^IXIC_close'],
          #"Market Cap": data.loc['^IXIC_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, '^IXIC_close_trading_week_change'],
          "MTD": report_data.loc[report_date, '^IXIC_close_MTD_change'],
          "YTD": report_data.loc[report_date, '^IXIC_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', '^IXIC_close'],
      },
      "S&P500": {
          "Asset": "S&P500",
          "Price": report_data.loc[report_date, '^GSPC_close'],
          #"Market Cap": data.loc['^GSPC_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, '^GSPC_close_trading_week_change'],
          "MTD": report_data.loc[report_date, '^GSPC_close_MTD_change'],
          "YTD": report_data.loc[report_date, '^GSPC_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', '^GSPC_close'],
      },
      "XLF": {
          "Asset": "XLF Financials ETF",
          "Price": report_data.loc[report_date, 'XLF_close'],
          #"Market Cap": data.loc['XLF_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, 'XLF_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'XLF_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'XLF_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'XLF_close'],
      },
      "XLE": {
          "Asset": "XLE Energy ETF",
          "Price": report_data.loc[report_date, 'XLE_close'],
          #"Market Cap": data.loc['XLE_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, 'XLE_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'XLE_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'XLE_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'XLE_close'],
      },
      "FANG+": {
          "Asset": "FANG+ ETF",
          "Price": report_data.loc[report_date, 'FANG.AX_close'],
          #"Market Cap": data.loc['FANG.AX_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, 'FANG.AX_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'FANG.AX_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'FANG.AX_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'FANG.AX_close'],
      },
  }

  # Convert the dictionary to a DataFrame
  performance_table_df = pd.DataFrame(list(performance_metrics_dict.values()))

  return performance_table_df

def create_macro_performance_table(report_data, data, report_date, correlation_results):
  # Define the structure for performance metrics
  performance_metrics_dict = {
      "Bitcoin": {
          "Asset":
          "Bitcoin",
          "Price":
          report_data.loc[report_date, 'PriceUSD'],
          #"Market Cap": report_data.loc[report_date, 'CapMrktCurUSD'],
          "Week To Date Return":
          report_data.loc[report_date, 'PriceUSD_trading_week_change'],
          "MTD":
          report_data.loc[report_date, 'PriceUSD_MTD_change'],
          "YTD":
          report_data.loc[report_date, 'PriceUSD_YTD_change'],
          "90 Day BTC Correlation":
          correlation_results['priceusd_90_days'].loc['PriceUSD', 'PriceUSD'],
      },
      "US Dollar Index": {
          "Asset": "US Dollar Index",
          "Price": report_data.loc[report_date, 'DX=F_close'],
          "Week To Date Return": report_data.loc[report_date, 'DX=F_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'DX=F_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'DX=F_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'DX=F_close'],
      },
      "Gold Futures": {
          "Asset": "Gold Futures",
          "Price": report_data.loc[report_date, 'GC=F_close'],
          "Week To Date Return": report_data.loc[report_date, 'GC=F_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'GC=F_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'GC=F_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'GC=F_close'],
      },
      "Crude Oil Futures": {
          "Asset": "Crude Oil Futures",
          "Price": report_data.loc[report_date, 'CL=F_close'],
          "Week To Date Return": report_data.loc[report_date, 'CL=F_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'CL=F_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'CL=F_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'CL=F_close'],
      },
      "20+ Year Treasury Bond ETF": {
          "Asset": "20+ Year Treasury Bond ETF",
          "Price": report_data.loc[report_date, 'TLT_close'],
          "Week To Date Return": report_data.loc[report_date, 'TLT_close_trading_week_change'],
          "MTD": report_data.loc[report_date, 'TLT_close_MTD_change'],
          "YTD": report_data.loc[report_date, 'TLT_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', 'TLT_close'],
      },
      "Bloomberg Commodity Index": {
          "Asset": "Bloomberg Commodity Index",
          "Price": report_data.loc[report_date, '^BCOM_close'],
          "Week To Date Return": report_data.loc[report_date, '^BCOM_close_trading_week_change'],
          "MTD": report_data.loc[report_date, '^BCOM_close_MTD_change'],
          "YTD": report_data.loc[report_date, '^BCOM_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', '^BCOM_close'],
      },
  }

  # Convert the dictionary to a DataFrame
  macro_performance_table_df = pd.DataFrame(list(performance_metrics_dict.values()))

  return macro_performance_table_df

def create_equities_performance_table(report_data, data, report_date, correlation_results):
  # Define a list of equity tickers including Bitcoin
  equities = ['COIN', 'SQ', 'MSTR', 'MARA', 'RIOT']

  # Initialize an empty dictionary to hold the performance metrics
  performance_metrics_dict = {}

  # Add Bitcoin's performance data
  performance_metrics_dict['Bitcoin'] = {
      "Asset": "Bitcoin",
      "Price": report_data.loc[report_date, 'PriceUSD'],
      "Market Cap": report_data.loc[report_date, 'CapMrktCurUSD'],
      "Week To Date Return": report_data.loc[report_date, 'PriceUSD_trading_week_change'],
      "MTD": report_data.loc[report_date, 'PriceUSD_MTD_change'],
      "YTD": report_data.loc[report_date, 'PriceUSD_YTD_change'],
      "90 Day BTC Correlation": 1,  # Bitcoin's correlation with itself is always 1
  }

  # Loop over each equity to collect its performance data
  for equity in equities:  # Skipping 'Bitcoin' since it's already added
      performance_metrics_dict[equity] = {
          "Asset": equity,
          "Price": report_data.loc[report_date, f'{equity}_close'],
          "Market Cap": data.loc[report_date, f'{equity}_MarketCap'],
          "Week To Date Return": report_data.loc[report_date, f'{equity}_close_trading_week_change'],
          "MTD": report_data.loc[report_date, f'{equity}_close_MTD_change'],
          "YTD": report_data.loc[report_date, f'{equity}_close_YTD_change'],
          "90 Day BTC Correlation": correlation_results['priceusd_90_days'].loc['PriceUSD', f'{equity}_close'],
      }

  # Convert the dictionary to a DataFrame
  performance_table_df = pd.DataFrame(list(performance_metrics_dict.values()))

  return performance_table_df

# Style Table
def style_performance_table(performance_table):
  
  # Check if "Market Cap" column exists before formatting
  if 'Market Cap' in performance_table.columns:
      performance_table['Market Cap'] = performance_table['Market Cap'].apply(
          lambda x: '{:,.1f} Billion'.format(pd.to_numeric(x, errors='coerce') / 1e9) 
          if pd.notnull(pd.to_numeric(x, errors='coerce')) else x
      )

  format_dict = {
      'Asset': '{}',
      'Price': '{:,.2f}',
      #"Market Cap": '{:.0f}',
      'Week To Date Return': '{:.2%}',
      'MTD': '{:.2%}',
      'YTD': '{:.2%}',
      '90 Day BTC Correlation': '{:,.2f}'
  }

  diverging_cm = sns.diverging_palette(100, 133, as_cmap=True)
  diverging_cm = sns.diverging_palette(0, 0, s=0, l=85, as_cmap=True)
  bg_colormap = sns.light_palette("white", as_cmap=True)

  def color_values(val):
    color = 'green' if val > 0 else ('red' if val < 0 else 'black')
    return 'color: %s' % color

  gradient_columns = [
      'Week To Date Return', 'MTD', 'YTD', '90 Day BTC Correlation'
  ]

  # Define the style for the table: smaller font size
  table_style = [
      {
          'selector': 'th',
          'props': 'font-size: 10px;'  # Adjust header font size
      },
      {
          'selector': 'td',
          'props': 'font-size: 10px;'  # Adjust cell font size
      }
  ]

  # Apply the style to the table
  styled_table = (
      performance_table.style.format(format_dict)
      .applymap(color_values, subset=gradient_columns)
      .hide_index()
      .set_properties(**{'white-space': 'nowrap'})
      .set_table_styles(table_style)  # Apply the font size style
  )

  return styled_table
