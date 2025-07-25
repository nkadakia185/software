def select_material(temperature, pressure):
    """
    Selects a material based on input temperature (°C) and pressure (bar).
    Returns the name of the material as a string.
    """
    if temperature < 200 and pressure < 20:
        return "Stainless Steel"
    elif temperature < 500 and pressure < 50:
        return "Inconel"
    else:
        return "Special Alloy"

def asme_allowable_stress(material, temperature):
    """
    Returns the allowable stress (MPa) for a given material and temperature (°C)
    using simplified ASME equations.
    """
    asme_data = {
        "Stainless Steel": lambda T: 140 - 0.1 * T,
        "Inconel": lambda T: 200 - 0.15 * T,
        "Special Alloy": lambda T: 250 - 0.2 * T
    }
    if material in asme_data:
        allowable = asme_data[material](temperature)
        return max(allowable, 0)  
    else:
        return None

if __name__ == "__main__":
    try:
        temp = float(input("Enter temperature (°C): "))
        pres = float(input("Enter pressure (bar): "))
        material = select_material(temp, pres)
        print(f"Selected material: {material}")
        allowable_stress = asme_allowable_stress(material, temp)
        if allowable_stress is not None:
            print(f"ASME allowable stress for {material} at {temp}°C: {allowable_stress:.2f} MPa")
        else:
            print("ASME allowable stress data not available for this material.")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
class Material:
    def __init__(self, name, allowable_stress_func):
        self.name = name
        self.allowable_stress_func = allowable_stress_func

    def allowable_stress(self, temperature):
        allowable = self.allowable_stress_func(temperature)
        return max(allowable, 0)
stainless_steel = Material("Stainless Steel", lambda T: 140 - 0.1 * T)
inconel = Material("Inconel", lambda T: 200 - 0.15 * T)
special_alloy = Material("Special Alloy", lambda T: 250 - 0.2 * T)

corrosion_allowances = {
    "Stainless Steel": 1.5,
    "Inconel": 1.0,
    "Special Alloy": 2.0
}


temperature_derating = {
    "Stainless Steel": lambda T: 1.0 if T < 100 else 0.95 if T < 300 else 0.9,
    "Inconel": lambda T: 1.0 if T < 200 else 0.92 if T < 400 else 0.85,
    "Special Alloy": lambda T: 1.0 if T < 250 else 0.93 if T < 500 else 0.88
}

def get_corrosion_allowance(material):
    """Returns the corrosion allowance (mm) for the given material."""
    return corrosion_allowances.get(material, 0)

def get_derated_allowable_stress(material, temperature):
    """Returns the allowable stress after temperature derating for the given material and temperature."""
    base_stress = asme_allowable_stress(material, temperature)
    if base_stress is None:
        return None
    derating_factor = temperature_derating.get(material, lambda T: 1.0)(temperature)
    return max(base_stress * derating_factor, 0)