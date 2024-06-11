import numpy as np
import matplotlib.pyplot as plt

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, pe, temp = read_msd(filename).T
    
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel(r'$MSD (\AA^2)$', color=color)
    ax1.scatter(temp, msd_tt, s=1.5, color=color, label=r'$MSD_{total}$')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Potential Energy (kcal/mol)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(temp, pe, s=1.5, color=color, label='Potential Energy')
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
    # derivative of MSD 
    msd_derivative = np.gradient(msd_tt, temp)
    pe_derivative = np.gradient(msd_tt, temp)

    # Identify significant changes
    msd_threshold = np.mean(msd_derivative) + 2.5 * np.std(msd_derivative)
    pe_threshold = np.mean(pe_derivative) + 3 * np.std(pe_derivative)
    
    significant_msd_changes = np.where(np.abs(msd_derivative) > msd_threshold)[0]
    significant_pe_changes = np.where(np.abs(pe_derivative) > pe_threshold)[0]

    # Identify the melting point
    # where a sharp increase
    melting_point_temp1 = temp[significant_msd_changes[0]]
    print(f'Estimated Melting Point(MSD-T): {melting_point_temp1:.2f} K')

    melting_point_temp2 = temp[significant_pe_changes[0]]
    print(f'Estimated Melting Point(Pe-T): {melting_point_temp2:.2f} K')

    # Combine criteria to estimate melting point or Tg
    if len(significant_msd_changes) > 0 and len(significant_pe_changes) > 0:
        transition_indices = np.intersect1d(significant_msd_changes, significant_pe_changes)
        if len(transition_indices) > 0:
            transition_index = transition_indices[0]
            transition_temperature = temp[transition_index]
    print(f'Estimated Melting Point: {transition_temperature:.2f} K')

def calc_mp0(filename):
    timesteps, *_, msd_tt, pe, temp = read_msd(filename).T
    # derivative of MSD 
    msd_derivative = np.gradient(msd_tt, temp)

    
    # Identify the melting point
    # where a sharp increase
    melting_point_index1 = np.argmax(np.abs(msd_derivative))
    melting_point_temp1 = temp[melting_point_index1]
    print(f'Estimated Melting Point(MSD-T): {melting_point_temp1:.2f} K')

    pe_derivative = np.gradient(pe, temp)
    # Identify the melting point
    # where a sharp increase
    melting_point_index2 = np.argmax(np.abs(pe_derivative))
    melting_point_temp2 = temp[melting_point_index2]
    print(f'Estimated Melting Point(Pe-T): {melting_point_temp2:.2f} K')

    # # Plot the derivative to find sharp changes
    # plt.figure()
    # plt.plot(temperatures, msd_derivative, 'b-', label=r'd(MSD$_{total}$)/dT')
    # plt.xlabel('Temperature (K)')
    # plt.ylabel(r'd(MSD)/dT')
    # plt.legend()
    # plt.title('Derivative of MSD with respect to Temperature')

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

def plot_rdf(filename):
    rdf_data = read_rdf(filename)
    plt.figure(figsize=(8,6))
    
    # Extract the 1st frame (timestep 0)
    it_rdf = iter(rdf_data.items())
    # Extract the average 1-1000 frame (timestep 0-1000)
    # next(it_rdf)
    timestep, data = next(it_rdf)
    
    labels = ['C-C', 'C-Si','Si-O']
    # labels = ['C-C', 'C-Si','Si-O', 'C-H', 'Si-Si']
    r = data[:, 0]  # distance, r

    for i, label in enumerate(labels):
        g_r = data[:, 2*i+1]  # g(r)
        coor_r = data[:, 2*i+2]  # coor(r)
        
        plt.plot(r, g_r, label=f'{label}')
        # plt.plot(r, coor_r, label=f'coor(r)')
        
    plt.xlabel('r')
    plt.ylabel('g(r)')
    plt.title(f'RDF for timestep {timestep}')
    plt.legend()
    pngname = 'rdf.png'
    plt.savefig(pngname, dpi=300)
    print(f'RDF has been plotted to {pngname}')

def plot_rdf0(filename):
    '''
    Plot radial distribution function for initial and final frames
    '''
    data = read_rdf(filename)[100]
    
    r, g, coor = data[:,1], data[:,2], data[:,3]
    print(r)
    print(g)
    plt.plot(r, g)
    plt.plot(r, coor)
    plt.xlabel(r'$r (\AA)$')
    plt.ylabel('g(r)')
    plt.title('Radial Distribution Function')
    plt.legend([f'g(r) for {filename}'])
    pngname = 'rdf.png'
    plt.savefig(pngname, dpi=300)
    print(f'RDF has been plotted to {pngname}')

    return


if __name__ == '__main__':
    msd_filename = r'msd.out'
    rdf_filename = r'rdf.out'
    plot_msd(msd_filename)
    calc_mp0(msd_filename)
    plot_rdf(rdf_filename)