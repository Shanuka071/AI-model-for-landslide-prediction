import pandas as pd
import numpy as np
import os

def load_and_process_data(filepath=None):
    # 1. Determine the file path robustly
    if filepath is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, 'ASPU DATA.xlsx')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Could not find the dataset at: {filepath}.")

    print(f"📂 Loading data from: {filepath}...")
    
    # 2. Load the Excel file
    try:
        df = pd.read_excel(filepath, sheet_name='qry_xdaily_data', header=0)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    # Drop completely empty rows
    df = df.dropna(how='all')

    # ⚠️ CRITICAL FIX: Convert all column names to strings
    # This ensures we can find '1', '2', '3', etc.
    df.columns = df.columns.astype(str)

    # 3. Identify columns
    id_vars = ['station_name', 'longitude', 'latitude', 'Year', 'Month']
    
    # Ensure day columns exist as strings
    day_cols = [str(i) for i in range(1, 32)]
    available_day_cols = [col for col in day_cols if col in df.columns]
    
    if not available_day_cols:
        # Print the actual columns for debugging if it fails
        print(f"Available columns: {df.columns.tolist()}")
        raise ValueError("❌ Could not find columns for days 1-31. Please check the Excel headers.")

    # 4. Melt the data from Wide to Long format
    print("🔄 Reshaping data from Wide to Long format...")
    df_long = pd.melt(
        df, 
        id_vars=id_vars, 
        value_vars=available_day_cols, 
        var_name='Day', 
        value_name='Rainfall_mm'
    )
    
    # 5. Clean up and handle missing values
    df_long['Day'] = pd.to_numeric(df_long['Day'], errors='coerce')
    df_long = df_long.dropna(subset=['Rainfall_mm'])
    
    # 6. Create a proper Date column
    df_long['Date'] = pd.to_datetime(df_long[['Year', 'Month', 'Day']], errors='coerce')
    df_long = df_long.dropna(subset=['Date'])
    df_long = df_long.sort_values(by=['station_name', 'Date']).reset_index(drop=True)
    
    # 7. Feature Engineering: Cumulative Rainfall
    print("⚙️ Engineering features (3-day and 7-day rolling averages)...")
    df_long['Rainfall_3day_avg'] = df_long.groupby('station_name')['Rainfall_mm'].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )
    df_long['Rainfall_7day_avg'] = df_long.groupby('station_name')['Rainfall_mm'].transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    )
    
    # 8. Create Target Labels
    print("🏷️ Generating Flood and Landslide Risk labels...")
    df_long['Flood_Risk'] = np.where(
        (df_long['Rainfall_mm'] > 100) | (df_long['Rainfall_3day_avg'] > 70), 1, 0
    )
    df_long['Landslide_Risk'] = np.where(
        (df_long['Rainfall_mm'] > 150) | (df_long['Rainfall_7day_avg'] > 100), 1, 0
    )
    
    print(f"✅ Data processing complete! Final dataset shape: {df_long.shape}")
    return df_long

if __name__ == "__main__":
    try:
        data = load_and_process_data()
        print(data.head())
    except Exception as e:
        print(f"❌ Error: {e}")