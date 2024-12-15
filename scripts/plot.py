# Visualization of Financial Analysis
import plotly.graph_objects as go

class StockPlot:
    def __init__(self, dataframe):
        self.df = dataframe

    def StockPrice50DaySMA(self):
        """
        Plot Stock Price with 50-Day Simple Moving Average (SMA).
        """
        fig = go.Figure()

        # Add Close Price
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))
        
        # Add 50-Day SMA
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['SMA_50'], mode='lines', name='50-Day SMA', line=dict(color='orange')))

        # Customize layout
        fig.update_layout(
            title='Stock Price with 50-Day Simple Moving Average (SMA)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            template='plotly_dark',  # You can change to other templates or customize
            plot_bgcolor='rgba(240, 240, 240, 0.85)',  # Light gray background
            paper_bgcolor='rgba(255, 255, 255, 1)',  # White paper background
            font=dict(color='black')  # Black text color
        )
        fig.show()

    def RSIPlot(self):
        """
        Plot the RSI (Relative Strength Index).
        """
        fig = go.Figure()

        # Add RSI line
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['RSI_14'], mode='lines', name='RSI (14)', line=dict(color='green')))
        
        # Add Overbought and Oversold levels
        fig.add_trace(go.Scatter(x=self.df.index, y=[70] * len(self.df), mode='lines', name='Overbought (70)', line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=self.df.index, y=[30] * len(self.df), mode='lines', name='Oversold (30)', line=dict(color='blue', dash='dash')))

        # Customize layout
        fig.update_layout(
            title='RSI (Relative Strength Index)',
            xaxis_title='Date',
            yaxis_title='RSI Value',
            template='plotly_dark',  # Change template for different look
            plot_bgcolor='rgba(240, 240, 240, 0.85)',  # Light gray background
            paper_bgcolor='rgba(255, 255, 255, 1)',  # White paper background
            font=dict(color='black')  # Black text color
        )
        fig.show()

    def MACDPlot(self):
        """
        Plot MACD (Moving Average Convergence Divergence) and Signal Line.
        """
        fig = go.Figure()

        # Add MACD line
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['MACD_Line'], mode='lines', name='MACD Line', line=dict(color='purple')))
        
        # Add Signal line
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['Signal_Line'], mode='lines', name='Signal Line', line=dict(color='red', dash='dash')))
        
        # Add MACD Histogram
        fig.add_trace(go.Bar(x=self.df.index, y=self.df['MACD_Line'] - self.df['Signal_Line'], name='MACD Histogram', marker=dict(color='gray', opacity=0.3)))

        # Customize layout
        fig.update_layout(
            title='MACD and Signal Line',
            xaxis_title='Date',
            yaxis_title='Value',
            template='plotly_dark',  # You can change to other templates or customize
            plot_bgcolor='rgba(240, 240, 240, 0.85)',  # Light gray background
            paper_bgcolor='rgba(255, 255, 255, 1)',  # White paper background
            font=dict(color='black')  # Black text color
        )
        fig.show()
