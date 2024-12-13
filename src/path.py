import pandas as pd 
import os 
import os

# Get the current working directory
current_dir = os.getcwd()

# Build the relative path

def get_path_price():
    # Path to the folder containing your CSV files
    folder_path = os.path.join(current_dir, '..', '..', 'week1_data', 'yfinance_data')
    # folder_path = 'C:/Users/Admin/Week1_data/yfinance_data'  # Replace with your folder path
    return folder_path
def get_path_news():
    # Path to the folder containing your CSV files
    folder_path = os.path.join(current_dir, '..', '..','week1_data', 'news', 'raw_analyst_ratings.csv')  # Replace with your folder path
    return folder_path

def new_load(path):
    return path



    
def load_news_csv(file_path):
    """Loads a single CSV file from a given path and converts it to a DataFrame."""
    try:
        # Check if the file exists and is a CSV
        if not os.path.isfile(file_path) or not file_path.endswith('.csv'):
            raise ValueError("The provided file path is invalid or not a CSV file.")
        
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if df.empty:
            print(f"Warning: The file at {file_path} is empty.")
            return None
        return df
    
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

