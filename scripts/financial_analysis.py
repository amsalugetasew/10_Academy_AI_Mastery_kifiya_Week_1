import pandas as pd
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.exponential_moving_average import exponential_moving_average as ema
import pynance as pn

class FinancialAnalysis:
    def __init__(self, dataframe):
        self.df = dataframe

    def SimpleMovingAverage(self, period=50):
        """
        Calculate the Simple Moving Average (SMA) of the stock's closing price.
        """
        self.df['SMA_50'] = sma(self.df['Close'].tolist(), period=period)

    def RelativeStrengthIndex(self, period=14):
        """
        Calculate the Relative Strength Index (RSI) of the stock's closing price.
        """
        self.df['RSI_14'] = rsi(self.df['Close'].tolist(), period=period)

    def MovingAverageConvergenceDivergence(self, short_period=12, long_period=26):
        """
        Calculate the MACD and Signal Line.
        """
        macd_values = macd(self.df['Close'].tolist(), short_period=short_period, long_period=long_period)
        self.df['MACD_Line'] = macd_values

        # Calculate the Signal Line (EMA of the MACD line)
        self.df['Signal_Line'] = ema(self.df['MACD_Line'].tolist(), period=9)

    def FinancialMetrics(self, symbol='AAPL', start='2020-01-01', end='2024-12-15'):
        """
        Fetch financial data for a given stock symbol and date range.
        """
        data = pn.data.get(symbol, start=start, end=end)
        return data
