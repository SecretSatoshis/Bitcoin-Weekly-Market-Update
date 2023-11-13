import datapane as dp

from report_tables import create_crypto_performance_table


def generate_report_layout(weekly_summary_big_numbers, crypto_performance_table, index_performance_table, macro_performance_table, equities_performance_table,trading_range_table,plotly_dp_chart,ma_table, roi_table,table_fig,plotly_heatmap_chart,plotly_weekly_heatmap_chart,yoy_plot,ohlc_plot):
  welcome_text = dp.Text("""
  ## Secret Satoshis Weekly Market Update Data
  
Explore our latest weekly market update data report, the data behind our <a href="https://www.newsletter.secretsatoshis.com/s/premium" target="_blank"> Weekly Market Update</a>. This report is delivered each Sunday morning and is available @ [<a href="https://www.newsletter.secretsatoshis.com/" target="_blank">newsletter.secretsatoshis.com</a>](https://www.newsletter.secretsatoshis.com/).
  
  ## Report Navigation:
  
  The report is organized into three distinct sections, each accessible through individual tabs for a structured exploration:
  
  1. **Weekly Market Update Data Report**: A detailed analysis of the current state of Bitcoin.
  
  2. **Weekly Market Update Data Report FAQ**: A section dedicated to providing answers to commonly asked questions regarding the report.
  
  3. **Report Definitions/Glossary**: A section that serves as a glossary, explaining the key terms, metrics, and concepts discussed throughout the report.
  
  To navigate between different sections, click on the respective tab.
""")


  # Weekly Report Summary Section Components
  weekly_header = dp.Text("# Weekly Market Summary")
  weekly_footer = dp.Text(
      "For a deeper dive into the key metrics, visit the Report Definitions Tab above."
  )

  # Performance Report Summary Section Components
  performance_header = dp.Text("# Performance Table")
  performance_description = dp.Text("""
  A comparative view of Bitcoin's performance against key assets and indices.
      """)
  performance_footer = dp.Text(
      "For a deeper dive into the performance metrics, visit the Report Definitions Tab above."
  )

  # Fundamentals Report Summary Section Components
  fundamentals_header = dp.Text("# Fundamentals Table")
  fundamentals_description = dp.Text("""
  A detailed analysis of Bitcoin's on-chain activity, illustrating network security, economic activity, and overall user engagement.
      """)
  fundamentals_footer = dp.Text(
      "For a deeper dive into the fundamental metrics, visit the Report Definitions Tab above."
  )

  # Trade Report Summary Section Components
  trade_header = dp.Text("# Marekt Analysis")
  trade_description = dp.Text("""
  A comprehensive guide to Bitcoin's price through various analytical lenses, aiding in understanding its current and historical price performance.
      """)
  valuation_footer = dp.Text(
      "For a deeper dive into the market metrics, visit the Report Definitions Tab above."
  )

  # Weekly Adjustment Newsletter Promo
  promo_header = dp.Text("# The Next Step in Your Bitcoin Exploration: <a href='https://www.newsletter.secretsatoshis.com/s/premium' target='_blank'>The Weekly Market Update</a>")
  promo_description = dp.Text("""
  The Weekly Market Update provides a comprehensive narrative on the data presented, offering enhanced insights into the Bitcoin market.

  **Why Subscribe?**

  1. **Clear, In-depth Analysis:** Understand the nuances of the data in the Weekly Market Update Data Report through a concise, well-written narrative.

  2. **Stay Ahead of the Curve:** Receive timely updates on crucial Bitcoin investment metrics, ensuring you're always informed.

  3. **Expertise of Agent 21:** Benefit from the insights of Agent 21, an AI persona powered by Chat-GPT 4.

  Ready to further enhance your understanding of Bitcoin?
  <a href="https://www.newsletter.secretsatoshis.com/s/premium" target="_blank">Subscribe Now</a>.
  """)
  
  # Assume styled_table1, styled_table2, ... styled_tableN are your styled performance tables
  styled_performance_tables1 = [crypto_performance_table, equities_performance_table]

  # Create individual Groups for each performance table
  performance_table_group1 = [dp.Group(blocks=[table], label=f"Table {i+1}") for i, table in enumerate(styled_performance_tables1)]

  # Combine all performance table Groups into a Group block with specified columns
  performance_tables_section1 = dp.Group(blocks=performance_table_group1, columns=len(styled_performance_tables1))

  # Assume styled_table1, styled_table2, ... styled_tableN are your styled performance tables
  styled_performance_tables2 = [index_performance_table, macro_performance_table]

  # Create individual Groups for each performance table
  performance_table_group2 = [dp.Group(blocks=[table], label=f"Table {i+1}") for i, table in enumerate(styled_performance_tables2)]

  # Example headers for each section
  header_performance_tables1 = dp.Text("### Crypto & Stocks")
  header_performance_tables2 = dp.Text("### Indexes & Macros")
  header_trading_range_section = dp.Text("### Bitcoin Price Trading Ranges")
  header_roi_ma_section = dp.Text("### Bitcoin Investment ROI & Price Moving Average Growth")
  header_yoy_section = dp.Text("### Bitcoin Price Performacne Year Over Year")
  header_heatmap_section = dp.Text("### Bitcoin Price Performacne Heatmap")
  header_weekly_price_section = dp.Text("### Bitcoin Weekly Price Chart")
  header_definition = dp.Text("### Report Section Definitions")

  # Combine all performance table Groups into a Group block with specified columns
  performance_tables_section2 = dp.Group(blocks=performance_table_group2, columns=len(styled_performance_tables2))
  trading_range_section = dp.Group(blocks=[trading_range_table, plotly_dp_chart], columns=2)
  roi_ma_section = dp.Group(blocks=[roi_table, ma_table,], columns=2)
  
  # Difficulty Report Summary
  difficulty_summary_layout = dp.Group(
      weekly_header,
      weekly_summary_big_numbers,
      weekly_footer,
      header_weekly_price_section,
      ohlc_plot,
      performance_header,
      performance_description,
      header_performance_tables1,
      performance_tables_section1,
      header_performance_tables2,
      performance_tables_section2,
      performance_footer,
      trade_header,
      trade_description,
      header_trading_range_section,
      trading_range_section,
      header_roi_ma_section,
      roi_ma_section,
      header_yoy_section,
      yoy_plot,
      header_heatmap_section,
      plotly_heatmap_chart,
      plotly_weekly_heatmap_chart,
      valuation_footer,
      fundamentals_header,
      fundamentals_description,
      table_fig,
      fundamentals_footer,
      promo_header,
      promo_description,
      columns=1,
  )

  faq_summary_text = dp.Text("""
  ## Frequently Asked Questions (FAQ) for the Weekly Market Update Data Report
  
  1. **What is the "Weekly Market Update Data Report"?**
  The "Weekly Market Update Data Report" is a comprehensive data report that serves as the foundation for the "Secret Satoshis Weekly Market Update." It offers an in-depth analysis of the Bitcoin market, focusing on pivotal financial and on-chain metrics, and includes all the  data, tables, and charts that are highlighted in the newsletter.
  
  2. **How does the "Weekly Market Update Data Report" relate to the "Secret Satoshis Weekly Market Update"?**
  The "Weekly Market Update Data Report" serves as a primary data source for the "Weekly Market Update". While the report distills this data into actionable narratives and insights, the data report allows readers to independently analyze the data, facilitating a deep and comprehensive understanding of the Bitcoin market.

 3. **How often is the "Weekly Market Update Data Report" updated?**
  The "Weekly Market Update Data Report" is updated daily, presenting data with a T+1 timeline.
  """)

  bitcoin_101_summary_text = dp.Text("""
  ## Bitcoin 101: A Step-by-Step Guide to Key Terms and Concepts
  
  **Bitcoin**: A decentralized digital currency, operating without central control, where transactions are verified by network nodes and recorded on a public ledger.
  
  **Blockchain**: A decentralized digital ledger recording all Bitcoin transactions across a network of computers, with transactions grouped into blocks, forming a secure and immutable chain.
  
  **Block**:  A collection of confirmed transactions within the Bitcoin network, added to the blockchain in a secure and chronological order.
  
  **Block Time**: The average time taken to add a new block to the blockchain, maintained at around 10 minutes in the Bitcoin network.
  
  **Mining**: The process of adding new blocks to the blockchain, where miners solve complex mathematical problems using high computational power.
  
  **Difficulty**: A dynamic metric representing the challenge miners encounter when adding the next block to the blockchain, adjusting based on the network's total hash rate to maintain a consistent block time.
  
  **Miner Rewards**: Miners receive two forms of compensation:
  
  ***Block Rewards***: New bitcoins awarded for successfully adding a block.
  
  ***Transaction Fees***: Fees from each transaction in a block.
  
  **Node**:  A computer connected to the Bitcoin network that validates and relays transactions, collaboratively maintaining and securing the network.
  
  **Decentralization**: This foundational principle of Bitcoin negates the existence of a central governing body or authority. Instead, it allows for a distributed network where various participants, including miners and nodes, collaboratively work to secure and maintain the network's operations and integrity. 
  
  **Economic Model**: Bitcoin adheres to a deflationary economic model characterized by a fixed supply cap of 21 million coins. This intentional design induces scarcity, fostering a potential appreciation in value over time. As opposed to inflationary models where the supply of currency can increase indefinitely, Bitcoin's economic model aims to preserve and potentially increase the value of the digital asset in the long run.
  
  **Wallet**: A digital application allowing users to store, send, and receive bitcoins while securing their private keys.
  
  **Private Key**: A confidential cryptographic key granting users access and control over their bitcoins in their wallet.
  
 **Public Key**: A cryptographic key derived from the private key, serving as an address to which others can send bitcoins. The public key is essentially a user's identity in the Bitcoin network, which can be shared openly without compromising security, as it works in tandem with a private key to authorize transactions.
  
  **Transaction**: A transfer of value between Bitcoin wallets, recorded on the blockchain. Each transaction is signed by the sender's private key, ensuring the authenticity and integrity of the information conveyed.
  
  **UTXO (Unspent Transaction Output)**: A representation of the bitcoins owned by a wallet. UTXOs are created as outputs in a transaction and can be later used as inputs in new transactions, forming a chain of ownership. The UTXO model ensures that all bitcoins are accounted for and prevents double-spending.
""")

  # Definition Tab Tables
  faq_tabs = dp.Group(
      faq_summary_text,
      bitcoin_101_summary_text,
  )

  # Weekly Summary Table
  weekly_summary_table_content = """
  ## Weekly Summary Table
  **Purpose:** Provides a comprehensive overview of the current Bitcoin market situation, focusing on key metrics for a specific date.
  **Key Metrics:**
  - **Bitcoin Price USD:** The current market price of Bitcoin in US dollars.
  - **Report Date:** The specific date the report was run.
  - **Bitcoin Marketcap:** The total market capitalization of Bitcoin.
  - **Sats Per Dollar:** The number of satoshis (smallest unit of Bitcoin) per US dollar.
  - **Bitcoin Dominance:** Bitcoin's market dominance compared to other cryptocurrencies.
  - **Bitcoin Trading Volume:** The total trading volume of Bitcoin in the specified period.
  - **Bitcoin Market Sentiment:** An indicator of the current market sentiment towards Bitcoin.
  - **Bitcoin Market Trend:** The general market trend (Bullish, Neutral, Bearish) during the reporting period.
  - **Bitcoin Valuation:** The current valuation status of Bitcoin (Overvalued, Undervalued, Fair Value).
  
  **Insights:** This table gives a quick and comprehensive view of Bitcoin's market status. It helps readers understand the current valuation, market dominance, and trading trends of Bitcoin, which are critical for making informed investment decisions.
  """
  weekly_summary_table = dp.Text(weekly_summary_table_content)

  # OHLC Chart Overview
  ohlc_chart_overview = dp.Text("""
  ## Open-High-Low-Close (OHLC) Chart
  **Purpose:** Presents an OHLC chart of Bitcoin prices, offering a detailed view of its price movements within specific time frames.
  
  **Insights:** Essential for technical analysis, providing insights into market sentiment and potential price directions. Helps in identifying patterns like bullish or bearish trends, breakouts, or reversals.
  """)

  # Combine the sections for the first part of the report
  first_section = dp.Group(
      weekly_summary_table,
      ohlc_chart_overview
  )

  # Cryptocurrency Performance Table
  crypto_performance_overview = dp.Text("""
  ## Cryptocurrency Performance Table
  **Purpose:** Compares the performance of various cryptocurrencies over a specified period.
  
  **Insights:** This table allows readers to compare the performance of major cryptocurrencies, providing insights into their relative strengths, market movements, and correlations with Bitcoin.
  """)

  # Index Performance Table
  index_performance_overview = dp.Text("""
  ## Index Performance Table
  **Purpose:** Analyzes the performance of Bitcoin against major stock indices like Nasdaq, S&P500, and ETFs.
  
  **Insights:** By comparing Bitcoin with major indices, this table provides an understanding of how Bitcoin performs in relation to traditional financial markets.
  """)

  # Macro Performance Table
  macro_performance_overview = dp.Text("""
  ## Macro Performance Table
  **Purpose:** Evaluates Bitcoin's performance in relation to macroeconomic indicators like the US Dollar Index, Gold Futures, and others.
  
  **Insights:** This table is crucial for understanding Bitcoin's position and performance in the global economic landscape.
  """)

  # Equities Performance Table
  equities_performance_overview = dp.Text("""
  ## Equities Performance Table
  **Purpose:** Focuses on the performance of equities related to Bitcoin and the cryptocurrency market, such as COIN, SQ, MSTR, MARA, RIOT, etc.
  
  **Insights:** This table illustrates how Bitcoin-related equities perform in the stock market, providing insights into the investor sentiment.
  """)

  # Combine the sections for the second part of the report
  second_section = dp.Group(
      crypto_performance_overview,
      index_performance_overview,
      macro_performance_overview,
      equities_performance_overview,
  )


  # Price Buckets Analysis
  price_buckets_analysis_text = """
  ## Price Buckets Analysis
  **Purpose:** Categorizes Bitcoin prices into defined buckets, providing a view of how many days Bitcoin traded within specific price ranges.
  
  **Insights:** Offers a historical perspective on the price distribution of Bitcoin. Helps in understanding which price ranges have been most common, potentially indicating key support or resistance levels.
  """

  # Monthly Heatmap of Returns
  monthly_heatmap_text = """
  ## Monthly Heatmap of Returns
  **Purpose:** Presents monthly and yearly Bitcoin returns in a heatmap format, providing a quick visual overview of performance over time.
  
  **Insights:** Allows for easy identification of periods with high returns or significant losses. Can be used to spot seasonal patterns or annual trends in Bitcoin's market performance.
  """

  # Weekly Heatmap
  weekly_heatmap_text = """
  ## Weekly Heatmap
  **Purpose:** Shows Bitcoin's weekly returns over the last 5 years in a heatmap format.
  
  **Insights:** Useful for spotting short-term trends and weekly patterns in Bitcoin's price movements.
  """

  # Year-Over-Year (YOY) Change Chart
  yoy_change_chart_text = """
  ## Year-Over-Year (YOY) Change Chart
  **Purpose:** Plots Bitcoin's year-over-year percentage change, providing insights into its long-term growth trajectory.
  
  **Insights:** Highlights periods of significant growth or decline. Useful for investors focusing on long-term trends.
  """

  # Return on Investment (ROI) Table
  roi_table_text = """
  ## Return on Investment (ROI) Table
  **Purpose:** Calculates and presents the ROI for Bitcoin over various time frames, providing a snapshot of its investment performance.
  
  **Insights:** Allows investors to gauge the historical profitability of investing in Bitcoin over different periods. Helps in comparing short-term versus long-term investment returns.
  """

  # Moving Averages (MA) Table
  ma_table_text = """
  ## Moving Averages (MA) Table
  **Purpose:** Computes and displays various moving averages for Bitcoin, giving insights into its trending behavior.

  **Insights:** Moving averages are key indicators used in technical analysis to smooth out price trends and identify momentum. Helps in determining bullish or bearish market sentiments.
  """

  # Combine the sections for the third part of the report
  third_section = dp.Group(
      dp.Text(price_buckets_analysis_text),
      dp.Text(monthly_heatmap_text),
      dp.Text(weekly_heatmap_text),
      dp.Text(yoy_change_chart_text),
      dp.Text(roi_table_text),
      dp.Text(ma_table_text)
  )


  # Network Performance Description
  network_performance_text = """
  ## Network Performance
  **Purpose:** Analyzes various metrics that reflect the overall health and activity of the Bitcoin network.
  
  **Key Metrics:**
  - **Total Address Count & Address Count > $10:** These metrics give insights into the number of unique Bitcoin addresses and those holding more than $10, reflecting user adoption and distribution of wealth within the network.
  - **Active Addresses:** Indicates the number of unique addresses active in transactions, serving as a barometer of network engagement.
  - **Supply Held 1+ Year %:** Shows the percentage of Bitcoin supply that hasn't moved in over a year, highlighting investor sentiment and potential long-term holding behavior.
  - **Transaction Count & Transfer Count:** SRepresents the total number of transactions and transfers on the Bitcoin network, indicating network utilization and activity levels.
  - **Transaction Volume:** The total value of all Bitcoin transactions, offering insights into the economic throughput of the network.
  - **Transaction Fee USD:** Reflects the total fees paid for Bitcoin transactions, signifying network demand and miner revenue from fees.
  """

  # Network Security Description
  network_security_text = """
  ## Network Security
  **Purpose:** Provides insights into the security and mining dynamics of the Bitcoin network.
  
  **Key Metrics:**
  - **Hash Rate:** Measures the total computational power used in Bitcoin mining and transaction processing, indicating network security and mining activity.
  - **Network Difficulty:** Represents the complexity of mining a Bitcoin block, adjusting to maintain consistent block times and ensuring network stability.
  - **Miner Revenue:** Total earnings of Bitcoin miners from block rewards and transaction fees, providing insights into the economic incentives and health of the mining sector.
  - **Fee % Of Reward:** The proportion of miner revenue derived from transaction fees as opposed to block rewards, highlighting the economic dynamics of mining.
  """

  # Network Economics Description
  network_economics_text = """
  ## Network Economics
  **Purpose:** Examines the economic aspects of the Bitcoin network, including supply dynamics and inflation rate.
  
  **Key Metrics:**
  - **Bitcoin Supply & Bitcoin Supply In 10 Years:** Tracks the total and projected Bitcoin supply, shedding light on the scarcity dynamics of Bitcoin.
  - **% Supply Issued:** The percentage of the total possible Bitcoin supply that has been mined, indicating the progression towards the 21 million cap.
  - **Bitcoin Mined Per Day:** The daily rate of new Bitcoin creation, reflecting the pace of supply expansion.
Annual Inflation Rate: The rate at which the Bitcoin supply is increasing, providing insights into its inflationary or deflationary nature.
  - **Velocity:** A measure of how frequently Bitcoin is transacted, offering insights into its use as a medium of exchange versus a store of value.
  """

  # Network Valuation Description
  network_valuation_text = """
  ## Network Valuation
  **Purpose:** Evaluates Bitcoin's market position and valuation through various metrics.
  
  **Key Metrics:**
  - **Market Cap:** The total market value of all mined Bitcoin, reflecting its market significance and investor sentiment.
  - **Bitcoin Price:** The current market price of Bitcoin, directly representing market sentiment and investment value.
  - **Realised Price:** A metric that considers the price at which each Bitcoin last moved, offering a different perspective on market valuation.
  - **Thermocap Price:** A valuation model comparing the market cap with the total miner revenue, providing insights into the market's valuation of Bitcoin's security and miner commitment.
  """

  # Combine the sections for the fourth part of the report
  fourth_section = dp.Group(
      dp.Text(network_performance_text),
      dp.Text(network_security_text),
      dp.Text(network_economics_text),
      dp.Text(network_valuation_text)
  )


  # Definition Tab Tables
  definition_tabs = dp.Select(blocks=[
      dp.Group(first_section, label="Market Summary"),
      dp.Group(second_section, label="Performance Tables"),
      dp.Group(third_section, label="Market Analysis"),
      dp.Group(fourth_section, label="Fundamentals Table")
  ])

  # Definition Summary
  definition_layout = dp.Group(header_definition, definition_tabs, columns=1)
  report_tabs = dp.Select(blocks=[
      dp.Group(difficulty_summary_layout, label="Weekly Market Update Data Report"),
      dp.Group(faq_tabs, label="Weekly Market Update FAQ"),
      dp.Group(definition_layout, label="Report Definitions / Glossary")
  ])

  # Combine all parts for final report
  report_blocks = [welcome_text, report_tabs]

  # Return the final layout structure
  return report_blocks