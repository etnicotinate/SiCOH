import numpy as np

def read_C():
    '''Read elastic tensor from file'''
    C = np.genfromtxt(r'C.log', comments='#', delimiter=None)
    return C

def write_C(C):
    '''Write elastic tensor to file'''
    np.savetxt(r'C.log', C, fmt='%10.4f', header='Elastic tensor in Gpa')
    
    # with open(r'C.log', 'w') as f:
    #     f.write("# Elastic tensor (GPa)\n")
    #     for i in C:
    #         f.write(f"{i[0]:10.4f} {i[1]:10.4f} {i[2]:10.4f} {i[3]:10.4f} {i[4]:10.4f} {i[5]:10.4f}\n")
    print("Elastic tensor has been written to C.log.")
    return

def check_symmetric(C):
    assert np.allclose(C, C.T), "Incorrect stiffness marix: not symmetric."

def check_positive_definite(C):
    if not np.all(np.linalg.eigvals(C) > 0):
        print("\nCrystal is mechanically unstable: stiffness marix is not positive definite.")

# Voigt notation
def Voigt(C):
    Bv = 1.0/9.0 * (C[0,0] + C[1,1] + C[2,2] + 2*(C[0,1] + C[1,2] + C[2,0]))    # bulk modulus
    Gv = 1.0/15.0 * (C[0,0] + C[1,1] + C[2,2] - (C[0,1] + C[1,2] + C[2,0]) + 3*(C[3,3] + C[4,4] + C[5,5]))  # shear modulus
    Ev = 9 * Bv * Gv / (3.0 *Bv + Gv)  # Young's modulus
    miu = (3 * Bv - 2 * Gv) / (6 *Bv + 2 * Gv) # Poisson's ratio
    print("Voigt notation:")
    print(f"Bulk modulus: {Bv:.4f} Gpa")
    print(f"Shear modulus: {Gv:.4f} Gpa")
    print(f"Young's modulus: {Ev:.4f} Gpa")
    print(f"Poisson's ratio: {miu:.4f}")

# Reuss notation
def Reuss(C):
    s = C.I
    Br = 1.0 / (s[0,0] + s[1,1] + s[2,2] + 2.0*(s[0,1] + s[1,2] + s[2,0]))    # bulk modulus
    Gr = 15.0 / (4.0*(s[0,0] + s[1,1] + s[2,2]) - 4.0*(s[0,1] + s[1,2] + s[2,0]) + 3.0*(s[3,3] + s[4,4] + s[5,5]))  # shear modulus
    Er = 9.0 * Br * Gr / (3.0 *Br + Gr)  # Young's modulus
    miu = (3.0 * Br - 2.0 * Gr) / (6.0 *Br + 2.0 * Gr) # Poisson's ratio
    print("Reuss notation:")
    print(f"Bulk modulus: {Br:.4f} Gpa")
    print(f"Shear modulus: {Gr:.4f} Gpa")
    print(f"Young's modulus: {Er:.4f} Gpa")
    print(f"Poisson's ratio: {miu:.4f}")

def tensor2modulus(C, method='v'):
    ''''v' for Voigt, 'r' for Reuss'''
    check_symmetric(C)
    if method == 'v':
        Voigt(C)
    elif method == 'r':
        Reuss(C)
    check_positive_definite(C)

def read_stress_strain(filename):
    '''Read stress-strain data from output files'''
    data = np.genfromtxt(filename, delimiter=None, comments="#")
    eps = data[1:,0]    # strain vector(,1)
    sig = data[1:,1:]   # stress tensor(,6)
    return eps, sig

def calc_tensor():
    '''Calculate elastic tensor from stress-strain data'''
    C=np.zeros((6,6))
    for i in range(6):
        eps, sig = read_stress_strain(f'stress_strain/stress_strain.neg{i+1}.out')
        ncc = np.array([np.cov(eps,sig[:,j],ddof=0)[0,-1]/np.var(eps) for j in range(6)])
        eps, sig = read_stress_strain(f'stress_strain/stress_strain.pos{i+1}.out')
        pcc = np.array([np.cov(eps,sig[:,j],ddof=0)[0,-1]/np.var(eps) for j in range(6)])
        C[i,:] = 0.5*(ncc+pcc)
        C = 0.5 * (C + C.T)
    return C

def plot_curve(mode='pos', dir: str|int='all'):
    '''
    mode: 'pos' for positive deformation, 'neg' for negative deformation.
    dir: direction of deformation. 'all' for all directions, 1,2,3,4,5,6 for xx,yy,zz,yz,xz,xy direction, respectively.
    '''
    from matplotlib import pyplot as plt
    # all directions
    if dir == 'all':
        plt.figure(figsize=(15,10))
        for i in range(1,6+1):
            filename = f'stress_strain/stress_strain.{mode}{i}.out'
            eps, sig = read_stress_strain(filename)
            if i > 3:
                xlabel = r'Strain (double), $2 \epsilon$'
            else:
                xlabel = r'Strain, $\epsilon$'
            plt.subplot(2,3,i)
            plt.xlabel(xlabel)
            plt.ylabel(r'Stress, $\sigma$ (Gpa)')
            plt.plot(eps, sig, linewidth=1.5,marker='o',markersize=3)
            plt.title(f'{mode}{i}',x=0.1,y=1.0)
            plt.legend(labels=['1', '2', '3', '4', '5', '6'])
        pngpath = f'stress_strain/stress_strain.{mode}_all.png'
        plt.savefig(pngpath, dpi=300, transparent=True)
        print(f"Stress-strain curve for all {mode} directions has been plotted to {pngpath}\n")
        return
    # single direction
    dir = int(dir)
    filename = f'stress_strain/stress_strain.{mode}{dir}.out'
    eps, sig = read_stress_strain(filename)
    # plt.figure(figsize=(8,5))
    if dir > 3:
        xlabel = r'Strain (double), $2 \epsilon$'
    else:
        xlabel = r'Strain, $\epsilon$'
    plt.xlabel(xlabel)
    plt.ylabel(r'Stress, $\sigma$ (Gpa)')
    plt.plot(eps, sig, linewidth=1.5,marker='o',markersize=3)
    plt.title(f'Stress-strain curve for {mode}{dir} deformation',x=0.5,y=1.0)
    plt.legend(labels=['sig1', 'sig2', 'sig3', 'sig4', 'sig5', 'sig6'])
    pngpath = f'stress_strain/stress_strain.{mode}{dir}.png'
    plt.savefig(pngpath, dpi=300, transparent=True)
    print(f"Stress-strain curve for {mode}{dir} direction has been plotted to {pngpath}\n")
    return

if __name__ == '__main__':
    C = calc_tensor()
    write_C(C)
    # plot_curve(dir='all')
    # C = read_C(r'C.log')
    tensor2modulus(C)
    

