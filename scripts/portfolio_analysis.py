import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class SentimentPortfolioAnalysis:
    def __init__(self, merged_df):
        """
        Initialize SentimentPortfolioAnalysis with merged sentiment and stock data.

        Parameters:
            merged_df (pd.DataFrame): Merged DataFrame containing sentiment and stock price data.
        """
        self.merged_df = merged_df
        self.portfolio_returns = None
        self.daily_returns = None
        self.assets = None

    def calculate_daily_returns(self):
        """
        Calculate daily returns for each stock in the merged dataset.
        """
        # Calculate daily returns using percent change for each stock
        self.merged_df['daily_return'] = self.merged_df.groupby('stock')['Close'].pct_change()
        print("Daily Returns Calculated Successfully.")
        self.daily_returns = self.merged_df.pivot_table(index='date', columns='stock', values='daily_return')

    def assign_sentiment_weights(self):
        """
        Assign weights to stocks based on sentiment scores.
        """
        # Normalize sentiment scores to determine portfolio weights
        self.merged_df['weight'] = self.merged_df['sentiment_score'] / self.merged_df.groupby('date')['sentiment_score'].transform('sum')
        print("Sentiment Weights Assigned Successfully.")

    def calculate_portfolio_returns(self):
        """
        Calculate portfolio returns by weighting daily returns based on sentiment scores.
        """
        # Calculate weighted return: Weight * Daily Return
        self.merged_df['weighted_return'] = self.merged_df['weight'] * self.merged_df['daily_return']

        # Aggregate weighted returns for each date
        self.portfolio_returns = self.merged_df.groupby('date')['weighted_return'].sum().reset_index()
        self.portfolio_returns['cumulative_return'] = (1 + self.portfolio_returns['weighted_return']).cumprod()
        print("Portfolio Returns Calculated Successfully.")

    def plot_portfolio_performance(self):
        """
        Plot cumulative portfolio returns over time.
        """
        if self.portfolio_returns is None:
            raise ValueError("Portfolio returns not calculated. Call calculate_portfolio_returns() first.")

        # Plot cumulative returns
        plt.figure(figsize=(10, 6))
        plt.plot(self.portfolio_returns['date'], self.portfolio_returns['cumulative_return'], marker='o', linestyle='-', color='purple')
        plt.title("Sentiment-Based Portfolio Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.grid(True)
        plt.show()
        print("Portfolio Performance Plot Generated.")

    def optimize_portfolio(self):
        """
        Optimize the portfolio for maximum Sharpe ratio using SciPy optimization.
        """
        # Step 1: Calculate expected returns and covariance matrix
        mu = self.daily_returns.mean()  # Mean historical returns
        cov_matrix = self.daily_returns.cov()  # Covariance matrix of returns
        num_assets = len(mu)

        # Step 2: Define objective functions and constraints
        def portfolio_performance(weights):
            portfolio_return = np.dot(weights, mu)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return portfolio_return, portfolio_volatility
        
        def negative_sharpe_ratio(weights, risk_free_rate=0.01):
            returns, volatility = portfolio_performance(weights)
            return -(returns - risk_free_rate) / volatility

        # Constraints: Weights sum to 1, and weights are between 0 and 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))

        # Initial guess for weights
        initial_weights = np.array([1. / num_assets] * num_assets)

        # Step 3: Use SciPy minimize function to maximize Sharpe ratio
        result = minimize(negative_sharpe_ratio, initial_weights, bounds=bounds, constraints=constraints)

        if result.success:
            optimized_weights = result.x
            portfolio_return, portfolio_volatility = portfolio_performance(optimized_weights)
            sharpe_ratio = -result.fun
            print("Optimized Portfolio Weights:", optimized_weights)
            print("Portfolio Return:", portfolio_return)
            print("Portfolio Volatility:", portfolio_volatility)
            print("Sharpe Ratio:", sharpe_ratio)
            return optimized_weights
        else:
            raise ValueError("Optimization failed:", result.message)

    def run_analysis(self):
        """
        Run the entire analysis pipeline with merged data.
        """
        self.calculate_daily_returns()
        self.assign_sentiment_weights()
        self.calculate_portfolio_returns()
        self.plot_portfolio_performance()
        optimized_weights = self.optimize_portfolio()
        return optimized_weights
