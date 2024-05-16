import numpy as np

# define GLOBAL variables
# BOND_SELECTED = {'Si-Si', 'H-Si', 'C-O', 'O-O', 'H-H'}
BOND_SELECTED = {'Si-O', 'H-C', 'Si-H', 'Si-C', 'O-H',}
ATOM_DIC = {'1': 'C', '2': 'H', '3': 'O', '4': 'Si'}
# ATOM_DIC = {1: 'C', 2: 'H', 3: 'O', 4: 'Si'}
'''
1 12.0107 # C
2 1.00794 # H
3 15.9994 # O
4 28.0855 # Si
'''

def build_atom_table(reaxff):
    '''
    Build a table mapping atoms-id(str) and its atomic type(str) from reaxff file object
    '''
    end_flag = False    # Flag to indicate the end of the data block
    for line in reaxff:
            if "Timestep" in line:
                if end_flag:
                    break
                ATOM_TABLE = dict()
                end_flag = True
            elif line.strip() and not line.startswith("#"):
                # Process data lines
                atom_id, atom_type = line.split()[:2]
                ATOM_TABLE[atom_id] = atom_type
    return ATOM_TABLE

def write_bonds_log(filename):
    """
    Extract bonds information from bonds.*.reaxff, and write to bonds.*.log.

    Args:
    - filename (str): Path to the bonds.*.reaxff file.
    
    Returns:
    - None
    """

    # bonds.*.log
    logname = filename.removesuffix('reaxff')+'log'
    
    # Read the bonds.*.reaxff, write to bonds.*.log
    with open(filename, 'r') as reaxff:
        ATOM_TABLE = build_atom_table(reaxff)
        reaxff.seek(0)
        with open(logname, 'w') as log:
        
            for line in reaxff:
                if "Timestep" in line:
                    log.write(line)
                    log.write('# bond id, atom1 type, atom2 type, atom1 id, atom2 id, bond order, atom1 notation, atom2 notation\n')
                    # create a set to record bond-ids for each frame
                    bond_set = set()
                    bond_id = 1
                elif line.strip() and not line.startswith("#"):
                    # Process data lines
                    data_parts = line.split()
                    atom1_id, atom1_type, nbonds = data_parts[:3]
                    nbonds = int(nbonds)   # nbonds: number of bonds on atom1
                    # check each bond with atom2 and its bond_order
                    for i in range(nbonds):
                        atom2_id = data_parts[3+i]
                        atom2_type = ATOM_TABLE[atom2_id]
                        bond_order = data_parts[3+nbonds+i+1]

                        # sorted[atom1, atom2] to unit the order of atom1 and atom2 in set
                        # tuple is hashable can be in the set
                        new_key = tuple(sorted([atom1_id, atom2_id]))
                        # add new bond to bond_dict
                        if new_key not in bond_set:
                            bond_set.add(new_key)
                            # bond id, atom1 type, atom2 type, atom1 id, atom2 id, bond order, atom1 notation, atom2 notation
                            log.write(f"{bond_id:>4} {atom1_type:>4} {atom2_type:>4} {atom1_id:>4} {atom2_id:>4} {bond_order:>6}    {ATOM_DIC[atom1_type]:<3} {ATOM_DIC[atom2_type]:<3}\n")
                            bond_id += 1
    return      
                                                
def read_bonds(filename):
    """
    Read bonds info from a bonds.reaxff, splitting the content by frames.
    Each timestep's data is stored in a dictionary.
    
    Args:
    - filename (str): Path to the data file.
    
    Returns:
    - list: A list of dictionaries, each containing data for a single timestep.
    """
    
    logname = filename.removesuffix('reaxff')+'log' # bonds.*.log
    write_bonds_log(filename) # rewrite the bonds.*.reaxff file
        
    # Read the bonds.*.log file
    Frames = []
    data_list = []
    timestep = None

    with open(logname, 'r') as file:
        for line in file:
            if "Timestep" in line:
                # If not the first timestep, save the current timestep data
                if timestep is not None:
                    data = np.array(data_list)
                    Frames.append({
                        'timestep': timestep,
                        'data': data,
                        'bond_id': data[:, 0],
                        'atom1': data[:, 1],
                        'atom2': data[:, 2],
                    })
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
        
        # Append the last timestep's data
        if data_list:
            Frames.append({
                'timestep': timestep,
                'data': data,
                'bond_id': data[:, 0],
                'atom1': data[:, 1],
                'atom2': data[:, 2],
                'a1': data[:, 3],
                'a2': data[:, 4],
            })
    
    return Frames

def calc_bonds_perc(frames):
    '''
    Calculate the percentage of each bond type in all frames,
    return percentage data and labels.
    '''
    Percs = []  # percentage list of all bonds
    labels = [] # labels on plots
    # get all possible atomic combinations of bonds
    for a1,a2 in ((i,j) for i in ATOM_DIC for j in ATOM_DIC if i>=j):
        # print(a1,a2)
        labels.append(f'{ATOM_DIC[a1]}-{ATOM_DIC[a2]}')
        cur_perc = []
        for frame in frames:
            tolal_bonds = len(frame['bond_id']) 
            select_condition = ( (frame['atom1'] == a1) & (frame['atom2'] == a2) ) | ( (frame['atom1'] == a2) & (frame['atom2'] == a1) )
            cur_bond = np.sum(select_condition)
            # print(f'{ATOM_DIC[a1]}-{ATOM_DIC[a2]}: {cur_bond=}')
            cur_perc.append(cur_bond / tolal_bonds * 100)
        Percs.append(cur_perc)
    Percs = np.array(Percs)
    return Percs, labels

def calc_bonds(frames):
    '''
    Calculate the percentage of each bond type in all frames,
    return percentage data and labels.
    '''
    Nbonds = []  # percentage list of all bonds
    labels = [] # labels on plots
    # get all possible atomic combinations of bonds
    for a1,a2 in ((i,j) for i in ATOM_DIC for j in ATOM_DIC if i>=j):
        # print(a1,a2)
        labels.append(f'{ATOM_DIC[a1]}-{ATOM_DIC[a2]}')
        cur_bonds = []  # all bonds number list for current frame
        for frame in frames:
            # tolal_bonds = len(frame['bond_id']) 
            select_condition = ( (frame['atom1'] == a1) & (frame['atom2'] == a2) ) | ( (frame['atom1'] == a2) & (frame['atom2'] == a1) )
            cur_bond = np.sum(select_condition) # 1 bond number for current frame
            # print(f'{ATOM_DIC[a1]}-{ATOM_DIC[a2]}: {cur_bond=}')
            cur_bonds.append(cur_bond)
        Nbonds.append(cur_bonds)
    Nbonds = np.array(Nbonds)
    return Nbonds, labels

def count_QTD_SiO(frames):
    '''
    Calculate the percentage of each bond type in all frames,
    return percentage data and labels.
    '''
    from collections import Counter, defaultdict

    QTD = []  # QTD dict list of all frames
    for frame in frames:
        data = frame['data']

        si_o_bonds = defaultdict(int)
        for row in data:
            atom1_notation = row[-2]
            atom2_notation = row[-1]
            atom1_id = row[3]
            atom2_id = row[4]
            
            if atom1_notation == 'Si' and atom2_notation == 'O':
                si_o_bonds[atom1_id] += 1
            elif atom1_notation == 'O' and atom2_notation == 'Si':
                si_o_bonds[atom2_id] += 1

        # Initialize QTD dictionary
        cur_QTD = {'Q': [], 'T': [], 'D': [], 'M': []}

        # Categorize Si atoms into Q, T, D, and M groups
        for si_id, o_count in si_o_bonds.items():
            if o_count == 1:
                cur_QTD['M'].append(si_id)
            elif o_count == 2:
                cur_QTD['D'].append(si_id)
            elif o_count == 3:
                cur_QTD['T'].append(si_id)
            elif o_count == 4:
                cur_QTD['Q'].append(si_id)

        # Count the number of Si atoms in each group
        QTD.append(cur_QTD)
            
    # QTD_counts: {Q: [Si_id1,...], T: [Si_id1,...], D: [Si_id1,...], M: [Si_id1,...]}    
    # QTD_counts = {c: len(ids) for c, ids in QTD}
    QTD_counts = {c: np.array([len(Si[c]) for Si in QTD]) for c in {'Q', 'T', 'D', 'M'}}

    return QTD, QTD_counts

# def count_QTD_SiO0(frames):
#     '''
#     Calculate the percentage of each bond type in all frames,
#     return percentage data and labels.
#     '''
#     QTD = []  # QTD dict list of all frames
#     for frame in frames:
#         data = frame['data']
#         SiO_data = data[((data[:,-2] == 'Si') & (data[:,-1] == 'O')) | ((data[:,-2] == 'O') & (data[:,-1] == 'Si'))]
#         # SiO_data = data[(data[:,-2] == 'Si') & (data[:,-1] == 'O')]
#         from collections import Counter
#         # count Si number for each Si from O_id column (SiO_data[:,4])
#         counts_dict = Counter(SiO_data[:,3])

#         # build current QTD dict, {O counts: [Si_id1,...]}
#         cur_QTD = {c: [] for c in {'Q', 'T', 'D', 'M'}} # {O counts: [Si_id1,...]} for current frame
#         for si,c in counts_dict.items():
#             if c == 4:
#                 cur_QTD['Q'].append(si)
#             elif c == 3:
#                 cur_QTD['T'].append(si)
#             elif c == 2:
#                 cur_QTD['D'].append(si)
#             elif c == 1:
#                 cur_QTD['M'].append(si)

#         QTD.append(cur_QTD)
        
#     # QTD_counts: {Q: [Si_id1,...], T: [Si_id1,...], D: [Si_id1,...], M: [Si_id1,...]}    
#     QTD_counts = {c: np.array([len(Si[c]) for Si in QTD]) for c in {'Q', 'T', 'D', 'M'}}
#     return QTD, QTD_counts

def plot_QTD(filename):
    from matplotlib import pyplot as plt
    
    frames = read_bonds(filename)
    T = [frame['timestep'] for frame in frames]
    QTD, QTD_counts = count_QTD_SiO(frames)
    labels = QTD_counts.keys()
    plt.figure(figsize=(15,10))

    print('Initial QTDM counts: ', end='')
    for c in labels:
        print(f'{c}: {QTD_counts[c][0]}, ', end='')
        plt.plot(T, QTD_counts[c], linewidth=2.0,marker='o',markersize=2.5)  # counts
    print()

    # set axis scale
    ax=plt.gca()
    y_major_locator=plt.MultipleLocator(2)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.xlabel(r'Timesteps')
    plt.ylabel(r'Number of Q, T, D, M')
    plt.title(r'Substructure statistics during deformation', x=0.5,y=1.0)
    plt.legend(labels=labels)
    pngname = r'QTD.png'
    plt.savefig(pngname, dpi=300, transparent=True, bbox_inches='tight')
    print(f"QTD has been plotted to {pngname}\n")
    return

def plot_bonds_perc(mode='pos', dir: str|int='all'):
    '''
    mode: 'pos' for positive deformation, 'neg' for negative deformation.
    dir: direction of deformation. 'all' for all directions, 1,2,3,4,5,6 for xx,yy,zz,yz,xz,xy direction, respectively.
    If meet the error "TypeError: unsupported operand type(s) for |: 'type' and 'type'",
    change the function define line into (because your Python version < 3.10)
    ```
    def plot_curve(mode='pos', dir='all'):
    ```
    '''
    from matplotlib import pyplot as plt
    # # all directions
    if dir == 'all':
        plt.figure(figsize=(15,10))
        for d in range(1,6+1):
            filename = f'./bonds.{mode}{d}.reaxff'
            frames = read_bonds(filename)
            T = [f['timestep'] for f in frames] # X axis data: timesteps
            Percs, Bond_types = calc_bonds_perc(frames) # Y axis data: bonds percentage; labels: bond types
            labels = []

            plt.subplot(2,3,d)
            for i, bond in enumerate(Bond_types):
                # exclude bonds not in BOND_SELECTED
                if bond not in BOND_SELECTED:
                    continue
                # plt.figure(figsize=(8,5))    
                plt.plot(T, Percs[i,:], linewidth=1.5,marker='o',markersize=2)
                labels.append(bond)

            plt.xlabel(r'Timesteps')
            plt.ylabel(r'Percentage of bonds (%)')
            # print(f'{i=}')
            plt.title(f'Bond statistics in {mode}{d} direction',x=0.5,y=1.0)
            plt.legend(labels=labels)

        # save PNG
        pngpath = f'bonds.{mode}_all.png'
        plt.savefig(pngpath, dpi=300, transparent=True)
        print(f"Bonds for {mode}_all direction has been plotted to {pngpath}\n")
    
    # single direction
    else:
        filename = f'./bonds.{mode}{dir}.reaxff'
        frames = read_bonds(filename)
        T = [f['timestep'] for f in frames] # X axis data: timesteps
        Percs, Bond_types = calc_bonds_perc(frames) # Y axis data: bonds percentage; labels: bond types
        labels = []
        plt.figure(figsize=(8, 5))
        for i, bond in enumerate(Bond_types):
            # exclude bonds not in BOND_SELECTED
            if bond not in BOND_SELECTED:
                continue
            # plt.figure(figsize=(8,5))    
            plt.plot(T, Percs[i,:], linewidth=1.5,marker='o',markersize=2)
            labels.append(bond)

        plt.xlabel(r'Timesteps')
        plt.ylabel(r'Percentage of bonds (%)')
        plt.title(f'Bond statistics during deformation in {mode}{dir} direction',x=0.5,y=1.0)
        plt.legend(labels=labels)

        # save PNG
        pngpath = f'bonds.{mode}{dir}.png'
        plt.savefig(pngpath, dpi=300, transparent=True)
        print(f"Bonds for {mode}{dir} direction has been plotted to {pngpath}\n")
    return

def plot_bonds(mode='pos', dir: str|int='all'):
    '''
    Plot the number of bonds for each bond type in all frames.
    mode: 'pos' for positive deformation, 'neg' for negative deformation.
    dir: direction of deformation. 'all' for all directions, 1,2,3,4,5,6 for xx,yy,zz,yz,xz,xy direction, respectively.
    If meet the error "TypeError: unsupported operand type(s) for |: 'type' and 'type'",
    change the function define line into (because your Python version < 3.10)
    ```
    def plot_curve(mode='pos', dir='all'):
    ```
    '''
    from matplotlib import pyplot as plt
    # # all directions
    if dir == 'all':
        plt.figure(figsize=(15,10))
        for d in range(1,6+1):
            filename = f'./bonds.{mode}{d}.reaxff'
            frames = read_bonds(filename)
            T = [f['timestep'] for f in frames] # X axis data: timesteps
            Nbonds, Bond_types = calc_bonds(frames) # Y axis data: bonds percentage; labels: bond types
            labels = []

            plt.subplot(2,3,d)
            for i, bond in enumerate(Bond_types):
                # exclude bonds not in BOND_SELECTED
                if bond not in BOND_SELECTED:
                    continue
                # plt.figure(figsize=(8,5))    
                plt.plot(T, Nbonds[i,:], linewidth=1.5,marker='o',markersize=2)
                labels.append(bond)

            plt.xlabel(r'Timesteps')
            plt.ylabel(r'Number of bonds')
            # print(f'{i=}')
            plt.title(f'Bond statistics in {mode}{d} direction',x=0.5,y=1.0)
            plt.legend(labels=labels)

        # save PNG
        pngpath = f'bonds.{mode}_all.png'
        plt.savefig(pngpath, dpi=300, transparent=True)
        print(f"Bonds for {mode}_all direction has been plotted to {pngpath}\n")
    
    # single direction
    else:
        filename = f'./bonds.{mode}{dir}.reaxff'
        frames = read_bonds(filename)
        T = [f['timestep'] for f in frames] # X axis data: timesteps
        Nbonds, Bond_types = calc_bonds(frames) # Y axis data: bonds percentage; labels: bond types
        labels = []
        plt.figure(figsize=(8,5))
        for i, bond in enumerate(Bond_types):
            # exclude bonds not in BOND_SELECTED
            if bond not in BOND_SELECTED:
                continue
            # plt.figure(figsize=(8,5))    
            plt.plot(T, Nbonds[i,:], linewidth=1.5,marker='o',markersize=2)
            labels.append(bond)

        plt.xlabel(r'Timesteps')
        plt.ylabel(r'Number of bonds')
        plt.title(f'Bond statistics during deformation in {mode}{dir} direction',x=0.5,y=1.0)
        plt.legend(labels=labels)

        # save PNG
        pngpath = f'bonds.{mode}{dir}.png'
        plt.savefig(pngpath, dpi=300, transparent=True)
        print(f"Bonds for {mode}{dir} direction has been plotted to {pngpath}\n")
    return


if __name__ == '__main__':
    # plot_bonds(mode='pos', dir='all')
    plot_bonds(mode='pos', dir=3)
    plot_QTD(r'./bonds.pos3.reaxff')


    
