from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from app import BaseDetails, RunningDetails
# SQLAlchemy database setup
engine = create_engine('sqlite:///C:/driver gui project/webapp/instance/data.db')
Session = sessionmaker(bind=engine)
session = Session()

# Function to export data to Excel files
def export_data_to_excel():
    # Query BaseDetails and RunningDetails
    base_details_query = session.query(BaseDetails).statement
    running_details_query = session.query(RunningDetails).statement
    
    # Read data into DataFrames
    base_details_df = pd.read_sql(base_details_query, engine)
    running_details_df = pd.read_sql(running_details_query, engine)
    
    # Merge BaseDetails and RunningDetails on 'vehicle' column
    merged_df = pd.merge(base_details_df, running_details_df, on='id')
    
    # Group merged data by 'vehicle' and export to Excel
    for vehicle_no, group_df in merged_df.groupby('vehicle'):
        output_file = f'C:/data/{vehicle_no}.xlsx'
        
        if os.path.exists(output_file):
            # Append to existing Excel file without headers
            existing_data = pd.read_excel(output_file, header=None)
            print(existing_data)
            print(group_df)
            # Convert the first row to header
            new_header = existing_data.iloc[0]  # First row for header
            existing_data = existing_data[1:]  # Take the data less the header row
            existing_data.columns = new_header  # Set the header row as the dataframe header
            updated_data = pd.concat([existing_data, group_df], ignore_index=True)
            updated_data.to_excel(output_file, index=False, header=True)
            print(updated_data)
            print(f"Data appended to {output_file} below existing content.")
        else:
            # Create new Excel file with data and without headers
            group_df.to_excel(output_file, index=False, header=True)
            print(f"Data exported to new file: {output_file} with headers.")
    
    # Delete all data from the database tables
    session.query(BaseDetails).delete()
    session.query(RunningDetails).delete()
    
    # Commit the changes and close the session
    session.commit()
    session.close()

# Export data to Excel files
export_data_to_excel()
