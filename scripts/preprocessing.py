import pandas as pd
import matplotlib.pyplot as plt

class Preprocessing:
    def __init__(self, dataframe):
        """
        Initializes the Preprocessing class with the provided DataFrame.
        """
        self.dataframe = dataframe

    def determine_sentiment_category(self):
        """
        Determines sentiment categories based on sentiment scores
        and visualizes the distribution of sentiment categories.

        Assumes the DataFrame has a 'sentiment' column with sentiment scores.
        """
        if 'sentiment' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'sentiment' column. Please calculate sentiment scores first.")

        # Categorize sentiments
        self.dataframe['sentiment_category'] = self.dataframe['sentiment'].apply(
            lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
        )

        # Calculate sentiment proportions
        sentiment_counts = self.dataframe['sentiment_category'].value_counts(normalize=True)

        # Plot the distribution
        sentiment_counts.plot(kind='bar', color=['green', 'grey', 'red'])
        plt.title("Proportion of Sentiment Categories")
        plt.ylabel("Percentage")
        plt.xlabel("Sentiment")
        plt.show()

    # Obtain basic statistics for textual lengths (like headline length).
    def headline_length_statistics(self):
        """
        Calculates and displays basic statistics for headline lengths.

        Assumes the DataFrame has a 'headline' column containing text data.
        """
        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column. Please provide the correct input.")

        # Calculate headline lengths
        self.dataframe['headline_length'] = self.dataframe['headline'].apply(len)

        # Generate descriptive statistics
        length_stats = self.dataframe['headline_length'].describe()
        print("Headline Length Statistics:")
        print(length_stats)

        # Plot the distribution of headline lengths
        plt.figure(figsize=(10, 6))
        self.dataframe['headline_length'].hist(bins=20, color='blue', alpha=0.7)
        plt.title("Distribution of Headline Lengths")
        plt.xlabel("Headline Length")
        plt.ylabel("Frequency")
        plt.show()
        
    # Count the number of articles per publisher to identify which publishers are most active.
    def count_articles_per_publisher(self):
        """
        Counts the number of articles per publisher and visualizes the most active publishers.

        Assumes the DataFrame has a 'publisher' column.
        """
        if 'publisher' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'publisher' column. Please provide the correct input.")

        # Count the number of articles per publisher
        # publisher_counts
        
        # publisher_counts = self.dataframe['publisher'].value_counts()
        # publisher_counts = self.dataframe['publisher'].value_counts().sort_values(ascending=False)
        publisher_counts = self.dataframe['publisher'].value_counts().sort_values(ascending=False).head(30)



        # Print the number of articles per publisher
        print("Number of Articles Per Publisher:")
        print(publisher_counts)

        # Plot the distribution of articles per publisher
        plt.figure(figsize=(12, 6))
        publisher_counts.plot(kind='bar', color='purple', alpha=0.7)
        plt.title("Number of Articles Per Publisher of Top 30 Publisher")
        plt.xlabel("Publisher")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=45, ha="right")
        plt.show()
        
    
    # Analyze the publication dates to see trends over time, such as increased news frequency on particular days or during specific events.
    def analyze_publication_dates(self):
        """
        Analyzes the publication dates to identify trends over time,
        such as increased news frequency on particular days or during specific events.
        
        The method assumes the DataFrame has a 'date' column with datetime objects.
        """
        if 'date' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'date' column. Please provide the correct input.")

        # Ensure the 'date' column is in datetime format
        self.dataframe['date'] = pd.to_datetime(self.dataframe['date'], errors='coerce')

        # Drop rows with invalid or missing dates
        self.dataframe = self.dataframe.dropna(subset=['date'])

        # Extract additional date components for analysis
        self.dataframe['year'] = self.dataframe['date'].dt.year
        self.dataframe['month'] = self.dataframe['date'].dt.month
        self.dataframe['day'] = self.dataframe['date'].dt.day
        self.dataframe['day_of_week'] = self.dataframe['date'].dt.day_name()

        # Count the number of articles per day
        daily_counts = self.dataframe['date'].dt.date.value_counts().sort_index()

        # Plot the trend of articles over time
        plt.figure(figsize=(12, 6))
        daily_counts.plot(kind='line', color='blue')
        plt.title("Articles Published Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=45)
        plt.show()

        # Count articles by day of the week
        weekly_counts = self.dataframe['day_of_week'].value_counts().sort_index()

        # Plot the frequency of articles by day of the week
        plt.figure(figsize=(10, 6))
        weekly_counts.plot(kind='bar', color='orange', alpha=0.7)
        plt.title("Articles Published by Day of the Week")
        plt.xlabel("Day of the Week")
        plt.ylabel("Number of Articles")
        plt.show()

        # Count articles by month
        monthly_counts = self.dataframe['month'].value_counts().sort_index()

        # Plot the frequency of articles by month
        plt.figure(figsize=(10, 6))
        monthly_counts.plot(kind='bar', color='green', alpha=0.7)
        plt.title("Articles Published by Month")
        plt.xlabel("Month")
        plt.ylabel("Number of Articles")
        plt.show()

        # Count articles by year
        yearly_counts = self.dataframe['year'].value_counts().sort_index()

        # Plot the frequency of articles by year
        plt.figure(figsize=(10, 6))
        yearly_counts.plot(kind='bar', color='red', alpha=0.7)
        plt.title("Articles Published by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Articles")
        plt.show()
        
    def process_date_column(df, date_column, date_format=None):
        """
        Processes the date column in a DataFrame.
        
        Parameters:
            df (pd.DataFrame): The DataFrame containing the date column.
            date_column (str): The name of the date column to process.
            date_format (str, optional): The format of the date strings, if known.
        
        Returns:
            pd.DataFrame: The DataFrame with the processed date column.
        """
        # Convert the date column to datetime format
        if date_format:
            df[date_column] = pd.to_datetime(df[date_column], format=date_format)
        else:
            # Handle cases where the date string length might be inconsistent
            df[date_column] = df[date_column].apply(lambda x: x[:10] if len(x) > 10 else x)
            df[date_column] = pd.to_datetime(df[date_column])
        
        return df
