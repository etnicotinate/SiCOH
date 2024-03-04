# change structure file (lmpdata) name in lmp file
obj_dir=r'.'
old_str=r'(variable\s+structure\s+string).+'
re_flag=True

import os
import re
def str_replace(obj_dir,old_str,new_str,re_flag=False):
    '''
    replace a string in file
    '''
    with open(obj_dir, 'r') as f:  
        txt = f.read()  
        if re_flag:
            str_replace = re.sub(old_str, new_str, txt, count=1)
        else:
            str_replace = txt.replace(old_str,new_str)
        with open(obj_dir, 'w') as f:
            f.write(str_replace)      

def multi_replace(obj_dir,old_str,re_flag=False):
    '''
    replace strings in each file in a directory
    '''
    if re_flag:
        old_str = re.compile(old_str)
    for root, dirs, files in os.walk(obj_dir):
        for file in files:
            if file.endswith(r'.lmp'):
                new_str=r'\1 '+os.path.split(root)[-1]
                file_path=os.path.join(root,file)
                # change the initial structure file name in lmp file
                str_replace(file_path,old_str,new_str,re_flag)
                print(f'{file_path} is modified.')
            if file == (r'run.sh'):
                new_str=r'\1 '+os.path.split(root)[-1]
                file_path=os.path.join(root,file)
                # remove '&' in each `run.sh`
                str_replace(file_path,r'&',r'',re_flag=False)
                print(f'{file_path} is modified.')

multi_replace(obj_dir,old_str,re_flag=re_flag)
