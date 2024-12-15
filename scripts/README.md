

# Key Components of the Project
1. **Data Loading**
The dataset includes stock prices and sentiment data for seven companies.

**Stock prices**: Includes historical OHLC (Open, High, Low, Close) data.
**Sentiment data**: Derived from news articles, social media, or other sources.
Relevant Script: **csv_loader.py**

Automatically loads and formats the datasets.
2. **Data Transformation**
Prepares the data for analysis:

Handles missing values.
Standardizes date formats.
Merges stock prices and sentiment data for combined analysis.
Relevant Script: **preprocessing.py**

3. **Exploratory Data Analysis (EDA)**
Provides visual insights into:

Stock price trends over time.
Sentiment score distributions.
Correlations between stock prices and sentiment.
Relevant Script: **EDA.py**

4. **Time-Series Analysis**
Analyzes stock price data using time-series methods:

Moving averages.
Trend analysis.
Volatility estimation.
Relevant Script: **time_series.py**

5. **Sentiment Analysis**
Evaluates the impact of sentiment on stock prices:

Sentiment score aggregation by company and time period.
Statistical correlation analysis.
Optional machine learning models for predictive analysis.
Relevant Script: **insight.py**