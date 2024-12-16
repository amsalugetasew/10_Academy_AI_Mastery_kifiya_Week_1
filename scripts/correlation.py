# correlation.py

import pandas as pd

class Correlation:
    def __init__(self, merged_df, news_df):
        """
        Initializes the Correlation class with two dataframes.
        :param merged_df: DataFrame with stock data
        :param news_df: DataFrame with news data
        """
        self.merged_df = merged_df
        self.news_df = news_df

    def aligned_date_stock_price(self):
        """
        Aligns stock data by finding rows in the stock data that match dates from the news dataset
        and displays the corresponding rows from the news data.
        :return: Three DataFrames - aligned stock data, aligned news data, and filtered sentiment data.
        """
        # Ensure both 'date' columns are in datetime format
        self.merged_df['date'] = pd.to_datetime(self.merged_df['date'])
        self.news_df['date'] = pd.to_datetime(self.news_df['date'])

        # Find common dates
        common_dates = self.merged_df['date'].isin(self.news_df['date'])

        # Filter stock data based on common dates
        aligned_stock_data = self.merged_df[common_dates]

        # Filter news data for the same common dates
        aligned_news_data = self.news_df[self.news_df['date'].isin(aligned_stock_data['date'])]

        # Filter sentiment data for common dates and specific stocks
        company_list = self.merged_df['stock'].unique()  # Get unique companies from merged_df
        common_conditions = (
            self.news_df['date'].isin(self.merged_df['date']) &
            self.news_df['stock'].isin(company_list)
        )
        aligned_sentiment_data = self.news_df[common_conditions]

        return aligned_stock_data, aligned_news_data, aligned_sentiment_data
