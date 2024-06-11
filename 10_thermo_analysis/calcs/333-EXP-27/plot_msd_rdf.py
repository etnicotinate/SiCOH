import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import find_peaks, savgol_filter

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, pe, temp = read_msd(filename).T
    fig, ax1 = plt.subplots(figsize=(8,6))

    color = 'tab:blue'
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel(r'$MSD (\AA^2)$', color=color)
    ax1.scatter(temp, msd_tt, s=3.0, color=color, label=r'$MSD_{total}$')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Potential Energy (kcal/mol)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(temp, pe, s=3.0, color=color, label='Potential Energy')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('MSD and Potential Energy vs Temperature')
    # plt.legend(loc='upper left')

    pngname = r'msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD and Potential Energy have been plotted to {pngname}')

def plot_msd0(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, pe, temp = read_msd(filename).T
    # plt.scatter(temp, msd_x, s=.5)
    # plt.scatter(temp, msd_y, s=.5)
    # plt.scatter(temp, msd_z, s=.5)
    plt.scatter(temp, msd_tt, s=1.5, label=r'$MSD_{total}$') # total MSD
    plt.scatter(temp, pe, s=1.5) # E_potentials
    plt.xlabel('Temperature (K)')
    plt.ylabel(r'$MSD (\AA^2)$')
    plt.title('MSD and Volumn vs Temperature')
    plt.legend()
    # plt.legend([r'$MSD_x$', r'$MSD_y$', r'$MSD_z$', r'$MSD_{total}$'])
    pngname = r'msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

def calc_mp(filename):
    timesteps, *_, msd_tt, pe, temp = read_msd(filename).T
    # Calculate and smooth derivatives
    msd_derivative = np.abs(np.gradient(msd_tt, temp))
    pe_derivative = np.abs(np.gradient(pe, temp))

    window, poly = 20, 3
    height = 2
    msd_derivative_smooth = savgol_filter(msd_derivative, window, poly)  # window size 11, polynomial order 3
    pe_derivative_smooth = savgol_filter(pe_derivative, window, poly)  # window size 11, polynomial order 3

    # Normalize derivatives
    msd_derivative_norm = (msd_derivative_smooth - np.mean(msd_derivative_smooth)) / np.std(msd_derivative_smooth)
    pe_derivative_norm = (pe_derivative_smooth - np.mean(pe_derivative_smooth)) / np.std(pe_derivative_smooth)

    # Identify local maxima in the smoothed and normalized derivatives
    msd_peaks, _ = find_peaks(msd_derivative_norm, height=height)
    pe_peaks, _ = find_peaks(pe_derivative_norm, height=height)

    # Calculate average transition temperature
    transition_temperatures_msd = temp[msd_peaks]
    transition_temperatures_pe = temp[pe_peaks]
    
    # combined_transition_temperatures = np.concatenate((transition_temperatures_msd, transition_temperatures_pe))
    # average_transition_temperature = np.mean(combined_transition_temperatures)

    combined_transition_temperatures = np.array((transition_temperatures_msd[0], transition_temperatures_pe[0]))
    average_transition_temperature = np.mean(combined_transition_temperatures)

    # # Highlight the transition point
    # ax1.axvline(x=average_transition_temperature, color='green', linestyle='--', linewidth=1.5, label='Transition Point')

    print(f'Transition Temperature (MSD): {transition_temperatures_msd} K')
    print(f'Transition Temperature (Pe): {transition_temperatures_pe} K')
    print(f'Combined Estimated Transition Temperature {average_transition_temperature:.2f} K')

    # Plot smoothed and normalized derivatives
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel(r'Normalized d(MSD)/dT', color=color)
    ax1.plot(temp, msd_derivative_norm, color=color, label=r'Normalized d(MSD$_{total}$)/dT')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Normalized d(Potential Energy)/dT', color=color)
    ax2.plot(temp, pe_derivative_norm, color=color, label='Normalized d(Potential Energy)/dT')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Normalized Derivatives of MSD and Potential Energy vs Temperature')
    fig.legend(loc='upper left')

    pngname = r'dv_msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'Plotted to {pngname}')

def read_rdf(filename):
    # {Timestep: [[r, g_r, coor_r,...], ...]}
    rdf_data = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        current_timestep = None
        current_data = []
        
        for line in lines:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            
            if len(parts) == 2:
                # This line indicates a new timestep
                if current_timestep is not None:
                    # Convert current_data to ndarray and store in rdf_data
                    rdf_data[current_timestep] = np.array(current_data, dtype=float)
                
                current_timestep = int(parts[0])
                current_data = []
            else:
                # This line contains RDF data, romoving the index column
                current_data.append([float(x) for x in parts[1:]])
        
        # the last set of data
        if current_timestep is not None:
            rdf_data[current_timestep] = np.array(current_data, dtype=float)
    
    return rdf_data

def plot_rdf(filename, timestep2=1000):
    rdf_data = read_rdf(filename)
    plt.figure(figsize=(8,6))
    ax = plt.gca()
    # Set major ticks locator for x-axis
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # Set minor ticks locator for x-axis
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    
    # Extract the 1st frame (timestep 0)
    data = rdf_data[0]

    labels = ['C-C', 'C-Si','Si-O', 'C-H']
    colors = ['blue', 'orange', 'green', 'red']

    r = data[:, 0]  # distance, r
    for i, (label, color) in enumerate(zip(labels, colors)):
        g_r = data[:, 2*i+1]  # g(r)
        coor_r = data[:, 2*i+2]  # coor(r)
        
        plt.plot(r, g_r, label=label, color=color)
    legend1=plt.legend(loc='upper left', title='Before')
    ax.add_artist(legend1)

    # plot the middle frame (timestep 1000)
    data = rdf_data[timestep2]
    for i, (label, color) in enumerate(zip(labels, colors)):
        g_r = data[:, 2*i+1]  # g(r)
        coor_r = data[:, 2*i+2]  # coor(r)
        
        plt.plot(r, g_r, label=label, color=color, linestyle='--')
    
    # Add a legend2 
    handles, labels = ax.get_legend_handles_labels()
    handles_middle = handles[len(labels)//2:]
    labels_middle = labels[len(labels)//2:]
    plt.legend(handles=handles_middle, labels=labels_middle, loc='upper right', title='After')
    
    plt.xlabel(r'Distance, $r (\AA)$')
    plt.ylabel('g(r)')
    # plt.title(f'RDF for timestep {timestep}')

    pngname = r'rdf.png'
    plt.savefig(pngname, dpi=300)
    print(f'RDF has been plotted to {pngname}')


if __name__ == '__main__':
    msd_filename = r'msd.out'
    rdf_filename = r'rdf.out'
    calc_mp(msd_filename)

    plot_msd(msd_filename)
    plot_rdf(rdf_filename)

    # calc_mp0(msd_filename)
    # plot_msd_with_derivatives(msd_filename)