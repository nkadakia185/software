import pandas as pd
import pandas as pd

def filter_pipe_by_section_viii(pipe_df, material_props_df, material, design_temp, design_pressure, seamless=True, section_viii=True):
    """
    Filters pipe sizes based on ASME Section VIII UG-27 required thickness.

    Parameters:
    - pipe_df: DataFrame with 'inside_diameter' and 'wall_thickness' columns
    - material_props_df: DataFrame with stress values for materials by temperature
                         Must contain 'material' column and temperature columns as floats
    - material: str, material name to look up in material_props_df
    - design_temp: float, temperature (°F or °C depending on table)
    - design_pressure: float, internal design pressure (same units as stress)
    - seamless: bool, True if pipe is seamless (E = 1.0), else E = 0.85
    - section_viii: bool, if True, apply UG-27 filtering

    Returns:
    - DataFrame with only rows where wall_thickness > required t
    """
    
    if not section_viii:
        return pipe_df  # Placeholder for future piping code filters

    # Set joint efficiency E
    E = 1.0 if seamless else 0.85
    
    # Find closest temperature in the material properties
    temp_cols = [col for col in material_props_df.columns if isinstance(col, (int, float))]
    closest_temp = min(temp_cols, key=lambda t: abs(t - design_temp))

    # Get S (maximum allowable stress)
    try:
        S = material_props_df.loc[material_props_df['material'] == material, closest_temp].values[0]
    except IndexError:
        raise ValueError(f"Material '{material}' not found in material properties table.")

    # Apply UG-27 thickness formula: t = (P * R) / (SE - 0.6P)
    def calc_required_t(row):
        R = row['inside_diameter'] / 2
        denominator = (S * E - 0.6 * design_pressure)
        return (design_pressure * R) / denominator if denominator > 0 else float('inf')

    pipe_df = pipe_df.copy()
    pipe_df['required_thickness'] = pipe_df.apply(calc_required_t, axis=1)
    pipe_df['meets_UG27'] = pipe_df['wall_thickness'] > pipe_df['required_thickness']

    # Return only valid rows
    return pipe_df[pipe_df['meets_UG27']].drop(columns=['required_thickness', 'meets_UG27'])
