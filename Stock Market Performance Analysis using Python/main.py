import pandas as pd
import yfinance as yf #pip install yfinance
from datetime import datetime
import plotly.express as px #pip install plotly

# Verileri indireceğimiz tarih aralığını belirliyoruz
start_date = datetime.now() - pd.DateOffset(months=3)
end_date = datetime.now()

# İnceleyeceğimiz hisse senetlerini belirliyoruz
tickers = ['AAPL', 'MSFT', 'NFLX', 'GOOG']

# Her bir hisse senedi için veri depolamak için boş bir liste oluşturuyoruz
df_list = []

# Belirtilen hisse senetleri için verileri yfinance ile indirip df_list'e ekliyoruz
for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    df_list.append(data)

# Tüm hisse senetlerinin verilerini birleştirerek tek bir DataFrame'e dönüştürüyoruz
df = pd.concat(df_list, keys=tickers, names=['Ticker', 'Date'])
print(df.head())

# DataFrame'in index'ini sıfırlayarak düzgün bir yapı oluşturuyoruz
df = df.reset_index()
print(df.head())


# Hisse senetlerinin son 3 aydaki performansını görselleştiriyoruz
fig = px.line(df, x='Date', 
              y='Close', 
              color='Ticker', 
              title="Stock Market Performance for the Last 3 Months")
fig.show()

# Apple, Microsoft, Netflix ve Google için hisse senedi fiyatlarını görselleştiriyoruz
fig = px.area(df, x='Date', y='Close', color='Ticker',
              facet_col='Ticker',
              labels={'Date':'Date', 'Close':'Closing Price', 'Ticker':'Company'},
              title='Stock Prices for Apple, Microsoft, Netflix, and Google')
fig.show()

# Hareketli ortalamaları hesaplayarak DataFrame'e ekliyoruz
df['MA10'] = df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
df['MA20'] = df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)

# Hisseler için hareketli ortalamaları görselleştiriyoruz
for ticker, group in df.groupby('Ticker'):
    print(f'Moving Averages for {ticker}')
    print(group[['MA10', 'MA20']])
    
    for ticker, group in df.groupby('Ticker'):
        fig = px.line(group, x='Date', y=['Close', 'MA10', 'MA20'], 
                    title=f"{ticker} Moving Averages")
        fig.show()
        
# Hisselerin volatilitesini hesaplayarak DataFrame'e ekliyoruz      
df['Volatility'] = df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)

# Tüm şirketlerin volatilitesini görselleştiriyoruz
fig = px.line(df, x='Date', y='Volatility', 
              color='Ticker', 
              title='Volatility of All Companies')
fig.show()

# Apple ve Microsoft hisselerinin kapanış fiyatlarını içeren bir DataFrame oluşturuyoruz
apple = df.loc[df['Ticker'] == 'AAPL', ['Date', 'Close']].rename(columns={'Close': 'AAPL'})
microsoft = df.loc[df['Ticker'] == 'MSFT', ['Date', 'Close']].rename(columns={'Close': 'MSFT'})
df_corr = pd.merge(apple, microsoft, on='Date')

# Apple ve Microsoft arasındaki korelasyonu görselleştiriyoruz
fig = px.scatter(df_corr, x='AAPL', y='MSFT', 
                 trendline='ols', 
                 title='Correlation between Apple and Microsoft')
fig.show()