# Kabsch-Back Backmapping Tool
Tool used to convert coarse-grained (CG) molecular dynamics trajectories back to all-atom (AA) resolution for rigid and semi rigid molecules

# Authors
- Pratyush Dhal
- Ronald Larson
- Rebecca Lindsey

## Requirements

- Python 3.x
- NumPy

```bash
pip install numpy
```

## Quick Start

```bash
python3 kabsch_back.py -ref_cg cg.gro -ref_aa aa.gro -traj cg_traj.gro -ndx index.ndx -o backmapped > backmap.log
```

## Command-Line Arguments

```
Required arguments:
  -ref_cg FILE      Reference CG structure (.gro file)
  -ref_aa FILE      Reference all-atom structure (.gro file)
  -ndx FILE         Mapping index file (.ndx)
  -o PREFIX         Output file prefix (without .gro extension)

Optional arguments:
  -traj FILE        CG trajectory to backmap (.gro, multi-frame)
                    If not provided, uses -ref_cg as single frame
  -ref_mol ID       Reference molecule ID (0-indexed, default: 0)
  -h, --help        Show help message
```

## Input Files Required

All files must be in GROMACS .gro format:

1. **Reference CG structure** - A single-frame CG structure (typically the starting structure)
2. **Reference AA structure** - The corresponding all-atom structure for the reference
3. **CG trajectory** (optional) - The coarse-grained trajectory to backmap (can be multi-frame)
4. **Mapping index file (.ndx)** - Defines how CG beads map to AA atoms

## Index File Format

The `.ndx` file must contain two sections:

```
[CG sub groups]
0 1 2 3
4 5 6
7 8 9

[AA sub groups]
0 1 2 3 4 5 6 19 20
7 8 9 10 11 12 21 22 23 24 25
13 14 15 16 17 18 26 27 28 29 30
```

- Each line is one mapping group
- Number of CG groups must equal number of AA groups
- Indices are 0-based (atom numbering starts at 0)
- Comments start with `;`

### When There Are No Sub-groups

For simple molecules like naphthalene where the entire molecule is treated as one rigid unit, put all atom indices on a single line:

```
[CG sub groups]
0 1 2 3 4 5 6 7 8 9

[AA sub groups]
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
```

This treats the entire molecule as one mapping group - all CG beads align to all AA atoms together.

## Usage Examples

### Example 1: Backmap a trajectory

```bash
python3 kabsch_back.py -ref_cg ref_cg.gro -ref_aa ref_aa.gro \
                       -traj trajectory.gro -ndx mapping.ndx \
                       -o backmapped
```

Output: `backmapped_frame_0000.gro`, `backmapped_frame_0001.gro`, etc.

### Example 2: Backmap single frame

```bash
python3 kabsch_back.py -ref_cg cg.gro -ref_aa aa.gro \
                       -ndx mapping.ndx -o output
```

Output: `output.gro`

### Example 3: Use specific reference molecule

```bash
python3 kabsch_back.py -ref_cg ref_cg.gro -ref_aa ref_aa.gro \
                       -traj traj.gro -ndx mapping.ndx \
                       -o backmapped -ref_mol 26
```

Uses molecule 26 (0-indexed) as the reference template.

## How It Works

The script automatically detects:
- Number of atoms/beads per molecule
- Number of molecules in the system
- Number of frames in trajectory

**Algorithm:**
1. Read mapping scheme from .ndx file
2. Load reference structures (CG and AA)
3. For each frame and molecule:
   - For each mapping group:
     - Align reference CG to target CG (Kabsch algorithm)
     - Apply same rotation to reference AA atoms
     - Reconstruct backmapped AA structure
4. Write output with original box vectors and atom names

## Output

- **Single frame**: `{prefix}.gro`
- **Multiple frames**: `{prefix}_frame_0000.gro`, `{prefix}_frame_0001.gro`, etc.

Statistics printed to console:
- Mean RMSD (alignment quality)
- Max/Min RMSD values
- Number of frames processed
- Note: RMSD values calculated here are in comparison to reference system coordinates. Use of a different state/system for the same species will yield high RMSD values. This feature is majorly to validate the algorithm efficiency with respect to a known AA trajectory i.e the case where -traj has no input parameter
## Algorithm Details

Uses SVD-based Kabsch algorithm for optimal rigid-body alignment:
- Computes optimal rotation matrix between CG structures
- Applies rotation to corresponding AA atoms
- Preserves molecular geometry from reference structure
- Maintains original atom names, residue names, and residue numbers

## Tips

- **Reference molecule ID**: Choose a well-equilibrated molecule from your reference structures (often middle of the system to avoid edge effects). Make sure you have a whole molecule i.e unwrapped coordiantes.
- **Mapping groups**: Divide molecules into rigid or semi-rigid regions for best results
- **Single group vs multiple groups**: For rigid molecules (like naphthalene), use one group. For semi-rigid molecules (like phenytoin), divide into sub-groups that are rigid (Eg:rings).
- **Auto-detection**: All system parameters (atoms per molecule, number of molecules, frames) are read automatically from files

## Troubleshooting

**Error: "Number of CG groups must match AA groups"**
- Ensure your .ndx file has the same number of lines in both sections

**Error: "Reference molecule X out of range"**
- Check that your -ref_mol value is less than the number of molecules in the system
- Remember: molecule IDs are 0-indexed (first molecule is 0, not 1)

**Error: "index X is out of bounds"**
- Check your .ndx file - make sure all atom indices exist in your molecules
- Verify indices are 0-based (first atom is 0, not 1)
- Check that CG indices match your CG molecule and AA indices match your AA molecule

**Poor RMSD values**
- Check your mapping scheme in the .ndx file
- Verify reference molecule ID points to a representative molecule
- Ensure CG and AA reference structures are properly aligned
