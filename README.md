# Weekly Market Update Report

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Workflow Summary](#workflow-summary)
6. [Output Overview](#output-overview)
7. [Report Interface](#report-interface)
8. [Data Sources](#data-sources)
9. [License](#license)

## Introduction
The Weekly Market Update is a Python project specifically designed to analyze Bitcoin and its weekly performance. It retrieves data from a variety of sources, processes this data, and generates an insightful report that includes Bitcoin performance metrics, market analysis, and on-chain indicators. This tool is particularly useful for investors and analysts seeking weekly insights into Bitcoin market trends.

## Setup
1. Clone the repository to your local machine:
 ```
git clone https://github.com/SecretSatoshis/Bitcoin-Weekly-Market-Summary.git
 ```
2. Navigate to the project directory.
 ```
cd Bitcoin-Weekly-Market-Summary
 ```
3. Install the necessary packages using the following command:
 ```
pip install -r requirements.txt
 ```
4. You are now ready to run the script.
 ```
python main.py
 ```

The project code can also be accessed and run on [Replit](https://replit.com/@SecretSatoshis/Bitcoin-Weekly-Market-Update).


## Usage
Run the `main.py` script to generate the Weekly Market Update. This script orchestrates the data collection, analysis, and report generation processes.

## Project Structure
- `main.py`: Orchestrates the entire process of the report generation.
- `data_format.py`: Responsible for data retrieval, processing, and calculation of custom metrics.
- `data_definitions.py`: Defines the data structure, including tickers, start dates for market data, and key metrics for analysis.
- `report_tables.py`: Contains functions for creating tables and styling data presentations in the report.
- `datapane_report.py`: Handles the creation of the report layout, integrating various tables and visual elements using Datapane.

## Workflow Summary
The workflow consists of:
1. **Data Retrieval**: Collecting data from various sources.
2. **Data Processing**: Calculating custom metrics and processing financial data.
3. **Report Generation**: Creating tables, charts, and visualizations from the processed data.
4. **Output Production**: Compiling the components into an interactive HTML report.

## Output Overview
The report includes:
1. **HTML Report**: An interactive report detailing the week's Bitcoin market summary.
- You can download the report from `Weekly_Market_Update.html` or vist the [Report Link](https://secretsatoshis.github.io/Bitcoin-Weekly-Market-Update/Weekly_Market_Update.html).
3. **CSV Files**: Data files with the raw data used in the report.

## Report Interface
Utilizes Datapane for an interactive interface, offering tables, charts, and summaries for insights into the Bitcoin market.

## Data Sources
The project utilizes data from various sources. The data sources include:

### Bitcoin / Crypto Data
- **Coinmetrics**
  - [Twitter](https://twitter.com/coinmetrics)
  - [GitHub](https://github.com/coinmetrics/data/tree/master/csv)
- **CoinGecko**
  - [Website](https://www.coingecko.com/)
  - [API](https://www.coingecko.com/en/api)
  - 
### Traditional Finance Data
- **Yahoo Finance**
  - [Website](https://finance.yahoo.com/)
- **Yahoo_fin Python Library**
  - [Documentation](https://theautomatic.net/yahoo_fin-documentation/)
- **Finnhub**
  - [Website](https://finnhub.io/)
  - [API Documentation](https://finnhub.io/docs/api)
 
## Automated Report Updates with GitHub Actions

The report is updated daily using a GitHub Actions workflow. 

The workflow is scheduled to run every day at 16:10 UTC. It runs the `main.py` script, which generates the updated report. After running the script, the workflow stages, commits, and pushes the changes to the main branch of the repository. This way, the report is updated on a daily basis.

## License
Distributed under the GNU GENERAL PUBLIC LICENSE. See `LICENSE` for more information.
