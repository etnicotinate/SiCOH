import numpy as np
import glob

# Read volume data from files
Temp = []
Vol = []

for file in sorted(glob.glob(r"vol-T_*.out")):
    data = np.loadtxt(file)

    volume = data[1] 
    temperature = data[2]
    
    Vol.append(volume)
    Temp.append(temperature)
    
# Perform a linear fit to volume vs temperature
Vol = np.array(Vol)*1e-30  # AA^3 to m^3
Temp = np.array(Temp)
coeffs = np.polyfit(Temp, Vol, 1)
# the slope (dV/dT)
dV_dT = coeffs[0]

# Calculate the CTE
CTE = dV_dT / Vol[0] * 1e6  # 10^-6 K^-1
print(f"CTE: {CTE:.2f} (10^-6 K^-1)")
