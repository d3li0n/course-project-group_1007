import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Method to merge all .csv files into one, so we can enter all data
def merge_data():
  data = [files for files in os.listdir(os.path.join('..', '..', 'data','raw')) if files.endswith('.csv')]
  dataFrames = []

  for i in range(len(data)):
    dataFrames.append(pd.read_csv(r"{0}/{1}".format(os.path.join('..', '..', 'data','raw'), data[i]), low_memory=False))

  result = pd.concat(dataFrames, ignore_index=True)
  return load_and_process(result)

# Method Chaining
def load_and_process(result):
  # Method Chain 1 (Load data and deal with missing data)
  df1 = (
    result
      .dropna(subset=['Junction_Control'], how='all')
      .reset_index(drop=True)
  )
  # Method Chain 2 (Create new columns, drop others, and do processing)
  df2 = (
    df1.drop(['Accident_Index', 'Urban_or_Rural_Area', 'Location_Easting_OSGR', 'Location_Northing_OSGR', 
              'LSOA_of_Accident_Location', '1st_Road_Class', 
              '1st_Road_Number', 'Special_Conditions_at_Site',
              '2nd_Road_Class', '2nd_Road_Number', 'Junction_Detail', 
              'Local_Authority_(District)', 'Local_Authority_(Highway)'], axis=1)
        .reset_index(drop=True)
        .rename(columns={"Weather_Conditions": "Weather_Type", "Did_Police_Officer_Attend_Scene_of_Accident": "Police_Presense"})
        .replace({'Police_Presense': {'Yes': True, 'No': False}})
        .replace({'Day_of_Week': {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}})
        .convert_dtypes()
        .sort_values("Year", ascending=True)
  )
  df2['Date'] = pd.to_datetime(df2['Date'], format='%d/%m/%Y')

  return df2

def process_data(data):
  SPLIT_FILE_NUMBER = 12 # Number of files we want to split
  for i, merged_df in enumerate(np.array_split(data, SPLIT_FILE_NUMBER)): # Figuring out how we want to split data size between SPLIT_FILE_NUMBER
    print('🚨 Started to create formatted .csv file [{}/{}]\n'.format(i + 1, SPLIT_FILE_NUMBER)) # Displaying/testing if everything works properly
    with open('{}/out{}.csv'.format(os.path.join('..', '..', 'data','processed'), i + 1), "w") as new_file: # Creating file
      new_file.write(merged_df.to_csv()) # Writing data to new file
  print("👍 Finished creating formatted .csv files") # Showing result to confirm 