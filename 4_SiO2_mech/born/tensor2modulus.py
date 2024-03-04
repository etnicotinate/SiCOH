import numpy as np

filename = r"C.log"
method = 'v' # 'v' for Voigt, 'r' for Reuss, 'v+r' for both

def read_data(filename):
    # data = []
    # with open(filename,'r') as f:
    #     for line in f:
    #         if line.startswith('#') or line=='\n':
    #             continue
    #         data.append(line.strip().split())
    data = np.genfromtxt(filename, comments='#', delimiter=None)
    C = np.matrix(data, np.float64)
    return C

def check_symmetric(C):
    assert np.allclose(C, C.T), "Incorrect stiffness marix: not symmetric."

def check_positive_definite(C):
    if not np.all(np.linalg.eigvals(C) > 0):
        print("\nCrystal is mechanically unstable: stiffness marix is not positive definite.")

def bulk_modulus(C):
    B = 1.0/9.0 * (C[0,0] + C[1,1] + C[2,2] + 2*(C[0,1] + C[1,2] + C[2,0]))
    return B

def shear_modulus(C):
    G = 1.0/15.0 * (C[0,0] + C[1,1] + C[2,2] - (C[0,1] + C[1,2] + C[2,0]) + 3*(C[3,3] + C[4,4] + C[5,5]))
    return G

def youngs_modulus(B, G):
    # B = bulk_modulus(C)
    # G = shear_modulus(C)
    E = 9 * B * G / (3 * B + G)
    return E

# 
def poisson_ratio(B, G):
    '''
    Always: 0.0 < nu < 0.5
    nu indicates the lateral response to loading,
    which is the ratio of lateral strain to axial strain.
    Materials with high Poisson's ratio are ductile,
    empirically, nu > 0.31 indicates a good Ductility.
    '''
    # B = bulk_modulus(C)
    # G = shear_modulus(C)
    nu = (3 * B - 2 * G) / (6 * B + 2 * G)
    return nu

# Voigt notation: Upper bound method
def Voigt(C):
    Bv = bulk_modulus(C)    # bulk modulus
    Gv = shear_modulus(C)   # shear modulus
    Ev = youngs_modulus(Bv, Gv)  # Young's modulus
    nu = poisson_ratio(Bv, Gv) # Poisson's ratio
    return Bv, Gv, Ev, nu

# Reuss notation: Lower bound method
def Reuss(C):
    S = C.I
    Br = bulk_modulus(S)    # bulk modulus
    Gr = shear_modulus(S)   # shear modulus
    Er = youngs_modulus(Br, Gr)  # Young's modulus
    nu = poisson_ratio(Br, Gr) # Poisson's ratio
    return Br, Gr, Er, nu

def uni_aniso_index(Bv, Br, Gv, Gr):
    '''
    Universal elastic anisotropy index: 
    higher value indicates higher anisotropy,
    which will cause the microcracks. 
    (AU = 0: completely isotropic)
    doi-org/10.1103/PhysRevLett.101.055504
    '''
    AU = 5*Gv/Gr + Bv/Br - 6.0
    assert AU > 0, "Universal elastic anisotropy index must be positive."
    return AU

def print_results(B, G, E, nu):
    print(f"Bulk modulus: {B:.4f} Gpa")
    print(f"Shear modulus: {G:.4f} Gpa")
    print(f"Young's modulus: {E:.4f} Gpa")
    print(f"Poisson's ratio: {nu:.4f}")
    check_positive_definite(C)

if __name__ == '__main__':
    C = read_data(filename)
    check_symmetric(C)
    if method == 'v':
        B, G, E, nu = Voigt(C)
        print("Voigt notation:")
        print_results(B, G, E, nu)
    elif method == 'r':
        B, G, E, nu = Reuss(C)
        print("Reuss notation:")
        print_results(B, G, E, nu)
    # elif method == 'v+r':
    #     Bv, Gv, Ev, nuv = Voigt(C)
    #     Br, Gr, Er, nur = Reuss(C)
    #     uni_aniso_index(Bv, Br, Gv, Gr)
    

