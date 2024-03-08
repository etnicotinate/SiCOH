# Import
import numpy as np
# import pandas as pd
from matplotlib import pyplot as plt

# Read file
filename = r"stress-strain-avg.log"
data = np.genfromtxt(filename, comments='#', delimiter=None)
data = np.array(data, np.float64)
# data
x, y = data[::5,1], data[::5,2]

# Set draw
plt.figure(figsize=(8,5))
plt.plot(x,y, linewidth=1.5,marker='o',markersize=3)
plt.xlabel('Strain ')
plt.ylabel('Stress (GPa)')
plt.title('Stress-strain curve',x=0.5,y=1.02)
plt.savefig(f'{filename.removesuffix("log")}png',dpi=300,bbox_inches='tight')
print(f'Saved to {filename.removesuffix("log")}png')
# plt.show()

# Select the linear part
max_index = np.argmax(y)
x, y = x[:max_index], y[:max_index]

# Calculate Young's modulus
from scipy import stats as st

slope, intercept, r_value, p_value, std_err = st.linregress(x, y)
Youngs = slope
print(f"Young's modulus: {Youngs:.4f} Gpa")