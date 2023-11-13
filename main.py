import datapane as dp
import pandas as pd
from datetime import datetime
import datetime
import warnings

# Ignore FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import Files
import data_format

from data_definitions import (
    tickers, market_data_start_date, moving_avg_metrics, yesterday, 
    report_date, filter_data_columns, stats_start_date, correlation_data, 
    metrics_template, chart_template
)

# Fetch the data
data = data_format.get_data(tickers, market_data_start_date)
data = data_format.calculate_custom_on_chain_metrics(data)
data = data_format.calculate_moving_averages(data, moving_avg_metrics)
start_timestamp = int(pd.Timestamp('2017-01-01').timestamp())
end_timestamp = int(pd.Timestamp(yesterday).timestamp())
ohlc_data = data_format.get_finnhub_ohlc('BINANCE:BTCUSDT','W', start_timestamp, end_timestamp)

# Forward fill the data for all columns
data.ffill(inplace=True)
data = data.loc[:yesterday]

# Flatten the list of columns from the dictionary
columns_to_keep = [item for sublist in filter_data_columns.values() for item in sublist]

# Filter the dataframe
filter_data = data[columns_to_keep]

# Run Data Analysis On Report Data
report_data = data_format.run_data_analysis(filter_data, stats_start_date)

# Calcuate Correlations
correlation_data = data[correlation_data]
# Drop NA Values
correlation_data = correlation_data.dropna()
# Calculate Bitcoin Correlations
correlation_results = data_format.create_btc_correlation_tables(report_date, tickers, correlation_data)

# Import Report Table Functions
import report_tables

# Create the difficulty update table
weekly_summary_table = report_tables.create_weekly_summary_table(report_data, report_date)
weekly_summary_table.to_csv('weekly_summary.csv', index=False)
weekly_summary_big_numbers = report_tables.create_weekly_summary_big_numbers(weekly_summary_table)
weekly_summary_dp = dp.Table(weekly_summary_table, name='Weekly_Summary')

# Create the performance table
crypto_performance_table = report_tables.create_crypto_performance_table(report_data, data, report_date, correlation_results)
styled_crypto_performance_table = report_tables.style_performance_table(crypto_performance_table)
styled_crypto_performance_table.data.to_csv('crypto_performance_table.csv', index=False)
styled_crypto_performance_table_dp = dp.Table(styled_crypto_performance_table, name='crypto_performance_table')

# Create index performance table 
index_performance_table = report_tables.create_index_performance_table(report_data, data, report_date, correlation_results)
styled_index_performance_table = report_tables.style_performance_table(index_performance_table)
styled_index_performance_table.data.to_csv('index_performance_table.csv', index=False)
styled_index_performance_table_dp = dp.Table(styled_index_performance_table, name='index_performance_table')

# Create index performance table 
macro_performance_table = report_tables.create_macro_performance_table(report_data, data, report_date, correlation_results)
styled_macro_performance_table = report_tables.style_performance_table(macro_performance_table)
styled_macro_performance_table.data.to_csv('macro_performance_table.csv', index=False)
styled_macro_performance_table_dp = dp.Table(styled_macro_performance_table, name='macro_performance_table')

# Create index performance table 
equities_performance_table = report_tables.create_equities_performance_table(report_data, data, report_date, correlation_results)
styled_equities_performance_table = report_tables.style_performance_table(equities_performance_table)
styled_equities_performance_table.data.to_csv('equities_performance_table.csv', index=False)
styled_equities_performance_table_dp = dp.Table(styled_equities_performance_table, name='equities_performance_table')

# Creating trading range table $5000
bucket_counts_df = data_format.calculate_price_buckets(data, 5000)
bucket_counts_df[bucket_counts_df['Price Range ($)'] != '$0K-$5K']
bucket_counts_df = data_format.style_bucket_counts_table(bucket_counts_df)
trading_range_table = dp.Table(bucket_counts_df)

# Creating trading range table $1000
bucket_counts_df = data_format.calculate_price_buckets(data, 1000)
plotly_dp_chart = data_format.create_price_buckets_chart(bucket_counts_df)

# Create ROI Table
roi_table = data_format.calculate_roi_table(data)
roi_table = data_format.style_roi_table(roi_table)
roi_table = dp.Table(roi_table)

# Create MA Table
ma_table = data_format.calculate_ma_table(data)
ma_table = data_format.style_ma_table(ma_table)
ma_table = dp.Table(ma_table)

# Create Fundamentals & Valuation Table
table_df = data_format.create_metrics_table(report_data, metrics_template)
table_fig = dp.Table(table_df)
table_df = table_df.data
table_df.to_csv('fundamentals_valuation_table.csv', index=False)

# Creat Heat Maps
plotly_monthly_heatmap_chart = data_format.monthly_heatmap(data)
plotly_weekly_heatmap_chart = data_format.weekly_heatmap(data)

# Create YOY Plot
yoy_plot = data_format.plot_yoy_change(report_data,"PriceUSD_365_change")

# Creat OHLC Plot
ohlc_plot = data_format.create_ohlc_chart(ohlc_data, report_data, chart_template)

# Datapane Report Imports
from datapane_report import generate_report_layout

# Configure Datapane Report
report_layout = generate_report_layout(weekly_summary_big_numbers,styled_crypto_performance_table_dp, 
                                       styled_index_performance_table_dp,styled_macro_performance_table_dp,
                                       styled_equities_performance_table_dp,trading_range_table,plotly_dp_chart,
                                       ma_table,roi_table,table_fig,plotly_monthly_heatmap_chart,
                                       plotly_weekly_heatmap_chart,yoy_plot,ohlc_plot
                                       )

# DataPane Styling
custom_formatting = dp.Formatting(
    light_prose=False,
    accent_color="#000", 
    bg_color="#EEE",  # White background
    text_alignment=dp.TextAlignment.LEFT,
    font=dp.FontChoice.SANS,
    width=dp.Width.FULL
  )

# Create Difficulty Report
dp.save_report(report_layout, path='Weekly_Market_Summary.html', formatting=custom_formatting)