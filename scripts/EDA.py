# EDA_analysis.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EDA:
    def __init__(self, dataframe):
        """
        Initializes the SentimentEDA class with the merged dataframe.
        """
        self.dataframe = dataframe

    
    def parse_dates(self):
        """
        Parses and converts dates to UTC format in the 'date' column. 
        Sorts the DataFrame by the 'date' column after parsing.
        """
        def parse_date(date):
            try:
                # Attempt parsing with the specific format
                dt = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
            except:
                try:
                    # Attempt automatic inference if the first attempt fails
                    dt = pd.to_datetime(date, errors='coerce')
                except:
                    return pd.NaT  # If all parsing fails, return NaT
            # Ensure tz-aware (convert to UTC)
            return dt.tz_convert('UTC') if dt is not pd.NaT and dt.tzinfo else dt.tz_localize('UTC')

        if 'date' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'date' column.")
        
        # Apply parsing to the 'date' column
        self.dataframe['date'] = self.dataframe['date'].apply(parse_date)
        # Drop rows with invalid dates (NaT)
        self.dataframe = self.dataframe.dropna(subset=['date'])
        # Sort the DataFrame by 'date'
        self.dataframe = self.dataframe.sort_values(by='date')
    
    def display_basic_info(self):
        """
        Displays basic information about the dataset, including null values, data types, and shape.
        """
        print("Dataset Info:")
        print(self.dataframe.info())
        print("\nMissing Values:")
        print(self.dataframe.isnull().sum())
        print(f"\nDataset Shape: {self.dataframe.shape}")
        
    def plot_sentiment_distribution(self):
        """
        Plots the distribution of sentiment categories.
        a 'headline' column exists.
        """
        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column.")
        
        sns.countplot(data=self.dataframe, x='headline', palette='viridis')
        plt.title("Sentiment Category Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.show()

    def visualize_word_counts(self):
        """
        Visualizes the number of words in headlines across sentiment categories.
        Assumes a 'headline' column exists.
        """
        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column.")
        
        self.dataframe['word_count'] = self.dataframe['headline'].str.split().apply(len)
        sns.boxplot(data=self.dataframe, x='sentiment_category', y='word_count', palette='coolwarm')
        plt.title("Word Count by Sentiment")
        plt.xlabel("Sentiment")
        plt.ylabel("Word Count")
        plt.show()

    def correlation_heatmap(self):
        """
        Plots a heatmap of correlations for numerical features in the dataset.
        """
        numerical_data = self.dataframe.select_dtypes(include=['float64', 'int64'])
        if numerical_data.empty:
            print("No numerical features found for correlation heatmap.")
            return
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title("Correlation Heatmap")
        plt.show()
        

    
    def sentiment_score(self):
        """
        Calculates sentiment scores for text data in the 'headline' column using SentimentIntensityAnalyzer.
        """
        
        analyzer = SentimentIntensityAnalyzer()

        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column.")
        
        def calculate_sentiment(text):
            sentiment = analyzer.polarity_scores(text)
            return sentiment['compound']  # Use the compound score
        
        # Apply sentiment calculation
        self.dataframe['sentiment'] = self.dataframe['headline'].apply(calculate_sentiment)
        print(self.dataframe[['headline', 'sentiment']].head())

    def setement_category(self):
        """
        Categorizes sentiment based on sentiment scores and visualizes the proportions.
        """
        if 'sentiment' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'sentiment' column. Please calculate sentiment scores first.")
        
        # Categorize sentiments
        self.dataframe['sentiment_category'] = self.dataframe['sentiment'].apply(
            lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
        )
        
        # Calculate and plot proportions
        sentiment_counts = self.dataframe['sentiment_category'].value_counts(normalize=True)
        sentiment_counts.plot(kind='bar', color=['green', 'grey', 'red'])
        plt.title("Proportion of Sentiment Categories")
        plt.ylabel("Percentage")
        plt.xlabel("Sentiment")
        plt.show()
