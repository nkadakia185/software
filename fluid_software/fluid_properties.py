import pandas as pd

# Function to load fluid properties from CSV and create variables dynamically
# Assume we have a "fluid_properties.csv" with columns: fluid_type, temperature, pressure, mass_flow_rate, target_velocity
def fluid_properties(csv_path):
    df = pd.read_csv(csv_path)
    fluid_vars = {}
    for _, row in df.iterrows():
        fluid_type = row['fluid_type'].lower()
        fluid_vars[f"{fluid_type}_temperature"] = row['temperature']
        fluid_vars[f"{fluid_type}_pressure"] = row['pressure']
        fluid_vars[f"{fluid_type}_mfr"] = row['mass_flow_rate']
        fluid_vars[f"{fluid_type}_target_velocity"] = row['target_velocity']
    return fluid_vars
fluid_properties('fluid_properties.csv')
fluid_vars
# Example usage:
# fluid_vars = load_fluid_properties('fluid_properties.csv')
# water_temperature = fluid_vars['water_temperature']
# water_pressure = fluid_vars['water_pressure']
# water_mfr = fluid_vars['water_mfr']
# water_target_velocity = fluid_vars['water_target_velocity']