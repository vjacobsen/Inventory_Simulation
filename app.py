import invsim.simulator as sim
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------------------------------
# SIDEBAR: define run parameters
# ----------------------------------------------------

demand_dict = sim.load_demand_dict()

with st.sidebar:  
    st.subheader('Replenishment parameters:')  
    RUN_PERIODS = st.slider('How many days to simulate?', 1, 400, 100)
    STARTING_INVENTORY = st.number_input('Starting Inventory', min_value=1, value=25)
    ORDER_UP_TO = st.number_input('Order Up to Level',min_value=1,value=50)
    REORDER_POINT = st.number_input('Reorder Point', min_value=10, value=20)
    
    if REORDER_POINT > ORDER_UP_TO:
        st.error('Reorder point must be less than order up to level.')

    # Order lead time can also be a function for sampling distribution
    ORDER_LEAD_TIME = st.number_input('Order lead time', min_value=1, value=3) 

    # DEMAND PICKER
    st.subheader('Demand generation parameters:')
    DEMAND_DIST = st.selectbox("Distribution", options=demand_dict.keys())
    demand_dist_func, kwargs, kwarg_names, defaults = demand_dict[DEMAND_DIST]    
    dist_args = {
        kwarg:st.number_input(name, value=dft) 
        for kwarg,name,dft in zip(kwargs, kwarg_names, defaults)
        }
    # Demand sampler function
    demand_sampler = lambda: int(round(demand_dist_func(**dist_args),0))
    st.info('Demand sample will be rounded to nearest integer if continuous distribution is used.')
    
        
# TODO - add demand distribution configuration options
# ----------------------------------------------------
# EXECUTION: run simulation with selected params
# ----------------------------------------------------
inv_system_args = {
    "starting_value": STARTING_INVENTORY,
    'order_up_to':ORDER_UP_TO,
    'reorder_point': REORDER_POINT,
    'order_lead_time': ORDER_LEAD_TIME
}

run = sim.execute_run(inv_system_args, demand_sampler, RUN_PERIODS)
run_log = run.log_df
run_summary = run.get_summary()
 
# ----------------------------------------------------
# CREATE CHARTS
# ----------------------------------------------------
fig_inv_over_time = px.line(run_log, y='boh_start', title='Inventory over time')
fig_demand_hist = px.histogram(run_log, x='demand', width=400, height=400, title='Demand Distribution')



# ----------------------------------------------------
# APP MAIN PAGE
# ----------------------------------------------------
st.title('Inventory Simulation App')
st.write('A very simple simulation. This is a continuous review inventory system, which means orders can be placed on any day.')

# METRIC SUMMARY
st.subheader('Run Summary')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Service Level', run_summary['service_level'])
col2.metric('Out of Stock Days', run_summary['oos_periods'])
col3.metric('Average Demand', round(run_log['demand'].mean(),2))
col4.metric('Average Inventory', int(run_log['boh_start'].mean()))

# CHARTS
st.plotly_chart(fig_inv_over_time,use_container_width=True)
st.plotly_chart(fig_demand_hist,use_container_width=True)
avg_demand = round(run_log['demand'].mean(),2)
std_demand = round(run_log['demand'].std(),2)
st.write(f'Average demand: {avg_demand}' )
st.write(f'Standard deviation of demand: {std_demand}' )

# RUN DETAILS
st.subheader('Run Details')
st.dataframe(data=run_log.astype(int), width=None, height=400)
st.write('boh: balance on hand at start/end of day')