import numpy as np
import matplotlib.pyplot as plt

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    timesteps, msd_x, msd_y, msd_z, msd_tt, temp = read_msd(filename).T
    plt.scatter(temp, msd_x, s=.5)
    plt.scatter(temp, msd_y, s=.5)
    plt.scatter(temp, msd_z, s=.5)
    plt.scatter(temp, msd_tt, s=1.5) # total MSD
    plt.xlabel('Temperature (K)')
    plt.ylabel('MSD')
    plt.title('Mean Squared Displacement')
    plt.legend([r'$MSD_x$', r'$MSD_y$', r'$MSD_z$', r'$MSD_{total}$'])
    pngname = r'msd.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

if __name__ == '__main__':
    filename = r'msd.out'
    plot_msd(filename)
    # plt.show()