from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from pykrx import stock

def get_today():
  dt_now = str(datetime.now().date())
  print(f'{dt_now} 기준')
  dt_now = ''.join(c for c in dt_now if c not in '-')
  return dt_now

def MinMaxScaler(data):
  numerator = data - np.min(data, 0)
  denominator = np.max(data, 0) - np.min(data, 0)
  return numerator / (denominator + 1e-7)

def get_stock_data(): # 1
  ticker = "005930"
  dt_now = get_today() # today
  dt_now_tmp = datetime.strptime(dt_now, '%Y%m%d')    
  dt_past = dt_now_tmp - timedelta(days=365 * 5)    
  dt_past = dt_past.strftime('%Y%m%d') # 5 years ago

  df = stock.get_market_ohlcv_by_date(dt_past, dt_now, ticker)

  print(df.head())
  df.to_csv(f'./{dt_now}_samsung_stock.csv', index=True)

def set_stock_data(): # 2
  dt_now = get_today() # today
  df = pd.read_csv(f'./{dt_now}_samsung_stock.csv', index_col=0)

  dfx = df[['시가','고가','저가','종가', '거래량']]
  dfx = MinMaxScaler(dfx)
  dfy = dfx[['종가']]
  dfx = dfx[['시가','고가','저가','거래량']]

  dfx.to_csv(f'./{dt_now}_dfx.csv', index=True)
  dfy.to_csv(f'./{dt_now}_dfy.csv', index=True)

def prepare_data():
  window_size = 10
  dt_now = get_today() # today

  dfx = pd.read_csv(f'./{dt_now}_dfx.csv', index_col=0)
  dfy = pd.read_csv(f'./{dt_now}_dfy.csv', index_col=0)
  X = dfx.values.tolist()
  y = dfy.values.tolist()

  data_X = []
  data_y = []
  for i in range(len(y) - window_size):
      _X = X[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
      _y = y[i + window_size]     # 다음 날 종가
      data_X.append(_X)
      data_y.append(_y)
  print(_X, "->", _y)

  return data_X, data_y

def train_test_data():
  data_X, data_y = prepare_data()

  train_size = int(len(data_y) * 0.7)
  train_X = np.array(data_X[0 : train_size])
  train_y = np.array(data_y[0 : train_size])

  test_size = len(data_y) - train_size
  test_X = np.array(data_X[train_size : len(data_X)])
  test_y = np.array(data_y[train_size : len(data_y)])

  print('훈련 데이터의 크기 :', train_X.shape, train_y.shape)
  print('테스트 데이터의 크기 :', test_X.shape, test_y.shape)

  return train_size, train_X, train_y, test_size, test_X, test_y

def prepare_model():
  model = Sequential()
  model.add(LSTM(units=20, activation='relu', return_sequences=True, input_shape=(10, 4)))
  model.add(Dropout(0.1))
  model.add(LSTM(units=20, activation='relu'))
  model.add(Dropout(0.1))
  model.add(Dense(units=1))
  model.summary()

  return model

def train_model_predict(): # 3
  model = prepare_model()
  train_size, train_X, train_y, test_size, test_X, test_y = train_test_data()

  model.compile(optimizer='adam', loss='mean_squared_error')
  model.fit(train_X, train_y, epochs=70, batch_size=30)

  dt_now = get_today() # today
  df = pd.read_csv(f'./{dt_now}_samsung_stock.csv', index_col=0)
  dfy = pd.read_csv(f'./{dt_now}_dfy.csv', index_col=0)
  
  pred_y = model.predict(test_X)
  print("내일 삼성전자 주가 :", df.종가[-1] * pred_y[-1] / dfy.종가[-1], 'KRW')