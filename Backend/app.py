from flask_cors import CORS
from flask import Flask, request, jsonify
import boto3
import pandas as pd
import pandas_ta as ta
import json

# Initializing the DynamoDB resource using boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('application')

app = Flask(__name__)
CORS(app)

def fetch_data_from_dynamodb(symbol):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('symbol').eq(symbol)
    )
    return response['Items']
    
def clean_data(data):
    # Convert the date column to datetime and set it as the index
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    # Filter records between 9:15 AM and 3:30 PM
    filtered_df = data.between_time('09:15', '15:30')

    # Fill missing values in specified columns using Forward Fill method
    cols_to_fill = ['close', 'open', 'high', 'low', 'volume']
    filtered_df[cols_to_fill] = filtered_df[cols_to_fill].fillna(method='ffill')

    return filtered_df

def process_data(data, candle_interval):
#Defining the Interval Map to pass it according to the resample function
    interval_to_freq = {
        '1 Min': '1Min',
        '5 Min': '5Min',
        '30 Min': '30Min',
        '1 Hour': '1H',
        '4 Hour': '4H',
        '1 Day': 'D',
        '1 Week': 'W'
    }
    
    freq = interval_to_freq.get(candle_interval, '1D')
    
    df = data.copy()
    
    #Converting Columns to numeric before proceeding to calculations
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df_resampled = df.resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
   
    #Impute missing values by using forward-fill and back-fill methods to handle potential NaN entries generated by the previous operations
    df_resampled.fillna(method='ffill', inplace=True)
    df_resampled.fillna(method='bfill', inplace=True) 
    return df_resampled

def process_indicator_data(data):
    df = data.copy()

    #Calculation of all the 15 indicators using pandas-ta lib 
    df.ta.adx(append=True)
    df.ta.ao(append=True)
    df.ta.aroon(append=True)
    df.ta.atr(append=True)
    df.ta.cci(append=True)
    df.ta.chop(append=True)
    df.ta.ema(append=True)
    df.ta.hma(append=True)
    df.ta.ichimoku(append=True)
    df.ta.macd(append=True)
    df.ta.mom(append=True)
    df.ta.rsi(append=True)
    df.ta.sma(append=True)
    df.ta.uo(append=True)
    df.ta.willr(append=True)
    
    #Impute missing values by using forward-fill and back-fill methods to handle potential NaN entries generated by the previous operations
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True) 

    #Renamed Columns to pass easily through the requests and display on the UI  
    df.rename(columns={
    "ADX_14": "ADX",
    "AO_5_34": "AO",
    "AROOND_14": "AROON_DOWN",
    "AROONU_14": "AROON_UP",
    "AROONOSC_14": "AROON_OSC",
    "ATRr_14": "ATR",
    "CCI_14_0.015": "CCI",
    "CHOP_14_1_100": "CHOP",
    "EMA_10": "EMA",
    "HMA_10": "HMA",
    "MACD_12_26_9": "MACD",
    "MOM_10": "MOM",
    "RSI_14": "RSI",
    "SMA_10": "SMA",
    "UO_7_14_28": "UO",
    "WILLR_14": "WILLR",
    "ISA_9": "ICHIMOKU_SEN_A_9",
    "ISB_26": "ICHIMOKU_SEN_B_26",
    "ITS_9": "ICHIMOKU_TENKAN_SEN_9",
    "IKS_26": "ICHIMOKU_KIJUN_SEN_26",
    "ICS_26": "ICHIMOKU_CHIKOU_SPAN_26"
    }, inplace=True)
  
    return df 

#Below Function gets triggered when accessed by below endpoints, and returns a processed DF to plot the candle stick graph
@app.route('/process_data/<symbol>/<candle_interval>', methods=['GET'])
def get_processed_data(symbol, candle_interval):
    try:
        data = fetch_data_from_dynamodb(symbol)
        if not data:
            return jsonify({"error": f"No data found for symbol: {symbol}"}), 400
        else:
            clean_data_df = clean_data(pd.DataFrame(data))
            processed_data = process_data(clean_data_df, candle_interval)
            #Converting Timestamp to milliseconds as used HighCharts Lib
            return jsonify([[row.Index.timestamp() * 1000, row.open, row.high, row.low, row.close] for row in processed_data.itertuples()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Below Function gets triggered when accessed by below endpoints, and returns a processed DF to plot the indicator graph
@app.route('/indicator_plot/<symbol>/<candle_interval>/<indicator>', methods=['GET'])
def get_indicator_plot(symbol, candle_interval, indicator):
    try:
        data = fetch_data_from_dynamodb(symbol)
        if not data:
            return jsonify({"error": f"No data found for symbol: {symbol}"}), 400
        else:
            clean_data_df = clean_data(pd.DataFrame(data))
            processed_data = process_data(clean_data_df, candle_interval)
            indicator_plot = process_indicator_data(processed_data)
            #Converting Timestamp to milliseconds as used HighCharts Lib
            return jsonify([[row.Index.timestamp() * 1000, getattr(row, indicator)] for row in indicator_plot.itertuples()]) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        
#Below Function gets triggered when accessed by below endpoints, and returns a processed DF to plot the indicator table
@app.route('/indicator_table/<symbol>/<candle_interval>/<indicator>', methods=['GET'])
def get_indicator_table(symbol, candle_interval, indicator):
    try:
        data = fetch_data_from_dynamodb(symbol)
        if not data:
            return jsonify({"error": f"No data found for symbol: {symbol}"}), 400
        else:
            clean_data_df = clean_data(pd.DataFrame(data))
            
            # Process the cleaned data and generate the indicator table
            processed_data = process_data(clean_data_df, candle_interval)
            indicator_table = process_indicator_data(processed_data)
            
            if not indicator_table.empty:
                # Find the maximum timestamp from the index of indicator_table
                max_timestamp = indicator_table.index.max()
                
                # Now, filter the table to only include rows with the maximum timestamp (latest bucket)
                latest_bucket_data = indicator_table[indicator_table.index == max_timestamp]
                
                # Convert the DataFrame to a JSON object
                result_json = latest_bucket_data.reset_index().drop(columns=["close", "open", "high", "low", "date", "volume"]).round(2).to_json(orient='records', date_format='iso')

                return jsonify(json.loads(result_json))

            else:
                return jsonify({"error": "The indicator table is empty"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
