import numpy as np
import matplotlib.pyplot as plt

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, temp = read_msd(filename).T
    plt.scatter(timesteps, msd_x, s=.5)
    plt.scatter(timesteps, msd_y, s=.5)
    plt.scatter(timesteps, msd_z, s=.5)
    plt.scatter(timesteps, msd_tt, s=1.5) # total MSD
    plt.xlabel('Temperature (K)')
    plt.ylabel(r'$MSD(\AA^2)$')
    plt.title('Mean Squared Displacement')
    plt.legend([r'$MSD_x$', r'$MSD_y$', r'$MSD_z$', r'$MSD_{total}$'])
    pngname = r'msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

def calc_mp(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, temp = read_msd(filename).T
    # derivative of MSD 
    msd_derivative = np.gradient(msd_tt, temp)

    # # Plot the derivative to find sharp changes
    # plt.figure()
    # plt.plot(temperatures, msd_derivative, 'b-', label=r'd(MSD$_{total}$)/dT')
    # plt.xlabel('Temperature (K)')
    # plt.ylabel(r'd(MSD)/dT')
    # plt.legend()
    # plt.title('Derivative of MSD with respect to Temperature')

    # plt.show()

    # Identify the melting point
    # where a sharp increase
    melting_point_index = np.argmax(np.abs(msd_derivative))
    melting_point_temp = temp[melting_point_index]

    print(f'Estimated Melting Point: {melting_point_temp:.2f} K')

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
    
    # Extract the 1st frame
    timestep, data = next(iter(rdf_data.items()))
    labels = ['Si-O', 'Si-Si', 'O-O']
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
    calc_mp(msd_filename)
    plot_rdf(rdf_filename)