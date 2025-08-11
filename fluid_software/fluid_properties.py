from fluid_properties import FluidProperties

# Example CSV data(for reference, not part of the code)
# fluid,temperature,density,viscosity
# Water,25,997,0.89
# Water,50,988,0.55

# Load fluid properties from a CSV file
fp = FluidProperties(data_source='fluids.csv')

# List available fluids
print("Available fluids:", fp.list_fluids())

# Get properties for Water at 25°C
props = fp.get_properties('Water', temperature=25)
print("Water at 25°C:", props)
