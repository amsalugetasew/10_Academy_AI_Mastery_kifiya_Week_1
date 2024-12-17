# Visualization of Financial Analysis
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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



    def stock_sentiment_correlation(self, sentiment_correlation):
        """
        Plot the correlation heatmap between sentiment scores and stock prices.
        
        Parameters:
            sentiment_correlation (pd.DataFrame): DataFrame containing correlation values.
        """
        plt.figure(figsize=(10, 6))
        sns.heatmap(sentiment_correlation, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
        plt.title("Correlation Between Sentiment and Stock Prices")
        plt.xlabel("Stock Price Features")
        plt.ylabel("Sentiment Metrics")
        plt.show()
        
    
    def daily_return_over_time(self):
        """
        Plot daily stock returns over time.
        """
        df = df.sort_values(by='date')  # Sort the DataFrame by date

        # Compute daily stock returns as percentage change in 'Close'
        df['daily_return'] = df['Close'].pct_change() * 100  # Multiply by 100 to get percentage
        
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['date'], self.df['daily_return'], marker='o', linestyle='-', color='purple', label='Daily Returns')
        plt.axhline(0, color='red', linestyle='--', linewidth=0.8, label='Zero Return')
        plt.title("Daily Stock Returns Over Time")
        plt.xlabel("Date")
        plt.ylabel("Daily Return (%)")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        
        
    def scatter_sentiment_vs_returns(self):
        """
        Scatter plot for sentiment vs. daily returns.

        Parameters:
            merged_data (pd.DataFrame): DataFrame containing 'avg_sentiment_score' and 'daily_return' columns.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=self.df, 
            x='avg_sentiment_score', 
            y='daily_return', 
            hue='daily_return', 
            palette='coolwarm'
        )
        plt.title("Correlation Between Daily Returns and Average Sentiment Score")
        plt.xlabel("Average Sentiment Score")
        plt.ylabel("Daily Return (%)")
        plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
        plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
        plt.grid(True)
        plt.show()

    def daily_return_over_time(self):
        """
        Plot daily stock returns over time.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['date'], self.df['daily_return'], marker='o', linestyle='-', color='purple', label='Daily Returns')
        plt.axhline(0, color='red', linestyle='--', linewidth=0.8, label='Zero Return')
        plt.title("Daily Stock Returns Over Time")
        plt.xlabel("Date")
        plt.ylabel("Daily Return (%)")
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def k_means_cluster(self, n_clusters=3):
        """
        Perform K-Means clustering on sentiment scores and visualize the clusters.
        
        Parameters:
            n_clusters (int): Number of clusters for K-Means.
        """
        # Check if 'sentiment' column exists
        if 'sentiment_score' not in self.df.columns:
            raise ValueError("DataFrame must contain a 'sentiment' column for clustering.")
        
        # Prepare the sentiment scores for clustering
        scores = self.df['sentiment_score'].values.reshape(-1, 1)
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(scores)
        self.df['sentiment_cluster'] = kmeans.labels_
        
        # Visualize the clusters
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df.index, self.df['sentiment_score'], c=self.df['sentiment_cluster'], cmap='viridis', alpha=0.5)
        plt.title("K-Means Clustering of Sentiment Scores")
        plt.xlabel("Index")
        plt.ylabel("Sentiment Score")
        plt.colorbar(label='Cluster')
        plt.grid(True)
        plt.legend()
        plt.show()
        
    
    def freq_dist_inHistogram(self):
        """
        Plot the frequency distribution of sentiment scores as a histogram.
        """
        if 'sentiment_score' not in self.df.columns:
            raise ValueError("DataFrame must contain a 'sentiment' column to plot its distribution.")
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['sentiment_score'], bins=50, color='blue', edgecolor='black')
        plt.title("Distribution of Sentiment Scores")
        plt.xlabel("Sentiment Score")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()