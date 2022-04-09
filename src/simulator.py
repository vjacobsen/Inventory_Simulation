from re import L
import pandas as pd
from collections import defaultdict
import numpy as np

class BaseInventorySystem():
    def __init__(self, starting_value=150, order_lead_time=3,starting_period=0, reorder_point=100, order_up_to=200) -> None:
        self.inventory = starting_value
        self.period = starting_period
        self.reorder_point = reorder_point
        self.order_up_to = order_up_to
        self.order_lead_time = order_lead_time
        self.log = {}
        self.order_log = []


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
        if self.inventory <= self.reorder_point:
            ## TODO - add current on order amount to calculation.
            order_quantity = self.order_up_to - self.inventory
            new_order = Order(self.order_lead_time, order_quantity, self.period)
            self.order_log.append(new_order)
            self.log[self.period]['ordered'] = order_quantity
        else:
            self.log[self.period]['ordered'] = 0
                    

    def deliver_orders(self):
        if len(self.order_log) > 0:
            # If we have orders, we'll go through each one and check to see if they deliver during the current period
            for order in self.order_log:
                if order.delivery_period == self.period:
                    self.replenish(order.quantity)
                    order.update_status()
                    self.log[self.period]['delivered'] += order.quantity
                    

    def start_period(self):
        # Set up logging dict
        self.log[self.period] = {
            'ordered':0, 
            'delivered':0, 
            'boh_start':self.inventory,
            'boh_end':0
            }

    
    def new_period(self):
        self.unmet_demand = 0
        self.log[self.period]['boh_end'] = self.inventory
        self.period += 1


class Order():
    def __init__(self, lead_time, quantity, created_period):
        self.lead_time = lead_time
        self.quantity = quantity
        self.created_period = created_period
        self.delivery_period = self.created_period +  self.lead_time
        self.status = 'IN TRANSIT'

    def update_status(self):
        self.status='DELIVERED'
                

def sample_demand():
    # This can be any sampling function, as long as it returns a float
    return round(np.random.normal(40,5), 0)


class InventorySimulation():
    # Orchestrator class to simulate an inventory system
    def __init__(self, system=BaseInventorySystem(), demand_sampler=sample_demand()):
        self.system = system # the inventory object to be simulated
        self.demand_sampler = demand_sampler # a demand sampler function


    def run(self, periods=100):
        # Simulate periods
        for _ in range(0, periods):
            self.system.start_period()
            self.system.deliver_orders()
            self.system.fulfill_demand(self.demand_sampler())
            self.system.place_order()
            self.system.new_period()

        # Create log DataFrame
        self.log_df = pd.DataFrame.from_dict(self.system.log, orient='index')


    def get_log_df(self):
        return self.log_df


    def get_summary(self):
        service_level = round(1 - self.log_df['unmet_demand'].sum() / self.log_df['demand'].sum(),4)
        oos_periods = sum(self.log_df['boh_start'] == 0)
        output = pd.DataFrame({'service_level':[service_level], 'oos_periods':[oos_periods]})
        
        return output