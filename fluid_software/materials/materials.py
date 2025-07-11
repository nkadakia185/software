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
 