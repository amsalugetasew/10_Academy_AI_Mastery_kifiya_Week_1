import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# from EDA import EDA
from preprocessing import Preprocessing
class TimeSeries:
    def __init__(self, dataframe):
        """
        Initializes the TimeSeries class with the provided DataFrame and preprocesses the date column.
        """
        # Use the Preprocessing class to parse the date column
        date_transformation = Preprocessing()
        self.dataframe = date_transformation.process_date_column(dataframe, 'date')
        
        # preprocessing.process_date_column()  # Assuming this method handles all date parsing logic
        # self.dataframe = preprocessing.dataframe  # Use the preprocessed DataFrame
        
        # eda = EDA(dataframe)
        # eda.parse_dates()
        # self.dataframe = eda.dataframe  # Preprocess the DataFrame during initialization

    def analyze_publication_frequency(self, time_unit='D'):
        """
        Analyze how the publication frequency varies over time. This method can identify any spikes
        in article publications related to specific market events. The time unit can be 'D' for daily,
        'W' for weekly, 'M' for monthly, or 'H' for hourly frequency.
        
        Args:
            time_unit (str): The frequency for resampling. Options are 'D', 'W', 'M', or 'H'.
        """
        # Set 'date' as the index for time series analysis
        self.dataframe.set_index('date', inplace=True)

        # Resample by the specified time unit and count the number of articles published in each period
        publication_frequency = self.dataframe.resample(time_unit).size()

        # Plot the publication frequency over time
        plt.figure(figsize=(12, 6))
        publication_frequency.plot(kind='line', color='blue')
        plt.title(f"Publication Frequency Over Time ({time_unit})")
        plt.xlabel("Time")
        plt.ylabel("Number of Articles Published")
        plt.grid(True)
        plt.show()

    def analyze_publishing_times(self):
        """
        Analyze the publishing times to identify if there's a specific time of day, week, or month when most news is released.
        This can be useful for traders and automated trading systems to identify patterns in market-related news.
        """
        # Extract time-related features from the 'date' column
        self.dataframe['hour'] = self.dataframe['date'].dt.hour
        self.dataframe['day_of_week'] = self.dataframe['date'].dt.dayofweek
        self.dataframe['month'] = self.dataframe['date'].dt.month

        # Analyze the publication times based on the hour of the day
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.dataframe, x='hour', palette='viridis')
        plt.title("Publication Frequency by Hour of the Day")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Number of Articles Published")
        plt.grid(True)
        plt.show()

        # Analyze the publication frequency by day of the week
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.dataframe, x='day_of_week', palette='viridis')
        plt.title("Publication Frequency by Day of the Week")
        plt.xlabel("Day of the Week")
        plt.ylabel("Number of Articles Published")
        plt.grid(True)
        plt.show()

        # Analyze the publication frequency by month
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.dataframe, x='month', palette='viridis')
        plt.title("Publication Frequency by Month")
        plt.xlabel("Month")
        plt.ylabel("Number of Articles Published")
        plt.grid(True)
        plt.show()

    def analyze_publishers(self):
        """
        Analyze the publishers contributing to the news feed. Identify which publishers are most active,
        and check if there are unique domains or organizations contributing more frequently. 
        The analysis will also consider sentiment and type of news reported.
        """
        if 'publisher' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'publisher' column. Please provide the correct input.")

        # Count the number of articles published by each publisher
        publisher_counts = self.dataframe['publisher'].value_counts()

        # Plot the number of articles published by each publisher
        plt.figure(figsize=(12, 6))
        publisher_counts.head(10).plot(kind='bar', color='lightblue')
        plt.title("Top 10 Most Active Publishers")
        plt.xlabel("Publisher")
        plt.ylabel("Number of Articles Published")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        # If email addresses are used as publisher names, extract unique domains
        if self.dataframe['publisher'].str.contains('@').any():
            self.dataframe['publisher_domain'] = self.dataframe['publisher'].apply(
                lambda x: x.split('@')[-1] if isinstance(x, str) else None
            )
            domain_counts = self.dataframe['publisher_domain'].value_counts()

            # Plot the most frequent publisher domains
            plt.figure(figsize=(12, 6))
            domain_counts.head(10).plot(kind='bar', color='orange')
            plt.title("Top 10 Most Frequent Publisher Domains")
            plt.xlabel("Domain")
            plt.ylabel("Number of Articles Published")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()

        # Analyzing sentiment per publisher to see which publishers have positive, negative, or neutral news
        if 'sentiment' in self.dataframe.columns:
            publisher_sentiment = self.dataframe.groupby('publisher')['sentiment'].mean()

            # Plot the average sentiment of articles by publisher
            plt.figure(figsize=(12, 6))
            publisher_sentiment.sort_values().head(10).plot(kind='bar', color='purple')
            plt.title("Average Sentiment of Articles by Publisher")
            plt.xlabel("Publisher")
            plt.ylabel("Average Sentiment")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()

    
    
    def analyze_correlation(self, stock_df):
        """
        Analyze the correlation between sentiment scores and stock price changes.
        """
        self.dataframe['date'] = self.dataframe['date'].dt.date
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])

        stock_df['Price_Change'] = stock_df['Close'].pct_change()
        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        self.dataframe['sentiment'] = self.dataframe['headline'].apply(
            lambda x: sentiment_map.get(x, 0)
        )

        merged_df = pd.merge(
            self.dataframe, stock_df,
            left_on=['date', 'stock'],
            right_on=['Date', 'company'],
            how='inner'
        )

        correlation_data = merged_df.groupby('sentiment')['Price_Change'].mean()
        print("Correlation data:")
        print(correlation_data)

        corr_matrix = merged_df[['sentiment', 'Price_Change']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title("Correlation Between Sentiment and Stock Price Change")
        plt.show()