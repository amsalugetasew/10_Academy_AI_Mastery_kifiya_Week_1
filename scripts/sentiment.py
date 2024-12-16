import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        # Initialize the VADER Sentiment Analyzer
        self.sia = SentimentIntensityAnalyzer()

    def calculate_sentiment(self, df, text_column):
        """
        Calculates sentiment scores for the given text column in a DataFrame.
        
        Parameters:
            df (pd.DataFrame): DataFrame containing the text data.
            text_column (str): Name of the column containing text for sentiment analysis.
            
        Returns:
            pd.DataFrame: DataFrame with additional columns 'sentiment_score' and 'sentiment_category'.
        """
        # Apply sentiment analysis to calculate scores
        df['sentiment_score'] = df[text_column].apply(lambda x: self.sia.polarity_scores(x)['compound'])
        
        # Determine sentiment category based on sentiment score
        df['sentiment_category'] = df['sentiment_score'].apply(self.get_sentiment_category)
        
        # Convert sentiment category to numeric values
        df['sentiment'] = df['sentiment_category'].apply(self.get_sentiment_numeric)
        
        return df

    @staticmethod
    def get_sentiment_category(score):
        """
        Classifies sentiment into categories based on the sentiment score.
        
        Parameters:
            score (float): Sentiment score from VADER.
            
        Returns:
            str: Sentiment category ('positive', 'negative', 'neutral').
        """
        if score > 0.1:
            return 'positive'
        elif score < -0.1:
            return 'negative'
        else:
            return 'neutral'

    @staticmethod
    def get_sentiment_numeric(category):
        """
        Converts sentiment categories into numeric values: negative (-1), neutral (0), positive (1).
        
        Parameters:
            category (str): Sentiment category ('positive', 'negative', 'neutral').
            
        Returns:
            int: Numeric sentiment value (-1, 0, 1).
        """
        sentiment_mapping = {'negative': -1, 'neutral': 0, 'positive': 1}
        return sentiment_mapping.get(category, 0)

    @staticmethod
    def merge_sentiment_stock_price(stock_data, sentiment_data):
        """
        Merges stock price data with sentiment data based on date and stock.
        
        Parameters:
            stock_data (pd.DataFrame): DataFrame containing stock price data.
            sentiment_data (pd.DataFrame): DataFrame containing sentiment data.
            
        Returns:
            pd.DataFrame: Merged DataFrame containing aligned stock price and sentiment data.
        """
        # Select relevant columns from the sentiment data
        sentiment_columns = ['headline', 'publisher', 'date', 'stock', 'sentiment_score', 'sentiment_category', 'sentiment']
        
        # Merge the two datasets on date and stock
        merged_data = pd.merge(
            stock_data,
            sentiment_data[sentiment_columns],
            on=['date', 'stock'],
            how='left'
        )
        
        return merged_data

