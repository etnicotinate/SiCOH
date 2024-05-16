# change box and connection information in structure files (lmpdata) 
work_dir=r'.'

import re
conn_patern1 = re.compile(r'\d+\s+(bond|angle|dihedral|improper).+\n')
conn_patern3 = re.compile(r'Bonds(\n|.)+')
cell_pattern = re.compile(r'.+xhi\n.+yhi\n.+zhi\n')
re_flag=True

def read_cell(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        for cl, line  in enumerate(lines):
            if '_cell_length_a' in line:
                a = float(line.split()[-1])
                b = float(lines[cl+1].split()[-1])
                c = float(lines[cl+2].split()[-1])
                alpha = float(lines[cl+3].split()[-1])
                beta = float(lines[cl+4].split()[-1])
                gamma = float(lines[cl+5].split()[-1])
                break
    return a, b, c, alpha, beta, gamma

def transform(a, b, c, alpha, beta, gamma, gap=0.0):
    """
    Transforms a, b, c, alpha, beta, gamma to x, y, z, xy, xz, yz,
    gap: between the two neighboring boxes, avoid overlap
    """
    import numpy as np

    alpha = np.radians(alpha)
    beta = np.radians(beta)
    gamma = np.radians(gamma)
    a += gap
    b += gap
    c += gap
    x = a
    xy = b*np.cos(gamma)
    xz = c*np.cos(beta)
    y = np.sqrt(b**2 - xy**2)
    yz = (b*c*np.cos(alpha) - xy*xz)/y
    z = np.sqrt(c**2 - xz**2 - yz**2)
    return x, y, z, xy, xz, yz

def format_box(a, b, c, alpha, beta, gamma):
    x, y, z, xy, xz, yz = transform(a, b, c, alpha, beta, gamma)
    xlo_b = 0.0
    xhi_b = x   + max(0.0,xy,xz,xy+xz)
    ylo_b = 0.0
    yhi_b = y   + max(0.0,yz)
    zlo_b = 0.0
    zhi_b = z

    box_info = f'''
  {xlo_b:>8.4f} {xhi_b:>8.4f}  xlo xhi
  {ylo_b:>8.4f} {yhi_b:>8.4f}  ylo yhi
  {zlo_b:>8.4f} {zhi_b:>8.4f}  zlo zhi
  {xy:>8.4f} {xz:>8.4f} {yz:>8.4f}  xy xz yz
    '''
    return box_info

def str_replace(obj_dir,old_str,new_str,re_flag=False):
    '''
    replace a string in a file
    '''
    with open(obj_dir, 'r') as f:  
        txt = f.read()  
        if re_flag:
            str_replace = re.sub(old_str, new_str, txt)
        else:
            str_replace = txt.replace(old_str,new_str)
        with open(obj_dir, 'w') as f:
            f.write(str_replace)      

def multi_replace(obj_dir,re_flag=False):
    '''
    replace strings in each file in a directory
    '''
    import os
    for root, dirs, files in os.walk(obj_dir):
        for file in files:
            if file.endswith('.data'):
                file_path=os.path.join(root,file)
                name=file.removesuffix('.data')
                cif_path=os.path.join(root,'../cif', name+'.cif')
                cell_info = read_cell(cif_path)
                cell_info = format_box(*cell_info)
                str_replace(file_path,cell_pattern,cell_info,re_flag)
                str_replace(file_path,conn_patern1,'',re_flag)
                str_replace(file_path,conn_patern3,'',re_flag)
                print(f'{file_path} is modified.')

multi_replace(work_dir,re_flag=re_flag)
