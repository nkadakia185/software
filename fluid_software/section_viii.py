import pandas as pd

def filter_pipe_by_section_viii(
    pipe_df: pd.DataFrame,
    material_props_df: pd.DataFrame,
    material: str,
    design_temp: float,
    design_pressure: float,
    seamless: bool = True,
    section_viii: bool = True
) -> pd.DataFrame:
    """
    Filters pipe sizes based on ASME Section VIII UG-27 required thickness.

    Parameters:
    - pipe_df: DataFrame with 'inside_diameter' and 'wall_thickness' columns
    - material_props_df: DataFrame with stress values for materials by temperature.
                         Must include a 'material' column and numeric temperature columns
    - material: Material name to look up in material_props_df
    - design_temp: Design temperature (same unit as temperature columns)
    - design_pressure: Internal design pressure
    - seamless: If True, assumes seamless pipe (E = 1.0), else E = 0.85
    - section_viii: If True, applies UG-27 filtering

    Returns:
    - Filtered DataFrame with only rows where wall_thickness > required thickness
    """

    if not section_viii:
        return pipe_df  # Skip filtering if Section VIII is not applied

    # Set weld joint efficiency factor E
    E = 1.0 if seamless else 0.85

    # Get numeric temperature columns
    try:
        temp_cols = [float(col) for col in material_props_df.columns if isinstance(col, (int, float, float))]
    except Exception as e:
        raise ValueError("Temperature columns must be numeric.") from e

    # Find the closest temperature available in material_props_df
    if not temp_cols:
        raise ValueError("No numeric temperature columns found in material properties DataFrame.")

    closest_temp = min(temp_cols, key=lambda t: abs(t - design_temp))

    # Get maximum allowable stress S
    try:
        S = material_props_df.loc[material_props_df['material'] == material, str(closest_temp)].values[0]
    except IndexError:
        raise ValueError(f"Material '{material}' not found in material properties.")
    except KeyError:
        raise ValueError(f"Temperature column '{closest_temp}' not found in material properties.")

    # Calculate required thickness using UG-27: t = (P * R) / (SE - 0.6P)
    def calc_required_t(row):
        R = row['inside_diameter'] / 2
        denominator = (S * E - 0.6 * design_pressure)
        return (design_pressure * R) / denominator if denominator > 0 else float('inf')

    # Apply calculation and filter
    pipe_df = pipe_df.copy()
    pipe_df['required_thickness'] = pipe_df.apply(calc_required_t, axis=1)
    pipe_df['meets_UG27'] = pipe_df['wall_thickness'] > pipe_df['required_thickness']

    return pipe_df[pipe_df['meets_UG27']].drop(columns=['required_thickness', 'meets_UG27'])
