import pandas as pd
from model import BangladeshModel
from mesa import batch_run

params = {collaps_dict = [{'A': 0, 'B': 0, 'C': 0, 'D': 5},
                          {'A': 0, 'B': 0, 'C': 0, 'D': 10},
                          {'A': 0, 'B': 0, 'C': 5, 'D': 10},
                          {'A': 0, 'B': 0, 'C': 10, 'D': 20},
                          {'A': 0, 'B': 5, 'C': 10, 'D': 20},
                          {'A': 0, 'B': 10, 'C': 20, 'D': 40},
                          {'A': 5, 'B': 10, 'C': 20, 'D': 40},
                          {'A': 10, 'B': 20, 'C': 40, 'D': 80}]}

results = batch_run(
    BangladeshModel,
    parameters=params,
    iterations=10,
    max_steps=10000,
    number_processes=1,
    data_collection_period=1,
    display_progress=True)

df_results = pd.DataFrame(results)
