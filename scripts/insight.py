import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import nltk
nltk.download('vader_lexicon')

class Insight:
    def __init__(self, dataframe):
        """
        Initializes the Insight class with the provided DataFrame.
        """
        self.dataframe = dataframe

    def sentiment_analysis(self):
        """
        Perform sentiment analysis on the headlines to gauge the sentiment (positive, negative, neutral)
        and visualize the sentiment distribution.
        """
        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column. Please provide the correct input.")
        
        # Initialize sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Function to calculate sentiment score
        def calculate_sentiment(text):
            sentiment = analyzer.polarity_scores(text)
            return sentiment['compound']  # Return the compound score

        # Apply the sentiment analysis
        self.dataframe['sentiment'] = self.dataframe['headline'].apply(calculate_sentiment)

        # Categorize sentiment as positive, negative, or neutral
        self.dataframe['sentiment_category'] = self.dataframe['sentiment'].apply(
            lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
        )

        # Plot sentiment distribution
        sentiment_counts = self.dataframe['sentiment_category'].value_counts(normalize=True)
        sentiment_counts.plot(kind='bar', color=['green', 'red', 'grey'])
        plt.title("Proportion of Sentiment Categories")
        plt.ylabel("Percentage")
        plt.xlabel("Sentiment")
        plt.show()

    def topic_modeling(self, num_topics=5, num_words=10):
        """
        Perform topic modeling using Latent Dirichlet Allocation (LDA) to extract key topics from headlines.

        Args:
            num_topics (int): The number of topics to extract (default is 5).
            num_words (int): The number of top words to display for each topic (default is 10).
        """
        if 'headline' not in self.dataframe.columns:
            raise ValueError("The dataframe does not contain a 'headline' column. Please provide the correct input.")

        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
        
        # Fit the vectorizer to the headlines and transform the text data
        tfidf_matrix = vectorizer.fit_transform(self.dataframe['headline'])

        # Apply Latent Dirichlet Allocation (LDA)
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(tfidf_matrix)

        # Get the top words for each topic
        feature_names = np.array(vectorizer.get_feature_names_out())
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-num_words:][::-1]
            top_words = feature_names[top_words_idx]
            print(f"Topic {topic_idx + 1}:")
            print(" ".join(top_words))
            print("\n")

        # Optional: Visualize the distribution of topics for each article
        topic_distribution = lda.transform(tfidf_matrix)
        self.dataframe['dominant_topic'] = topic_distribution.argmax(axis=1)

        # Plot the distribution of topics across articles
        topic_counts = self.dataframe['dominant_topic'].value_counts()
        topic_counts.plot(kind='bar', color='purple', alpha=0.7)
        plt.title("Topic Distribution Across Articles")
        plt.xlabel("Topic")
        plt.ylabel("Number of Articles")
        plt.show()

    def plot_sentiment_vs_topic_distribution(self):
        """
        Plots sentiment distribution against topic distribution.
        This allows visualizing how sentiment varies across different topics.
        """
        # Check if necessary columns exist
        if 'dominant_topic' not in self.dataframe.columns:
            raise ValueError("Topic modeling should be run first. Please run the 'topic_modeling' method first.")

        if 'sentiment_category' not in self.dataframe.columns:
            raise ValueError("Sentiment analysis should be run first. Please run the 'sentiment_analysis' method first.")

        # Create a cross-tabulation of sentiment and topic
        sentiment_topic = pd.crosstab(self.dataframe['sentiment_category'], self.dataframe['dominant_topic'])

        # Plot sentiment vs. topic distribution
        sentiment_topic.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
        plt.title("Sentiment Distribution by Topic")
        plt.xlabel("Sentiment Category")
        plt.ylabel("Number of Articles")
        plt.legend(title="Topic", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
