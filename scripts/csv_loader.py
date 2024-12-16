# Import necessary libraries
import os
import pandas as pd

# Define the CSVLoader class
class CSVLoader:
    def __init__(self, folder_path):
        """Initializes the CSVLoader with the folder path."""
        self.folder_path = folder_path
        self.dataframes = []

    def load_csv_files(self):
        """Loads all CSV files in the specified folder into dataframes, 
           adding a 'company' column with the first four characters of the file name."""
        # List all CSV files in the folder
        csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]        
        if not csv_files:
            print("No CSV files found in the folder!")
        
        # Loop through each CSV file and load it into a DataFrame
        for csv_file in csv_files:
            file_path = os.path.join(self.folder_path, csv_file)
            
            try:
                df = pd.read_csv(file_path)
                
                # Check if the DataFrame is empty
                if df.empty:
                    print(f"Warning: {csv_file} is empty and won't be added.")
                    continue
                
                # Add the 'company' column with the first four characters of the file name
                company_name = csv_file[:4] if len(csv_file) >= 4 else csv_file  # Handle short file names
                df['date'] = df['Date']
                df.drop(columns=['Date'], inplace=True)
                df['stock'] = company_name
                
                # Append the dataframe to the list
                self.dataframes.append(df)
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")
                
    def merge_dataframes(self):
        """Merges all loaded dataframes into one."""
        if not self.dataframes:
            raise ValueError("No dataframes loaded. Please load CSV files first.")
        
        # Merge all dataframes
        merged_df = pd.concat(self.dataframes, ignore_index=True)
        return merged_df
    
    
    
    def load_news_csv(self, file_path):
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
    

        


