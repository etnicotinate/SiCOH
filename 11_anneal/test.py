import numpy as np
import matplotlib.pyplot as plt

# Load your actual data
# For demonstration purposes, I'll create synthetic data
# Replace these with your actual data
temperatures = np.linspace(300, 1500, num=100)  # Example temperature data
msd_total = np.random.rand(100) * temperatures / 100  # Example MSD data

# Calculate the derivative of MSD with respect to Temperature
msd_derivative = np.gradient(msd_total, temperatures)

# Plot MSD_total vs Temperature
plt.figure()
plt.plot(temperatures, msd_total, 'r.', label=r'MSD$_{total}$')
plt.xlabel('Temperature (K)')
plt.ylabel('MSD')
plt.legend()
plt.title('Mean Squared Displacement')

# Plot the derivative to find sharp changes
# plt.figure()
plt.plot(temperatures, msd_derivative, 'b-', label=r'd(MSD$_{total}$)/dT')
plt.xlabel('Temperature (K)')
plt.ylabel(r'd(MSD)/dT')
plt.legend()
plt.title('Derivative of MSD with respect to Temperature')

pngname = r'111test.png'
plt.savefig(pngname, dpi=300)
print(f'MSD has been plotted to {pngname}')

# Find significant changes in the derivative
significant_changes = np.where(msd_derivative > 1.0)[0]  # Adjust threshold as necessary

# Filter out the first significant change
if len(significant_changes) > 0:
    melting_point_index = significant_changes[0]
    melting_point_temperature = temperatures[melting_point_index]
else:
    melting_point_temperature = None

if melting_point_temperature is not None:
    print(f'Estimated Melting Point: {melting_point_temperature:.2f} K')
else:
    print('No significant melting point detected.')


