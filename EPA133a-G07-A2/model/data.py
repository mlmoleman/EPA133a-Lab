import pandas as pd
import random
import os

def convert_data():
    """
    Converts data conform demo data files.
    """

    # import data
    path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    df = pd.read_excel(path+'\\data\\bridges.xlsx')
    


    # slice data information
    df = df[["road", "km", "type", "name", "length", "condition", "lat", "lon"]]
    
    # HANDLING MISSING VALUES

    # change NaN values in name with dot i.e. '.'
    df['name'].fillna('.', inplace=True)
    
    # check NaN values in other columns, only length has missing values
    df.isnull().sum(axis = 0)
    
    # assign new dataframe to missing values
    missing = df[df.length.isnull()]
    
    # for some missing values, missing values can be retrieved from bridges with same chainage, 
    # get length of these bridges and replace missing value with this value. 
    for index in missing.index:  
        if df.loc[index, 'km'] == df.loc[index-1, 'km']: 
            # assign length of bridge with same chainage to variable new_length
            new_length = df.loc[index-1, 'length']
            # replace missing value with new length
            df.loc[index, 'length'] = new_length

        elif df.loc[index, 'km'] == df.loc[index+1, 'km']: 
            new_length = df.loc[index+1, 'length']
            df.loc[index, 'length'] = new_length
        
    # update missing value dataframe
    updated_missing = df[df.length.isnull()]
    
    # for the left-over missing values, replace length with average length of bridges for specific road
    for index in missing.index:
        road_name = df.loc[index, 'road']
        road_subset = df[df['road'] == road_name]
        average_length = road_subset.loc[:, 'length'].mean()
        df.loc[index, 'length'] = average_length
      
    
    # HANDLING DUPLICATES
    
    # change type of column first
    df['name'] = df['name'].astype(str)

    # replace modifications of right/left in bridge names
    df['name'] = df['name'].apply(lambda x: x.replace(')', ''))
    df['name'] = df['name'].apply(lambda x: x.replace('RIGHT', 'R'))
    df['name'] = df['name'].apply(lambda x: x.replace('LEFT', 'L'))
    df['name'] = df['name'].apply(lambda x: x.replace('Right', 'R'))
    df['name'] = df['name'].apply(lambda x: x.replace('Left', 'L'))
    
    # strip the trailing whitespaces 
    df['name'] = df['name'].apply(lambda x: x.strip())
    
    # define dataframe for duplicates
    duplicateRows = df[df['road'] == 'N1']
    # subset based on latitude and longitude
    duplicateRows = duplicateRows[duplicateRows.duplicated(subset=['lat', 'lon'])]
    # sort by chainage
    duplicateRows.sort_values(by=['km'])
    # change condition from letters to numbers in order to compare them
    df['conditionNum'] = 0
    df.loc[df['condition'] == 'A', 'conditionNum'] = 1
    df.loc[df['condition'] == 'B', 'conditionNum'] = 2
    df.loc[df['condition'] == 'C', 'conditionNum'] = 3
    df.loc[df['condition'] == 'D', 'conditionNum'] = 4
    # initialize a list for indexes to remove after running for-loop
    remove_index = []

    # for index in dataframe with duplicates
    for index in duplicateRows.index: 
        # retrieve latitude and longitude
        latitude = df.loc[index, 'lat'] 
        longitude = df.loc[index, 'lon']

        # define a subset of duplicates based on the latitude and longitude
        subset = df.loc[((df['lat'] == latitude) & (df['lon'] == longitude))] 

        # define lists for bridges with left, right, or neither in their name
        contains_left = []
        contains_right = []
        contains_none = []

        for index in subset.index: 
            # for every row in subset, retrieve condition and assign to set
            condition = subset.loc[index, 'conditionNum']
            # define the set with both index and condition
            condition_set = (index, condition)

            # retrieve name and whether L or R in name
            name = subset.loc[index, 'name']
            last_letter = name[-1:]
            # check whether last letter is R, L, or something else
            if last_letter == 'R': 
                contains_right.append(condition_set)

            elif last_letter == 'L': 
                contains_left.append(condition_set)

            else: 
                contains_none.append(condition_set)   

        # when no left and right in name, but other letters
        if len(contains_left) == 0 and len(contains_right) == 0 and len(contains_none) > 0: 
            # check whether conditions of bridges are equal
            if contains_none[0][1] == contains_none[1][1]: 
                # if so, pick random index and append to list
                random_none = random.choice(contains_none)
                remove_index.append(random_none[0])

            # if condition of one is greater than other, remove the highest one
            # better be safe than sorry
            elif contains_none[0][1] < contains_none[1][1]: 
                remove_index.append(contains_none[0][0])

            elif contains_none[0][1] > contains_none[1][1]: 
                remove_index.append(contains_none[1][0])

        # capitalized one is often an updated version, we assume. Hence, remove the left and right
        if len(contains_left) == 1 and len(contains_right) == 1 and len(contains_none) == 1: 
            for element in contains_left: 
                remove_index.append(element[0])
            for element in contains_right: 
                remove_index.append(element[0])

        # if two times left
        if len(contains_left) == 2: 
            # check whether conditions are equal
            if contains_left[0][1] == contains_left[1][1]: 
                # then randomly pick one
                random_left = random.choice(contains_left)
                remove_index.append(random_left[0])

            # else check which condition is better, remove that one
            elif contains_left[0][1] < contains_left[1][1]: 
                remove_index.append(contains_left[0][0])

            elif contains_left[0][1] > contains_left[1][1]: 
                remove_index.append(contains_left[1][0])

        # same structure as with left, now for right
        if len(contains_right) == 2: 
            if contains_right[0][1] == contains_right[1][1]: 
                random_left = random.choice(contains_right)
                remove_index.append(random_left[0])

            elif contains_right[0][1] < contains_right[1][1]: 
                remove_index.append(contains_right[0][0])

            elif contains_right[0][1] > contains_right[1][1]: 
                remove_index.append(contains_right[1][0])

        # if left and capital, remove left one
        if len(contains_left) == 1 and len(contains_none) == 1: 
            for element in contains_left: 
                remove_index.append(element[0])

        # if right and capital, remove right one
        if len(contains_right) == 1 and len(contains_none) == 1: 
            for element in contains_right: 
                remove_index.append(element[0])

        # if both right and left, keep both 
        if len(contains_right) == 1 and len(contains_left) == 1 and len(contains_none) == 0: 
            continue

    # only retrieve unique indexes in list, otherwise we remove all
    used = set()
    unique_indexes = [x for x in remove_index if x not in used and (used.add(x) or True)]

    # remove all the indexes in removing list
    for element in unique_indexes: 
        df = df.drop(index = element)
        
        
    # FORMAT DATAFRAME CONFORM DEMO FILES
    
    # reset index
    df = df.reset_index()
    
    # drop unnecessary columns
    df = df.drop("conditionNum", axis='columns')
    df = df.drop("index", axis='columns')
    
    # add model type
    df['model_type'] = 'bridge'
    
    # import roads to get source and sink

    df_roads = pd.read_csv(path+"\\EPA133a-G07-A2\\data\\roads.csv")
    # select only N1 data entries
    df_roads = df_roads[df_roads['road'] == 'N1']
    
    # assign first column to new dataframe
    df_roads_0 = df_roads[0:1]
    # retrieve source characteristics
    road_name = df_roads_0.road[0]
    km = df_roads_0.chainage[0]
    lrp = df_roads_0.lrp[0]
    latitude = df_roads_0.lat[0]
    longitude = df_roads_0.lon[0]
    type_of_bridge = 'source'
    bridge_name = 'source'
    length = 0
    condition = 'A'
    
    # subset dataframe based on N1 road
    df = df[df['road'] == 'N1']
    
    # adding new row
    df.loc[-1] = [road_name, km, type_of_bridge, bridge_name, length, 
                  condition, latitude, longitude, type_of_bridge]  
    # shifting index
    df.index = df.index + 1  
    # sort index
    df.sort_index(inplace=True) 
    
    # assign last column to new dataframe
    df_roads_last = df_roads[-1::]
    # reset index
    df_roads_last = df_roads_last.reset_index()
    # retrieve sink characteristics
    road_name = df_roads_last.loc[0, 'road']
    km = df_roads_last.loc[0, 'chainage']
    lrp = df_roads_last.loc[0, 'lrp']
    latitude = df_roads_last.loc[0, 'lat']
    longitude = df_roads_last.loc[0, 'lon']
    type_of_bridge = 'sink'
    bridge_name = 'sink'
    length = 0
    condition = 'A'
    
    # adding new row
    df.loc[len(df)] = [road_name, km, type_of_bridge, bridge_name, length, 
              condition, latitude, longitude, type_of_bridge]
    # reset index
    df.sort_index(inplace=True) 
    
    # convert dataframe to csv
    df.to_csv(path+"\\data\\bridges_cleaned.csv")

convert_data()