import pandas as pd
from src import simulator as sim
import numpy as np

sim.sample_demand()

def execute_run(inv_system_args, sampler, run_periods):
    '''
    Executes single inventory simulation run with specified parameters.
    '''
    
    simulation = sim.BaseInventorySystem(**inv_system_args)

    simulation.run(demand_sampler=sampler, periods=run_periods)
    
    return simulation


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
    run = execute_run(inv_system_args, sim.sample_demand, 100)
    run.log_df.head()
    print()
    run.get_summary()
    
