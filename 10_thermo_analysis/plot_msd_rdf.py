import numpy as np
import matplotlib.pyplot as plt

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    t, msd_x, msd_y, msd_z, msd_tt = read_msd(filename).T
    plt.plot(t, msd_x)
    plt.plot(t, msd_y)
    plt.plot(t, msd_z)
    plt.plot(t, msd_tt) # total MSD
    plt.xlabel('Timesteps (0.5 fs)')
    plt.ylabel('MSD')
    plt.title('Mean Squared Displacement')
    plt.legend([r'$MSD_x$', r'$MSD_y$', r'$MSD_z$', r'$MSD_{total}$'])
    pngname = filename.removesuffix('.out') + '.png'
    # plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

def read_rdf(filename):
    with open(filename, 'r') as file:
        for line in file:
            if "Timestep" in line:
                # If not the first timestep, save the current timestep data
                if timestep is not None:
                    data = np.array(data_list)

                    # Reset the data list
                    data_list = []
                # Update the current timestep
                timestep = int(line.split()[-1])
            # no 'Timestep' in line, no '#'
            elif line.strip() and not line.startswith("#"):
                # Process data lines
                data_parts = line.split()
                data_list.append(data_parts)
                # data_list.append([int(part) for part in data_parts])
    

def plot_rdf(filename):
    '''
    Plot radial distribution function for initial and final frames
    '''
    data = read_rdf(filename)
    
    r, rdf = data[0].T
    plt.plot(r, rdf)
    plt.xlabel(r'$r (\AA)$')
    plt.ylabel('g(r)')
    plt.title('Radial Distribution Function')
    plt.legend([f'g(r) for {filename}'])
    pngname = filename.removesuffix('.out') + '0.png'
    # plt.savefig(pngname, dpi=300)
    print(f'RDF has been plotted to {pngname}')

    r, rdf = data[-1].T
    plt.plot(r, rdf)
    plt.xlabel(r'$r (\AA)$')
    plt.ylabel('g(r)')
    plt.title('Radial Distribution Function')
    plt.legend([f'g(r) for {filename}'])
    pngname = filename.removesuffix('.out') + '1.png'
    # plt.savefig(pngname, dpi=300)
    print(f'RDF has been plotted to {pngname}')


if __name__ == '__main__':
    filename = r'msd.out'
    plot_msd(filename)
    # plt.show()