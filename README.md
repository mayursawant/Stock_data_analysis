# Stock_data_analysis
This Repo contains complete application code with Frontend and Backend to process the stock data 

Detailed explanation of the architecture and code
o Any assumptions that you have made
o Instructions for accessing the front end if implemented

Architecture:- 

1) Database 

--> Data has been hosted on the DynamoDB with the below schema, where the symbol is the primary key and the date is the secondary key 

 |-- date
 |-- close
 |-- open
 |-- high
 |-- low
 |-- volume
 |-- symbol


2) Server 

--> Have used t2.micro instance for this application 
--> Frontend and Backend code has been deployed on this same server 

3) Dataflow 

[Frontend]   --> [Argumenst passe using API Calls] --> [Backend] <---> Get Data from Dynamo DB
                                                           
[Frontend]   <--   [  Data passed using API Requests  ]     <--[Backend]



**Instructions for accessing the front-end **



Assumption:
