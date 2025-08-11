#TODO: Read materials_properties.csv file to get the material properties
#TODO  Make function to interpolate between temperature values for allowable stress and return allowable stress
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "material_properties.csv")

# Load data from CSV
def load_material_data(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    return df

# Interpolate allowable stress for a given material and temperature
def interpolate_allowable_stress(material, temperature, csv_path=CSV_PATH):
    df = load_material_data(csv_path)
    material = str(material).strip()
    temperatures = df["Temperature"]
    try:
        material_stresses = df[material]
    except KeyError:
        raise ValueError(f"Material '{material}' not found in material properties.")
    allowable_stress = np.interp(temperature, temperatures, material_stresses)
    return allowable_stress
