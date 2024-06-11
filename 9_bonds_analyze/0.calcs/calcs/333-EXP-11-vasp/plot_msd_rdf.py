import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, temp = read_msd(filename).T
    plt.scatter(timesteps, msd_x, s=.5)
    plt.scatter(timesteps, msd_y, s=.5)
    plt.scatter(timesteps, msd_z, s=.5)
    plt.scatter(timesteps, msd_tt, s=1.5) # total MSD
    plt.xlabel('Timesteps')
    plt.ylabel('MSD')
    plt.title('Mean Squared Displacement')
    plt.legend([r'$MSD_X$', r'$MSD_Y$', r'$MSD_Z$', r'$MSD_{Total}$'])
    pngname = r'msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

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
    plot_msd(msd_filename)
    plot_rdf(rdf_filename)