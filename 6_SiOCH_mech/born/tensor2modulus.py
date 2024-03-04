from sys import exit
import numpy as np

filename = r"C.lmp.log"
method = 'v' # 'v' for Voigt, 'r' for Reuss

def read_data(filename):
    data = []
    with open(filename,'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            data.append(line.strip().split())
    C = np.matrix(data, np.float64)
    return C

def check_symmetric(C):
    if not np.allclose(C, C.T):
        print("Incorrect stiffness marix: not symmetric.")
        exit()

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

'''
BV = 26.889 GPa	
EV = 87.803 GPa	
GV = 45.933 GPa	
νV = -0.044234
'''

if __name__ == '__main__':
    C = read_data(filename)
    check_symmetric(C)
    if method == 'v':
        Voigt(C)
    elif method == 'r':
        Reuss(C)
    check_positive_definite(C)
    

