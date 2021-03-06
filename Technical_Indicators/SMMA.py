import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import yfinance as yf
yf.pdr_override()
import datetime as dt

# input
symbol = 'AAPL'
start = dt.date.today() - dt.timedelta(days = 365*2)
end = dt.date.today()

# Read data 
df = yf.download(symbol,start,end)

n = 10
SMMA = np.array([np.nan] * len(df['Adj Close']))
SMMA[n - 2] = df['Adj Close'][:n - 1].mean()
for i in range(n - 1, len(df['Adj Close'])):
    SMMA[i] = (SMMA [i - 1] * (n - 2) + 2 * df['Adj Close'][i]) / n

x = SMMA.reshape(-1,1)
data = pd.DataFrame.from_records(x)

df['SMMA'] = data.values

# Line Chart
plt.figure(figsize=(14,7))
plt.plot(df['Adj Close'])
plt.plot(df['SMMA'])
plt.title('Guppy Multiple Moving Averages of EMA')
plt.legend(loc='best')
plt.show()

# ## Candlestick with SMMA
from matplotlib import dates as mdates
dfc = df.copy()
dfc['VolumePositive'] = dfc['Open'] < dfc['Adj Close']
#dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc['Date'] = mdates.date2num(dfc['Date'].astype(dt.date))

from mplfinance.original_flavor import candlestick_ohlc
fig = plt.figure(figsize=(14,7))
ax1 = plt.subplot(111)
candlestick_ohlc(ax1,dfc.values, width=0.5, colorup='g', colordown='r', alpha=1.0)
ax1.plot(df['SMMA'], color='orange')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax1.grid(True, which='both')
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: 'g', False: 'r'})
ax1v.bar(dfc.Date, dfc['Volume'], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3*df.Volume.max())
ax1.set_title('Stock '+ symbol +' Closing Price of SMMA')
ax1.set_ylabel('Price')
plt.show()