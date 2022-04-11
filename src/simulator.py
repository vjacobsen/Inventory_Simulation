import pandas as pd
import numpy as np
from collections import defaultdict



def sample_demand():
    # This can be any sampling function, as long as it returns a float
    return round(np.random.normal(40,5), 0)


class BaseInventorySystem():
    def __init__(self, starting_value=150, order_lead_time=3,starting_period=0, reorder_point=100, order_up_to=200) -> None:
        self.inventory = starting_value
        self.period = starting_period
        self.reorder_point = reorder_point
        self.order_up_to = order_up_to
        self.order_lead_time = order_lead_time
        self.log = {}
        self.order_log_dict = defaultdict(lambda: 0) # Format: 'delivery_period':'qty_to_be_delivered'


    def replenish(self, quantity):
        # We have a replenish method that can be easily used to add loss
        # Ex: inventory += quantity * 0.95
        self.inventory += quantity
        

    def fulfill_demand(self, demand):
        # Inventory post-demand
        new_inventory = self.inventory - demand        
        self.unmet_demand = min(new_inventory,0)
        
        # Check if we have enough invntory to fulfill demand
        if new_inventory > 0: 
            # Net change is positive then we subtract demand from inventory
            self.inventory = new_inventory
        else:
            # Net change is negative, meaning we have lost sales
            self.inventory = 0

        # Log metrics
        self.log[self.period]['unmet_demand'] = abs(self.unmet_demand)
        self.log[self.period]['demand'] = demand


    def place_order(self):
        # Orders to be delivered in future periods
        in_transit_qty = sum([v for k,v in self.order_log_dict.items() if k > self.period])

        # If total inventory < reorder point
        if self.inventory  + in_transit_qty <= self.reorder_point:
            order_quantity = self.order_up_to - self.inventory - in_transit_qty
            lead_time = self.order_lead_time  # lead time could be a sampling function, add support for this in future
            # Register order to be delivered in future period
            self.order_log_dict[self.period + lead_time] += order_quantity
            self.log[self.period]['ordered'] = order_quantity
        else:
            self.log[self.period]['ordered'] = 0
                    

    def deliver_orders(self):
        deliver_qty = self.order_log_dict[self.period]
        self.replenish(deliver_qty)
        self.log[self.period]['delivered'] += deliver_qty
                

    def start_period(self):
        # Set up logging dict
        self.log[self.period] = {
            'ordered':0, 
            'delivered':0, 
            'boh_start':self.inventory,
            'boh_end':0
            }

    
    def new_period(self):
        # Register balance on hand at period end, prior to starting new period.
        self.log[self.period]['boh_end'] = self.inventory
        self.period += 1
        self.unmet_demand = 0


    def run(self, demand_sampler=sample_demand, periods=100):
        # Orchestrator for simulating inventory periods
        for _ in range(0, periods):
            self.start_period()
            self.deliver_orders()
            self.fulfill_demand(demand_sampler())
            self.place_order()
            self.new_period()

        self.log_df = pd.DataFrame.from_dict(self.log, orient='index')

        return self.log_df


    def get_summary(self):
        service_level = round(1 - self.log_df['unmet_demand'].sum() / self.log_df['demand'].sum(),4)
        oos_periods = sum(self.log_df['boh_start'] == 0)
        summary_df = pd.DataFrame({'service_level':[service_level], 'oos_periods':[oos_periods]})
        
        return summary_df
                

class BatchSimulator():
    # Simulate inventory 
    def __init__(self):
        pass
    
    def replicate(self, system, iterations):
        # Replicate runs for a number of iterations
        pass
        

def execute_run(inv_system_args, sampler, run_periods):
    '''
    Executes single inventory simulation run with specified parameters.

    Returns:
        object: simulation with results executed.
    '''
    simulation = BaseInventorySystem(**inv_system_args)
    simulation.run(demand_sampler=sampler, periods=run_periods)

    return simulation