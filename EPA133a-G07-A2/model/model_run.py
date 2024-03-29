from model import BangladeshModel
import random

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

# run time 1000 ticks
# run_length = 1000

seed = random.seed()

sim_model = BangladeshModel(seed=seed)

# Check if the seed is set
print("SEED " + str(sim_model._seed))

# One run with given steps
for i in range(run_length):
    sim_model.step()

model_data = sim_model.datacollector.get_model_vars_dataframe()
# agent_data = sim_model.datacollector.get_agent_vars_dataframe()

# model_data.to_csv("../data/model_data.csv")
# agent_data.to_csv("../data/agent_data.csv")
