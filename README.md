__Stock Data Analysis: A Comprehensive Stock Data Processing and Analysis Platform__

This repository hosts an application designed to facilitate a comprehensive analysis of stock data. It encompasses both the front-end and back-end code necessary to process, analyze, and visualize financial data efficiently. Below is a detailed explanation of the architecture and various components of this application, alongside some instructions to access its features.


__Architecture Overview -->__

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


__Front-end Access Instructions -->__

To access and utilize the features of the front-end interface, follow these steps:

  1. Navigate to http://3.84.81.214/ using a browser (ensure to use the HTTP protocol).
  2. Utilize the Search Button to generate a Candlestick Graph and an Indicator Table based on the entered stock symbol.
  3. Click on the Generate Indicator Plot to view individual or overlaid graphs of selected technical indicators. If "Overlay" is selected, multiple indicators will be plotted on the same graph for comprehensive analysis.
  4. Adjust the timeframe directly from the Candlestick graph for more granular or broader data analysis.

     

__Assumptions -->__

  1. The data ingested into the database is pre-processed and cleaned, ensuring accurate calculations and visualizations
  2. The indicators utilize default parameter values for calculations to maintain consistency and reliability across different datasets.
  3. NaN values encountered in the dataset are addressed using both forward and backward filling methods, applied post the primary data processing phase to preserve data integrity and continuity


     
__Scope of Developments -->__

  1. Integration with PySpark : 

The current system operates predominantly on Python due to the necessity of utilizing a Python library for indicator calculations. In the future, these computations could be transitioned to PySpark to potentially streamline the process further and leverage the capabilities of Spark for data processing. This would involve rewriting the indicator calculation logic within the PySpark framework.

  2. Frontend Enhancements: 

The frontend interface, particularly the Indicator Table, warrants further development. Enhancing the graphical representation and functionality of the table would not only provide a more defined view of the data but could also enrich the user experience by making it more visually appealing and intuitive.

   3. Optimization and Scalability: 

As we anticipate larger volumes of data to be handled, there is a critical need to optimize the existing infrastructure to ensure scalability. This could include implementing more efficient data retrieval and processing mechanisms, as well as potentially exploring options for parallel computation to speed up data analytics processes.

