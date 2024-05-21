import numpy as np

def read_msd(filename):
    data = np.genfromtxt(filename, comments='#')
    return data

def plot_msd(filename):
    import matplotlib.pyplot as plt

    t, msd_x, msd_y, msd_z, msd_tt, temp = read_msd(filename).T
    plt.plot(t, msd_x)
    plt.plot(t, msd_y)
    plt.plot(t, msd_z)
    plt.plot(t, msd_tt**0.5) # total MSD
    plt.xlabel('Timesteps (0.5 fs)')
    plt.ylabel('MSD')
    plt.title('Mean Squared Displacement')
    plt.legend([r'$MSD_x$', r'$MSD_y$', r'$MSD_z$', r'$MSD_{total}$'])
    pngname = filename.removesuffix('.out') + '.png'
    plt.savefig(pngname, dpi=300)
    print(f'MSD has been plotted to {pngname}')

if __name__ == '__main__':
    filename = r'msd.out'
    plot_msd(filename)
    # plt.show()