import pandas as pd
from src import simulator as sim
import numpy as np


def execute_run(inv_system_args, run_periods):
    '''
    Executes single inventory simulation run with specified parameters.
    '''
    
    SIM = sim.InventorySimulation(
        system=sim.BaseInventorySystem(**inv_system_args), 
        demand_sampler=sim.sample_demand
    )

    SIM.run(run_periods)
    
    return SIM


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
    run = execute_run(inv_system_args, 100)
    run.get_log_df().head()
    print()
    run.get_summary()
    