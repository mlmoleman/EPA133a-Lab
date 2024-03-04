import pandas as pd
import numpy as np

# Retrieve the Bridge dataframe
df = pd.read_csv('../data/bridges_cleaned.csv')

# Create a subset of the dataframe containing only bridges on road N1
df_N1 = df[df['road']=='N1']
# Sort the dataframe based on km, so the bridges follow the correct order
df_N1_sorted = df_N1.sort_values(by='km', ascending = False).reset_index().drop(labels='index', axis=1)
# Create a list of the indexes
index = df_N1_sorted.index

def create_links(df, indexes):
    # Create an empty dictionary
    inserting_links = {}
    # Loop over all the bridges, skipping the first one
    for i in index[1:]:
        # Determine the latitude of the bridge
        lat = df.iloc[i, df.columns.get_indexer(['lat'])].values
        # Determine the longitude of the bridge
        lon = df.iloc[i, df.columns.get_indexer(['lon'])].values
        # Determine the latitude of the previous bridge
        lat_prev = df.iloc[i-1, df.columns.get_indexer(['lat'])].values
        # Determine the longitude of the previous bridge
        lon_prev = df.iloc[i-1, df.columns.get_indexer(['lon'])].values
        # Check if the lat and lon of this bridge and the previous bridge are not the same
        if not (lat == lat_prev and lon == lon_prev):
            # if that is the case insert link
            # determine the length of the link by calculating the difference in km of the bridges
            # and substracting half of the length of the bridges.
            length = (1000*df.iloc[i, df.columns.get_indexer(['km'])].values
                      - 1000*df.iloc[i-1, df.columns.get_indexer(['km'])].values
                      - 0.5*df.iloc[i, df.columns.get_indexer(['length'])].values
                      - 0.5*df.iloc[i-1, df.columns.get_indexer(['length'])].values)
            # Calculate the km of the link by taking the average
            km = (df.iloc[i, df.columns.get_indexer(['km'])].values[0]+df.iloc[i-1, df.columns.get_indexer(['km'])].values[0])/2
            # Calculate the latitude of the link by interpolating
            lat = (df.iloc[i, df.columns.get_indexer(['lat'])].values[0]+df.iloc[i-1, df.columns.get_indexer(['lat'])].values[0])/2
            # Calculate the longitude of the link by interpolating
            lon = (df.iloc[i, df.columns.get_indexer(['lon'])].values[0]+df.iloc[i-1, df.columns.get_indexer(['lon'])].values[0])/2
            # Add the link to the dictionary with the necessary attributes
            inserting_links[i] = {'road': ['N1'], 'km': [km], 'type': ['link'], 'name': ['link'], 'length': [round(length[0])], 'lat': [lat], 'lon': [lon]}
    return inserting_links

dict_links = create_links(df_N1_sorted, index)

dict_links = create_links(df_N1_sorted, index)
#%%
# Create a function to insert the links into the main dataframe
def insert_links(df, dict_links):
    # Make a copy of the dataframe
    main_df = df.copy()
    # create a list of the indexes of the links to insert
    index_links = list(dict_links.keys())
    # Loop over the links in the dictionary
    for link in dict_links:
        # update the index by adding the index of the link in the list
        # so that the links that are already added to the dataframe are taken into account
        index = link + index_links.index(link)
        # create a dataframe based on the link we want to insert
        df_insert = pd.DataFrame(dict_links[link])
        # Add the link to the main dataframe by concatting the dataframe until the index,
        # the link dataframe and the dataframe from the index
        main_df = pd.concat([main_df.iloc[:index, ], df_insert, main_df.iloc[index:, ]])
    # Reset the index of the main dataframe
    main_df = main_df.reset_index(drop=True)
    # Return the dataframe
    return main_df

# Call the function to check the outcome
main_df = insert_links(df_N1_sorted, dict_links)

# Convert dataframe into csv
main_df.to_csv('../data/bridges_cleaned_linked.csv')