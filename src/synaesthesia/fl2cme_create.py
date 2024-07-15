import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    """
    This script is used to create labels from the fl2cme_vconf.csv file.
    This should eventually create a dataframe saved as csv file with the
    following columns:

    TO DO

    Index:
    Pandas datetime index for the whole range of the catalog. Make sure it
    has the same cadence as the data (12 minutes). Make sure to correctly
    interpolate all values for the whole range of dates!


    Possible target variables:

    - flareclass:
    A value between 0 and 3, where 0 is no flare, 1 is C class, 2 is M class,
    and 3 is X class. This is a possible target variable we could predict.

    - flare_timeline:
    Alternative way of predicting a flare. This is a numerical value that
    represents the time until the next flare in multiples of the cadence.
    This could be a regression target.

    - CME_associated:
    A boolean value indicating if there is a flare with an associated CME.
    Think about how to deal with different levels of cme_valid_confidence.

    - CME parameters such as cme_vel, cme_width, ...

    - think about other possible target variables
    """

    path = "/home/data/flare_labels/fl2cme_vconf.csv"

    # df = pd.read_csv(path)
   
    # print(df.columns)
    # print(df.head)
    
    # Index(['flare_id', 'start_time', 'peak_time', 'end_time', 'goes_class',
    #    'noaa_active_region', 'fl_lon', 'fl_lat', 'fl_loc_src', 'ssw_flare_id',
    #    'hinode_flare_id', 'primary_verified', 'secondary_verified',
    #    'candidate_ars', 'cme_id', 'fl_pa', 'cme_mpa', 'diff_a', 'cme_vel',
    #    'cme_width', 'cme_assoc_conf', 'cdaw_cme_id', 'cdaw_cme_width',
    #    'cdaw_cme_vel', 'cdaw_cme_pa', 'donki_cme_id', 'donki_cme_half_angle',
    #    'donki_cme_vel', 'lowcat_cme_id', 'lowcat_cme_width', 'lowcat_cme_vel',
    #    'lowcat_cme_pa', 'cme_valid_conf'],
    #   dtype='object')



    df_filtered = pd.read_csv(path, 
                            usecols=['flare_id', 'start_time', 'peak_time', 'end_time', 'goes_class', 'fl_lon', 'fl_lat'],
                            dtype={'flare_id': 'str',
                                    'goes_class': 'str',
                                    'fl_lon': 'float64',
                                    'fl_lat': 'float64'},
                            parse_dates=['start_time', 'peak_time', 'end_time'])
    
    
    # Plot flare location
    plt.figure(figsize=(10, 10))  # Set the figure size for better readability
    plt.scatter(df_filtered['fl_lon'], df_filtered['fl_lat'], color='red', alpha=0.5, s=10)  # Plot scatter with fl_lon as x and fl_lat as y
    
    # Set limits for x and y axes
    plt.xlim(-90, 90)
    plt.ylim(-90, 90)

    # Draw a circle centered at (0, 0) with radius 90
    circle = plt.Circle((0, 0), 90, color='blue', fill=False)
    plt.gca().add_artist(circle)
        
    plt.title('Flare Locations')  # Title of the plot
    plt.xlabel('Longitude (fl_lon)')  # X-axis label
    plt.ylabel('Latitude (fl_lat)')  # Y-axis label
    plt.grid(True)  # Show grid
    plt.savefig("fl2cme_flare_location.jpg")  # Display the plot
    
    
    # Debuging the issue with lat-lon flare location (1997-2010)
    # path = "/home/data/flare_labels/fl2cme_soho.csv"
        
    # df_soho = pd.read_csv(path, usecols=['flare_id', 'start_time', 'peak_time', 'end_time', 'goes_class', 'fl_lon', 'fl_lat', 'eit_lon', 'eit_lat'])

    # # Fixing errors in csv (two values have additional .0 at the end so can't be convert to float)
    # # Define a function to check if a cell contains two dots
    # def contains_two_dots(x):
    #     if isinstance(x, str):
    #         return x.count('.') == 2
    #     return False

    # # Apply this function across the DataFrame and filter rows
    # rows_with_two_dots = df_soho[df_soho.applymap(contains_two_dots).any(axis=1)]

    # # Display the filtered rows
    # print(rows_with_two_dots)

    # # breakpoint()
    # df_soho.loc[135, 'eit_lon'] = df_soho.loc[135, 'eit_lon'][:-2]
    # df_soho.loc[2127, 'eit_lon'] = df_soho.loc[2127, 'eit_lon'][:-2]
        
    # df_soho['eit_lon'] = df_soho['eit_lon'].astype('float64')

    # # breakpoint()

    # plt.figure(figsize=(10, 10))  # Set the figure size for better readability
    # plt.scatter(df_soho['fl_lon'], df_soho['fl_lat'], color='red', alpha=0.5, s=10)  # Plot scatter with fl_lon as x and fl_lat as y
    # plt.scatter(df_soho['eit_lon'], df_soho['eit_lat'], color='blue', alpha=0.5, s=10)  # Plot scatter with fl_lon as x and fl_lat as y

    
    # # Set limits for x and y axes
    # plt.xlim(-90, 90)
    # plt.ylim(-90, 90)

    # # Draw a circle centered at (0, 0) with radius 90
    # circle = plt.Circle((0, 0), 90, color='blue', fill=False)
    # plt.gca().add_artist(circle)
        
    # plt.title('Flare Locations')  # Title of the plot
    # plt.xlabel('Longitude (fl_lon)')  # X-axis label
    # plt.ylabel('Latitude (fl_lat)')  # Y-axis label
    # plt.grid(True)  # Show grid
    # plt.savefig("fl2cme_flare_location_soho.jpg")  # Display the plot
    


    # Min and max time of flares
    min_time_flares = np.min(df_filtered.start_time)
    max_time_flares = np.max(df_filtered.end_time)
    
    # Min and max time for the labels (0, 12, 24, 36, 48)
    min_time = min_time_flares.replace(minute=(min_time_flares.minute // 12) * 12, second=0, microsecond=0)
    max_time = max_time_flares.replace(minute=(max_time_flares.minute // 12) * 12+12, second=0, microsecond=0)

    # List of goes classes
    unique_goes_class = list(df_filtered['goes_class'].unique())
    
    # List of all timestamps
    timestamps = pd.date_range(start=min_time, end=max_time, freq='12min')

    # Create new DataFrame with 'timestamp' column
    df_flare_timestamp = pd.DataFrame(timestamps, columns=['timestamp'])

    # Create a column for storing class info
    df_flare_timestamp["flare_class"]=np.nan


    # Simplest version for classification
    # Use pandas to merge df_filtered with df_flare_timestamps
    # Find the closest date to peak_time and fill with the class name
    


    # # Create a dictionary where each key is a GOES class and each value is a Series of NaNs (or 0s) with the same index as df_flare_timestamp
    # columns_to_add = {goes_class: pd.Series(np.nan, index=df_flare_timestamp.index) for goes_class in unique_goes_class}

    # # Use pd.concat to add all the new columns at once
    # df_flare_timestamp = pd.concat([df_flare_timestamp, pd.DataFrame(columns_to_add)], axis=1)
  


    # # For regression
    # # fill the df with a time to the next flare and give 0 if flare is happening (i.e. it is in between start and end)
    
    
    
    # # For classificiation
    # # Fill the df with a tensor that shows if there is a flare within an hour for next 24 hours
    
    

    breakpoint()
    
