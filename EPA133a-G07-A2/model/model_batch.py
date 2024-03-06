import pandas as pd
import random
from model import BangladeshModel
from mesa import batch_run

"""
    Run simulation
    Perform batchrunner
"""

# ---------------------------------------------------------------

params = {"collapse_dict": [{'A': 0, 'B': 0, 'C': 0, 'D': 0.05},
                            {'A': 0, 'B': 0, 'C': 0, 'D': 0.10},
                            {'A': 0, 'B': 0, 'C': 0.05, 'D': 0.10},
                            {'A': 0, 'B': 0, 'C': 0.10, 'D': 0.20},
                            {'A': 0, 'B': 0.05, 'C': 0.10, 'D': 0.20},
                            {'A': 0, 'B': 0.10, 'C': 0.20, 'D': 0.40},
                            {'A': 0.05, 'B': 0.10, 'C': 0.20, 'D': 0.40},
                            {'A': 0.10, 'B': 0.20, 'C': 0.40, 'D': 0.80}]}

results = batch_run(
    BangladeshModel,
    parameters=params,
    iterations=10,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True)

df_results = pd.DataFrame(results)
print(df_results)