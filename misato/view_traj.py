import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
import MDAnalysis as mda
import h5py
import os, subprocess

mdh5_file_tiny = '/data/rishabh/MD/h5_files/MD.hdf5'
md_H5File_tiny = h5py.File(mdh5_file_tiny)

pdb_codes = list(dict(md_H5File_tiny).keys())
print ("number of PDBs:", len(pdb_codes))

def combine_pdbs(struct):
    # Define the path to your PDB files directory
    pdb_directory = f'combined_{struct}/'

    # Create an empty list to store coordinate data
    combined_coordinates = []

    # Loop through the PDB files and extract coordinates
    for timestep in range(100):  # Assuming you have 100 PDB files
        pdb_filename = os.path.join(pdb_directory, f'{struct}_MD_frame{timestep}.pdb')
        
        with open(pdb_filename, 'r') as pdb_file:
            coordinates = []
            for line in pdb_file:
                if line.startswith('ATOM'):
                    coordinates.append(line)
            combined_coordinates.append(coordinates)

    # Write the combined coordinates to a new PDB file
    output_filename = f'{struct}_final_animation.pdb'
    with open(output_filename, 'w') as output_file:
        for timestep, coordinates in enumerate(combined_coordinates, start=1):
            output_file.write(f'MODEL {timestep}\n')
            output_file.writelines(coordinates)
            output_file.write('ENDMDL\n')

    print(f'Combined PDB file saved as {output_filename}')

    return output_filename

mk_cmd = f"mkdir all_misato_anim"
subprocess.call(mk_cmd, shell=True)

for pdb in pdb_codes:
    odj = md_H5File_tiny[pdb]

    for i in range(100):
        cmd = f"python h5_to_pdb.py -s {pdb.upper()} -dMD '/data/rishabh/MD/h5_files/MD.hdf5' -f {i} -o combined_{pdb.upper()}/"
        subprocess.call(cmd, shell=True)

    fname = combine_pdbs(pdb)

    rm_cmd = f"rm -rf combined_{pdb.upper()}/"
    subprocess.call(rm_cmd, shell=True)

    mv_cmd = f"mv {fname} all_misato_anim/"
    subprocess.call(mv_cmd, shell=True)