import pandas as pd
from invsim import simulator as sim
import numpy as np

def test_simulation():
    # Test run with parameters
    inv_system_args = {
    "starting_value": 200,
    'order_up_to':400,
    'reorder_point': 100,
    'order_lead_time': 3
    }  

    # Run test
    run = sim.execute_run(inv_system_args, sim.sample_demand, 100)
    print(run.log_df.head())
    print()
    print(run.get_summary())

    sl = run.get_summary()['service_level'].values[0]
    
    assert isinstance(sl, float)


if __name__ == "__main__":
    test_simulation()



    
