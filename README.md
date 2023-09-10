__Stock Data Analysis: A Comprehensive Stock Data Processing and Analysis Platform__

This repository hosts an application designed to facilitate a comprehensive analysis of stock data. It encompasses both the front-end and back-end code necessary to process, analyze, and visualize financial data efficiently. Below is a detailed explanation of the architecture and various components of this application, alongside some instructions to access its features.

__Architecture Overview__

Our system is structured into three primary components:

  1. Database (DynamoDB)
     
  Our data is stored in an AWS DynamoDB database, structured with the following schema:

  `close`: The closing price of the stock for the given date 

  `open`: The opening price of the stock for the given date

  `high`: The highest price of the stock on the given date

  `low`: The lowest price of the stock on the given date.

  `volume`: The number of shares traded during the given date.

  `symbol`: The stock ticker symbol `(Primary Key)`

  `date`: The date the stock data `(Secondary Key)`

  This structure allows for efficient querying based on stock symbol and date.

  2. Server (AWS EC2)
     
Instance Type: We have deployed the application on a t2.micro instance, which balances computational power and cost-efficiency.

Deployment Strategy: Both the front-end and back-end codebases are deployed on the same server to streamline communication and reduce latency.

  3. Data Flow
     
The data flow within the application is represented visually in the diagram below:
![Architecture Diagram](image.png)

__Front-end Access Instructions__

To access and utilize the features of the front-end interface, follow these steps:

  1. Navigate to http://3.84.81.214/ using a browser (ensure to use the HTTP protocol).
  2. Utilize the Search Button to generate a Candlestick Graph and an Indicator Table based on the entered stock symbol.
  3. Click on the Generate Indicator Plot to view individual or overlaid graphs of selected technical indicators. If "Overlay" is selected, multiple indicators will be plotted on the same graph for comprehensive analysis.
  4. Adjust the timeframe directly from the Candlestick graph for more granular or broader data analysis.

__Assumptions__

  1.The data ingested into the database is pre-processed and cleaned, ensuring accurate calculations and visualizations
  2. Indicator have their default values for calculations
  3. Have Filled NAN values with both Forward and Back filling method [This is done after Data processing]
  4.   





