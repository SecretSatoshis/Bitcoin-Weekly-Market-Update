import datetime
import pandas as pd

#TradFi Data
tickers = {
    'stocks': [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-A',
        'BRK-B', 'TSM', 'V', 'JPM', 'PYPL', 'GS', 'COIN', 'SQ', 'MSTR', 'MARA',
        'RIOT'
    ],
    'etfs': [
        'BITQ', 'CLOU', 'ARKK', 'XLK', 'QQQ', 'IUIT.L', 'VTI', 'TLT', 'LQD',
        'JNK', 'GLD', 'XLF', 'XLRE', 'SHY', 'XLE', 'FANG.AX'
    ],
    'indices':
    ['^GSPC', '^VIX', '^IXIC', '^TNX', '^TYX', '^FVX', '^IRX', '^BCOM'],
    'commodities': ['GC=F', 'CL=F', 'SI=F'],
    'forex': [
        'DX=F', 'AUDUSD=X', 'CHFUSD=X', 'CNYUSD=X', 'EURUSD=X', 'GBPUSD=X',
        'HKDUSD=X', 'INRUSD=X', 'JPYUSD=X', 'RUBUSD=X'
    ],
    'crypto': ['ethereum', 'ripple', 'dogecoin', 'binancecoin', 'tether'],
}

# Start date for TradFi Data
market_data_start_date = '2010-01-01'

# Just stock tickers for marketcap calculation
stock_tickers = tickers['stocks']

# Get today's date
today = datetime.date.today()

# Get yesterday's date
yesterday = today - datetime.timedelta(days=1)

# Creat report data and convert to pandas.Timestamp
report_date = pd.Timestamp(yesterday)

# On-Chain Metrics to create moving averages of for data smoothing
moving_avg_metrics = [
    'HashRate',
    'AdrActCnt',
    'TxCnt',
    'TxTfrValAdjUSD',
    'TxTfrValMeanUSD',
    'FeeMeanUSD',
    'FeeMeanNtv',
    'IssContNtv',
    'RevUSD',
    'nvt_price',
    'nvt_price_adj',
]

# Define report data and fields
filter_data_columns = {
    'Report_Metrics': [
        'SplyCur', 'SplyExpFut10yr', '7_day_ma_IssContNtv', 'IssContNtv',
        'pct_supply_issued', '365_day_ma_IssContNtv', 'TxCnt',
        '7_day_ma_TxCnt', '365_day_ma_TxCnt', 'AdrBalCnt', 'HashRate',
        '7_day_ma_HashRate', '365_day_ma_HashRate', 'PriceUSD', 'TxTfrCnt',
        '50_day_ma_priceUSD', '200_day_ma_priceUSD', '200_day_multiple',
        '200_week_ma_priceUSD', 'TxTfrValAdjUSD', '7_day_ma_TxTfrValAdjUSD',
        '365_day_ma_TxTfrValAdjUSD', 'RevUSD', 'AdrActCnt', 'AdrBalUSD10Cnt',
        '30_day_ma_AdrActCnt', '365_day_ma_AdrActCnt', 'DiffLast',
        '7_day_ma_TxTfrValMeanUSD', 'FeeTotUSD', 'thermocap_multiple_4',
        'thermocap_multiple_8', 'thermocap_multiple_16', 'thermocap_price',
        'thermocap_multiple_32', 'thermocap_multiple', 'nvt_price',
        'nvt_price_adj', 'nvt_price_multiple', '30_day_ma_nvt_price',
        '365_day_ma_nvt_price', 'NVTAdj', 'NVTAdj90', 'NVTAdjFF',
        'IssContPctAnn', 'pct_fee_of_reward', 'realised_price', 'VelCur1yr',
        'supply_pct_1_year_plus', 'mvrv_ratio', 'realizedcap_multiple_3',
        'realizedcap_multiple_5', 'nupl', 'AAPL_close', 'CapMrktCurUSD',
        '^IXIC_close', "RevHashRateUSD", '^GSPC_close', 'XLF_close',
        'XLRE_close', 'GC=F_close', 'SI=F_close', 'CL=F_close', 'DX=F_close',
        'SHY_close', 'TLT_close', '^TNX_close', '^TYX_close', '^BCOM_close',
        '^FVX_close', '^IRX_close', 'XLE_close', 'BITQ_close', 'FANG.AX_close',
        'AUDUSD=X_close', 'CHFUSD=X_close', 'CNYUSD=X_close', 'EURUSD=X_close',
        'GBPUSD=X_close', 'HKDUSD=X_close', 'INRUSD=X_close', 'JPYUSD=X_close',
        'RUBUSD=X_close', 'ethereum_close', 'ripple_close', 'dogecoin_close',
        'binancecoin_close', 'tether_close', 'value_classification', 'value',
        'bitcoin_dominance', 'btc_trading_volume', 'ethereum_market_cap',
        'ripple_market_cap', 'dogecoin_market_cap', 'binancecoin_market_cap',
        'tether_market_cap', 'COIN_close', 'SQ_close', 'MSTR_close',
        'MARA_close', 'RIOT_close'
    ]
}

# First Halving Date Start Stats Calculation
stats_start_date = '2012-11-28'

# Timeframes to calculate volatitlity for
volatility_windows = [30, 90, 180, 365]

# Data to run correlations on
correlation_data = [
    'PriceUSD', 'AAPL_close', 'MSFT_close', 'GOOGL_close', 'AMZN_close',
    'NVDA_close', 'TSLA_close', 'META_close', 'BRK-A_close', 'BRK-B_close',
    'TSM_close', 'V_close', 'JPM_close', 'PYPL_close', 'GS_close',
    'FANG.AX_close', 'BITQ_close', 'CLOU_close', 'ARKK_close', 'XLK_close',
    'QQQ_close', 'IUIT.L_close', 'VTI_close', 'TLT_close', 'LQD_close',
    'JNK_close', 'GLD_close', 'XLF_close', 'XLRE_close', 'SHY_close',
    'XLE_close', '^GSPC_close', '^VIX_close', '^IXIC_close', '^TNX_close',
    '^TNX_close', '^TYX_close', '^FVX_close', '^IRX_close', 'GC=F_close',
    'CL=F_close', 'SI=F_close', 'DX=F_close', 'AUDUSD=X_close', '^BCOM_close',
    'CHFUSD=X_close', 'CNYUSD=X_close', 'EURUSD=X_close', 'GBPUSD=X_close',
    'HKDUSD=X_close', 'INRUSD=X_close', 'JPYUSD=X_close', 'RUBUSD=X_close',
    'ethereum_close', 'ripple_close', 'dogecoin_close', 'binancecoin_close',
    'tether_close', 'COIN_close', 'SQ_close', 'MSTR_close', 'MARA_close',
    'RIOT_close'
]

# Metrics to calculate valuation targets
valuation_data_metrics = {
    'valuation_metrics': [
        'NVTAdj', 'NVTAdj90', 'mvrv_ratio', 'thermocap_multiple',
        '200_day_multiple', 'nvt_price_multiple', 'nvt_price', 'nvt_price_adj',
        'NVTAdj_percentile', 'NVTAdj90_percentile', 'mvrv_ratio_percentile',
        'thermocap_multiple_percentile', '200_day_multiple_percentile',
        'nvt_price_multiple_percentile', 'NVTAdj_zscore', 'mvrv_ratio_zscore',
        'thermocap_multiple_zscore', '200_day_multiple_zscore',
        'NVTAdj90_zscore', 'nvt_price_multiple_zscore', 'PriceUSD',
        'SF_Predicted_Price', 'SF_Multiple', 'SF_Predicted_Price_percentile',
        'SF_Multiple_percentile', 'SF_Predicted_Price_zscore',
        'SF_Multiple_zscore'
    ]
}

#Fundamentals And Valuation Table Metrics
metrics_template = {
    'Network Performance': {
        'Total Address Count': ('AdrBalCnt', 'number'),
        'Address Count > $10': ('AdrBalUSD10Cnt', 'number'),
        'Active Addresses': ('AdrActCnt', 'number'),
        'Supply Held 1+ Year %': ('supply_pct_1_year_plus', 'percent'),
        'Transaction Count': ('TxCnt', 'number'),
        'Transfer Count': ('TxTfrCnt', 'number'),
        'Transaction Volume': ('TxTfrValAdjUSD', 'currency'),
        'Transaction Fee USD': ('FeeTotUSD', 'currency'),
    },
    'Network Security': {
        'Hash Rate': ('HashRate', 'number'),
        'Network Difficulty': ('DiffLast', 'number'),
        'Miner Revenue': ('RevUSD', 'currency'),
        'Fee % Of Reward': ('pct_fee_of_reward', 'percent'),
    },
    'Network Economics': {
        'Bitcoin Supply': ('SplyCur', 'number'),
        'Bitcoin Supply In 10 Years': ('SplyExpFut10yr', 'number'),
        '% Supply Issued': ('pct_supply_issued', 'percent'),
        'Bitcoin Mined Per Day': ('IssContNtv', 'number'),
        'Annual Inflation Rate': ('IssContPctAnn', 'percent'),
        'Velocity': ('VelCur1yr', 'number2'),
    },
    'Network Valuation': {
        'Market Cap': ('CapMrktCurUSD', 'currency'),
        'Bitcoin Price': ('PriceUSD', 'currency'),
        'Realised Price': ('realised_price', 'currency'),
        'Thermocap Price': ('thermocap_price', 'currency'),
    }
}

chart_template = {
    'title':
    "Bitcoin Weekly Price Chart",
    'x_label':
    "Date",
    'y1_label':
    "USD Price",
    'filename':
    "Bitcoin_OHLC",
    'events': [{
        'name': 'CME Futures',
        'dates': ['2017-12-17'],
        'orientation': 'v'
    }, {
        'name': 'Bitcoin Winter',
        'dates': ['2018-12-15'],
        'orientation': 'v'
    }, {
        'name': 'Coinbase IPO',
        'dates': ['2021-04-14'],
        'orientation': 'v'
    }, {
        'name': 'FTX Bankrupt',
        'dates': ['2022-11-11'],
        'orientation': 'v'
    }]
}