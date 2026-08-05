################ Developed by Pratyush Dhal ####################
import numpy as np
import argparse
import sys

#Read gro file

def read_gro(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    title = lines[0].strip()
    num_atoms = int(lines[1].strip())
    
    coords = []
    atom_metadata = []
    atom_lines = lines[2:2+num_atoms]
    
    for line in atom_lines:
        # Parse GROMACS .gro format
        resnr = int(line[0:5].strip())
        resname = line[5:10].strip()
        atomname = line[10:15].strip()
        x = float(line[20:28])
        y = float(line[28:36])
        z = float(line[36:44])
        coords.append([x, y, z])
        atom_metadata.append({'resnr': resnr, 'resname': resname, 'atomname': atomname})
    
    coords = np.array(coords)
    
    box_line = lines[2+num_atoms].split()
    box = np.array(box_line, dtype=float)
    box = box.reshape(3, 3) if len(box) == 9 else np.diag(box)
    
    # Auto-detect atoms per molecule by finding when residue number changes
    resnumbers = [meta['resnr'] for meta in atom_metadata]
    atoms_per_mol = num_atoms  # default: single molecule
    
    for i in range(1, len(resnumbers)):
        if resnumbers[i] != resnumbers[i-1]:
            # Found where second molecule starts
            atoms_per_mol = i
            break
    
    num_mols = num_atoms // atoms_per_mol
    
    # Verify the division is clean
    if num_atoms % atoms_per_mol != 0:
        print(f"WARNING: {num_atoms} atoms doesn't divide evenly by {atoms_per_mol} atoms/mol")
        print(f"         This may indicate residue numbering issues in the .gro file")
    
    coords = coords.reshape(num_mols, atoms_per_mol, 3)
    
    return coords, box, atom_metadata, atoms_per_mol, num_mols

#Read multi-frame GROMACS .gro file (trajectory)
def read_gro_multiframe(filename, atoms_per_mol, mols_per_frame):
    with open(filename, 'r') as f:
        lines = f.readlines()
    frames, box_vectors = [], []
    i, total_lines = 0, len(lines)
    
    while i < total_lines:
        if i+1 >= total_lines:
            break
        num_atoms = int(lines[i+1].strip())
        atom_lines = lines[i+2:i+2+num_atoms]
        coords = []
        for line in atom_lines:
            x = float(line[20:28])
            y = float(line[28:36])
            z = float(line[36:44])
            coords.append([x, y, z])
        coords = np.array(coords).reshape(mols_per_frame, atoms_per_mol, 3)
        box_line = lines[i+2+num_atoms].split()
        box = np.array(box_line, dtype=float)
        box = box.reshape(3, 3) if len(box) == 9 else np.diag(box)
        frames.append(coords)
        box_vectors.append(box)
        i += 2 + num_atoms + 1
    
    return frames, box_vectors

#Write .gro file using atom metadata from reference structure"""
def write_gro(filename, coords, box, atom_metadata, title="Backmapped structure"):
 
    n_atoms = coords.shape[0]
    with open(filename, 'w') as f:
        f.write(f"{title}\n")
        f.write(f"  {n_atoms}\n")
        for i, (atom, meta) in enumerate(zip(coords, atom_metadata)):
            atomnr = i + 1
            f.write(f'{meta["resnr"]:5d}{meta["resname"]:<5s}{meta["atomname"]:>5s}{atomnr:5d}'
                   f'{atom[0]:8.3f}{atom[1]:8.3f}{atom[2]:8.3f}\n')
        # Write box vectors
        if box.ndim == 2:
            f.write(f"{box[0,0]:10.5f}{box[1,1]:10.5f}{box[2,2]:10.5f}")
            f.write(f"{box[0,1]:10.5f}{box[0,2]:10.5f}{box[1,0]:10.5f}")
            f.write(f"{box[1,2]:10.5f}{box[2,0]:10.5f}{box[2,1]:10.5f}\n")
        else:
            f.write(f"{box[0]:10.5f}{box[1]:10.5f}{box[2]:10.5f}\n")


# *********** INDEX FILE HANDLING ***********

    # Read GROMACS index file with mapping scheme
    # Expected format:
    # [CG sub groups]
    # 0 1 2 3
    # 4 5 6
    # 7 8 9
    
    # [AA sub groups]
    # 0 1 2 3 4 5 6 19 20
    # 7 8 9 10 11 12 21 22 23 24 25
    # 13 14 15 16 17 18 26 27 28 29 30

def read_ndx(filename):
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    cg_groups = []
    aa_groups = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        
        if line.startswith('[') and line.endswith(']'):
            section_name = line[1:-1].strip().lower()
            if 'cg' in section_name:
                current_section = 'cg'
            elif 'aa' in section_name:
                current_section = 'aa'
            continue
        
        # Parse atom indices
        indices = [int(x) for x in line.split()]
        
        if current_section == 'cg':
            cg_groups.append(indices)
        elif current_section == 'aa':
            aa_groups.append(indices)
    
    if len(cg_groups) != len(aa_groups):
        raise ValueError(f"Number of CG groups ({len(cg_groups)}) must match AA groups ({len(aa_groups)})")
    
    return cg_groups, aa_groups


# ************* Kabsch-Back ***************


#    Align point set P to Q using Kabsch algorithm
#    Returns: rotation matrix and aligned coordinates

def kabsch_align(P, Q):
    P_centroid = P.mean(axis=0)
    Q_centroid = Q.mean(axis=0)
    P_centered = P - P_centroid
    Q_centered = Q - Q_centroid
    
    # Compute covariance matrix
    H = P_centered.T @ Q_centered
    
    # SVD
    U, _, Vt = np.linalg.svd(H)
    V = Vt.T
    
    # Correct for reflection
    d = np.linalg.det(V @ U.T)
    D = np.diag([1, 1, d])
    
    # Optimal rotation matrix
    R_mat = V @ D @ U.T
    
    # Apply rotation and translation
    P_aligned = (P_centered @ R_mat.T) + Q_centroid
    
    return R_mat, P_aligned



    # Backmap all-atom structure from coarse-grained coordinates
    # Uses simple Kabsch SVD alignment
def backmap_molecule(tgt_cg, ref_cg, ref_aa):
    # Get rotation matrix using Kabsch
    R_mat, _ = kabsch_align(ref_cg, tgt_cg)
    
    # Get centroids
    ref_center = ref_cg.mean(axis=0)
    tgt_center = tgt_cg.mean(axis=0)
    
    # Apply rotation to all-atom structure
    ref_aa_centered = ref_aa - ref_center
    backmapped = (ref_aa_centered @ R_mat.T) + tgt_center
    
    return backmapped


# ----------- MAIN FUNCTION -----------

    # Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Backmap coarse-grained trajectory to all-atom resolution',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 kabsch_back.py -ref_cg cg.gro -ref_aa aa.gro -traj cg_traj.gro -ndx index.ndx -o backmapped.gro
  python3 kabsch_back.py -ref_cg ref_cg.gro -ref_aa ref_aa.gro -traj trajectory.gro -ndx mapping.ndx -o output.gro -ref_mol 26
        """
    )
    
    parser.add_argument('-ref_cg', required=True, help='Reference CG structure (.gro)')
    parser.add_argument('-ref_aa', required=True, help='Reference all-atom structure (.gro)')
    parser.add_argument('-traj', help='CG trajectory to backmap (.gro, multi-frame). If not provided, uses -ref_cg')
    parser.add_argument('-ndx', required=True, help='Mapping index file (.ndx)')
    parser.add_argument('-o', '--output', required=True, help='Output file prefix (without .gro extension)')
    parser.add_argument('-ref_mol', type=int, default=0, help='Reference molecule ID (0-indexed, default: 0)')
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    print("=" * 60)
    print("Kabsch-Back : Backmapping Tool - CG to All-Atom")
    print("=" * 60)
    print()
    
    # If no trajectory specified, use reference CG as single-frame trajectory
    traj_file = args.traj if args.traj else args.ref_cg
    
    print("Input files:")
    print(f"  Reference CG:  {args.ref_cg}")
    print(f"  Reference AA:  {args.ref_aa}")
    print(f"  CG Trajectory: {traj_file}")
    print(f"  Mapping index: {args.ndx}")
    print(f"  Output prefix: {args.output}")
    print(f"  Reference mol: {args.ref_mol}")
    print()
    
    print("=" * 60)
    print("Reading input files...")
    print("=" * 60)
    
    # Read mapping scheme
    print(f"\nReading mapping scheme from {args.ndx}...")
    try:
        cg_subgroups, aa_subgroups = read_ndx(args.ndx)
        print(f"  Found {len(cg_subgroups)} mapping groups")
        for i, (cg, aa) in enumerate(zip(cg_subgroups, aa_subgroups)):
            print(f"    Group {i+1}: {len(cg)} CG beads → {len(aa)} AA atoms")
    except Exception as e:
        print(f"ERROR reading index file: {e}")
        sys.exit(1)
    
    # Load reference CG structure
    print(f"\nReading reference CG structure from {args.ref_cg}...")
    try:
        ref_cg_coords, ref_box, _, cg_atoms_per_mol, cg_num_mols = read_gro(args.ref_cg)
        print(f"  Detected: {cg_num_mols} molecules, {cg_atoms_per_mol} beads/molecule")
        print(f"  Using molecule {args.ref_mol} as reference")
        
        if args.ref_mol >= cg_num_mols:
            print(f"ERROR: Reference molecule {args.ref_mol} out of range (max: {cg_num_mols-1})")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR reading reference CG file: {e}")
        sys.exit(1)
    
    # Load reference AA structure
    print(f"\nReading reference AA structure from {args.ref_aa}...")
    try:
        ref_aa_coords, _, ref_aa_metadata, aa_atoms_per_mol, aa_num_mols = read_gro(args.ref_aa)
        print(f"  Detected: {aa_num_mols} molecules, {aa_atoms_per_mol} atoms/molecule")
            
    except Exception as e:
        print(f"ERROR reading reference AA file: {e}")
        sys.exit(1)
    
    # Load trajectory
    print(f"\nReading CG trajectory from {traj_file}...")
    try:
        frames, box_vectors = read_gro_multiframe(traj_file, cg_atoms_per_mol, cg_num_mols)
        print(f"  Found {len(frames)} frames")
    except Exception as e:
        print(f"ERROR reading trajectory file: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print(f"Starting backmapping: {len(frames)} frames, {cg_num_mols} molecules each")
    print("=" * 60)
    
    rmsd_values = []
    
    for frame_id in range(len(frames)):
        tgt_cg_frame = frames[frame_id]
        current_box = box_vectors[frame_id]
        backmapped_all = []
        
        for mol_i in range(cg_num_mols):
            tgt_cg = tgt_cg_frame[mol_i]
            ref_cg = ref_cg_coords[args.ref_mol]
            ref_aa = ref_aa_coords[args.ref_mol]
            
            sub_backmapped = np.zeros_like(ref_aa)
            
            # Backmap each subgroup
            for cg_map, aa_map in zip(cg_subgroups, aa_subgroups):
                tgt_cg_sub = tgt_cg[cg_map]
                ref_cg_sub = ref_cg[cg_map]
                ref_aa_sub = ref_aa[aa_map]
                
                bm_sub = backmap_molecule(tgt_cg_sub, ref_cg_sub, ref_aa_sub)
                sub_backmapped[aa_map] = bm_sub
                
                # Calculate RMSD
                _, aligned_ref = kabsch_align(ref_cg_sub, tgt_cg_sub)
                rmsd = np.sqrt(np.mean((tgt_cg_sub - aligned_ref)**2))
                rmsd_values.append(rmsd)
            
            backmapped_all.append(sub_backmapped)
        
        # Write output
        backmapped_all = np.vstack(backmapped_all)
        
        # Create full atom metadata for all molecules
        full_metadata = ref_aa_metadata * cg_num_mols
        
        # Determine output filename
        if len(frames) == 1:
            output_file = f"{args.output}.gro"
        else:
            output_file = f"{args.output}_frame_{frame_id:04d}.gro"
            
        write_gro(output_file, backmapped_all, current_box, full_metadata,
                  title=f"Backmapped frame {frame_id}")
        
        if (frame_id + 1) % 10 == 0 or frame_id == len(frames) - 1:
            print(f"  Processed {frame_id + 1}/{len(frames)} frames...")
    
    print()
    print("=" * 60)
    print("BACKMAPPING COMPLETE")
    print("=" * 60)
    
    if len(frames) == 1:
        print(f"Output file: {args.output}.gro")
    else:
        print(f"Output files: {args.output}_frame_XXXX.gro")
        
    print(f"Mean RMSD: {np.mean(rmsd_values):.4f} nm")
    print(f"Max RMSD:  {np.max(rmsd_values):.4f} nm")
    print(f"Min RMSD:  {np.min(rmsd_values):.4f} nm")
    print()


if __name__ == "__main__":
    main()
