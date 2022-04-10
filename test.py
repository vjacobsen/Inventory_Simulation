import pandas as pd
from src import simulator as sim
import numpy as np


if __name__ == "__main__":
    # Test run with parameters
    inv_system_args = {
    "starting_value": 200,
    'order_up_to':400,
    'reorder_point': 100,
    'order_lead_time': 3
    }  

    print('------------------------------------------')
    print('TEST RUN RESULTS')
    print('------------------------------------------')

    # Run test
    run = sim.execute_run(inv_system_args, sim.sample_demand, 100)
    run.log_df.head()
    print()
    run.get_summary()
    
