import numpy as np

def read_dipole(filename=r'dipole.out'):
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(r'dipole_m.log', 'w') as f:
        f.writelines(lines[::2])
    data = np.genfromtxt(r'dipole_m.log', comments='#', delimiter=None)
    volume = round(float(lines[0].split()[5]), 4)
    return data, volume

def calc_k():
    data, volume = read_dipole() # volume in A^3
    # parameters and unit conversion
    volume = volume * 1e-30  # volume in m^3
    temperature = 300.0  #  in Kelvin
    eps0 = 8.854187817e-12  # Vacuum permittivity, in C^2/N/m^2
    kB = 1.38064852e-23  # Boltzmann constant, in J/K
    ec = 1.602e-19  # Elementary charge, in C
    eA2Cm_sq = (ec*1e-10)**2  # dipole, from e*Angstrom to C*m
    # kcalmol2J = 4183.9954/(6.022*10**23)  # energy, from kcal/mol to J

    # Separate the data into uniaxial dipole and total dipole moment components
    # dipole_xyz = data[:,1:-1]
    t_dipole = data[:,-1]

    # Calculate the variance of the total dipole moment
    # var(M^2) = <M^2> - <M>^2
    var_dipole = np.var(t_dipole)

    # Calculate the dielectric constant using the fluctuation formula
    diele_const = 1.0 + var_dipole*eA2Cm_sq / (3.0 * eps0 * volume * kB * temperature)
    return diele_const

if __name__ == '__main__':
    diele_const = calc_k()
    print(f"Dielectric constant: {diele_const:.6f}")
    # exp: 4.2
    # PAW: 4.7261
    # uff: 2.02

