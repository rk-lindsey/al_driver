# Global (python) modules

import glob # Warning: glob is unserted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os
import math

# Local modules

import helpers
import cluster


def parse_inner_cutoffs(paramsfile):

    """ 
    
    Parses per-pair inner cutoffs (S_MINIM) and the penalty kick-in distance
    from a ChIMES params.txt.reduced file.
    
    Usage: rin, dp = parse_inner_cutoffs("params.txt.reduced")
    
    Notes: rin is a dictionary keyed by a frozenset of the two atom-type
           symbols, i.e. rin[frozenset(("C","N"))] = 0.9.
           Inner cutoffs are read from the lines following the "# PAIRIDX #"
           header: fields 1 and 2 are the atom types, field 3 is S_MINIM.
           dp is read from the "PAIR CHEBYSHEV PENALTY DIST:" line.
           
    """
    
    ifstream = open(paramsfile,'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    rin = {}
    dp  = None
    
    # Grab the per-pair inner cutoffs
    
    for i in range(len(contents)):
    
        if "ATOM PAIRS:" in contents[i]:
        
            npairs = int(contents[i].split()[-1])
            
            # Find the "# PAIRIDX #" header, then read the npairs lines below it
            
            for k in range(i+1, len(contents)):
            
                if "PAIRIDX" in contents[k]:
                
                    for j in range(k+1, k+1+npairs):
                    
                        line = contents[j].split()
                        
                        ty1 = line[1]
                        ty2 = line[2]
                        val = float(line[3])
                        
                        rin[frozenset((ty1,ty2))] = val
                        
                    break
                
        if "PAIR CHEBYSHEV PENALTY DIST:" in contents[i]:
        
            dp = float(contents[i].split()[-1])
            
    if dp is None:
        print("WARNING: Could not find PAIR CHEBYSHEV PENALTY DIST in", paramsfile)
        print("         Setting to default value of 0.01")
        dp = 0.01
        
    if len(rin) == 0:
        print("ERROR: Could not find any ATOM PAIRS inner cutoffs in", paramsfile)
        exit()
        
    return rin, dp


def mat_inverse_3x3(m):

    """ 
    
    Inverse of a 3x3 matrix given as three row vectors [m0, m1, m2].
    
    Usage: minv = mat_inverse_3x3([row0, row1, row2])
    
    Notes: Hand-rolled cofactor inverse to avoid a numpy dependency,
           matching the repo's dependency-light style. Returns the
           inverse as three row vectors.
              
    """
    
    a,b,c = m[0]
    d,e,f = m[1]
    g,h,i = m[2]
    
    det = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    
    if abs(det) < 1.0e-12:
        print("ERROR: Singular cell matrix in mat_inverse_3x3")
        exit()
        
    inv = [[ (e*i - f*h)/det, (c*h - b*i)/det, (b*f - c*e)/det],
           [ (f*g - d*i)/det, (a*i - c*g)/det, (c*d - a*f)/det],
           [ (d*h - e*g)/det, (b*g - a*h)/det, (a*e - b*d)/det]]
           
    return inv


def wrap_into_cell(coords, a, b, c):

    """ 
    
    Wraps every atom into the primary cell [0,1) in fractional space.
    
    Usage: wrapped = wrap_into_cell(coords, a, b, c)
    
    Notes: DFTB+ trajectories do not guarantee wrapped coordinates (atoms
           diffuse out of the box and are reported unwrapped). The ghost
           method assumes atoms live in the primary cell, so this must be
           applied before build_ghosts.
           
           The lattice matrix has the cell vectors as ROWS, so a Cartesian
           position r maps to fractional s via s = r . H^{-1}, and back via
           r = s . H.
              
    """
    
    H    = [a, b, c]
    Hinv = mat_inverse_3x3(H)
    
    wrapped = []
    
    for r in coords:
    
        # Cartesian -> fractional: s_j = sum_k r_k * Hinv[k][j]
        
        s = [ r[0]*Hinv[0][j] + r[1]*Hinv[1][j] + r[2]*Hinv[2][j] for j in range(3) ]
        
        # Wrap into [0,1)
        
        s = [ si - math.floor(si) for si in s ]
        
        # Fractional -> Cartesian: r_k = sum_j s_j * H[j][k]
        
        rw = [ s[0]*H[0][k] + s[1]*H[1][k] + s[2]*H[2][k] for k in range(3) ]
        
        wrapped.append(rw)
        
    return wrapped


def cross(u, v):

    """ Cross product of two length-3 vectors. """
    
    return [u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]]


def norm(u):

    """ Euclidean norm of a length-3 vector. """
    
    return math.sqrt(u[0]*u[0] + u[1]*u[1] + u[2]*u[2])


def replicate_counts(a, b, c, rcut):

    """ 
    
    Determines how many cell-shells are needed along each lattice
    direction so that every periodic image within rcut of the primary
    cell is captured by an explicit replica.
    
    Usage: na, nb, nc = replicate_counts(a, b, c, rcut)
    
    Notes: The controlling quantity is the interplanar spacing (the
           perpendicular distance between opposing cell faces), NOT the
           lattice-vector length. For a sheared cell a vector can be long
           while the cell is thin perpendicular to the opposing face, so
           |a| would under-count shells. The perpendicular widths are:
           
               d_a = V / |b x c|,  d_b = V / |c x a|,  d_c = V / |a x b|
           
           where V is the cell volume. n_dir = ceil(rcut / d_dir).
              
    """
    
    bxc = cross(b,c)
    cxa = cross(c,a)
    axb = cross(a,b)
    
    vol = abs(a[0]*bxc[0] + a[1]*bxc[1] + a[2]*bxc[2])
    
    d_a = vol / norm(bxc)
    d_b = vol / norm(cxa)
    d_c = vol / norm(axb)
    
    na = int(math.ceil(rcut / d_a))
    nb = int(math.ceil(rcut / d_b))
    nc = int(math.ceil(rcut / d_c))
    
    return na, nb, nc


def build_ghosts(symbols, coords, a, b, c, rcut):

    """ 
    
    Builds the periodic ghost-atom set: every atom replicated into the
    surrounding cells out to the shell count needed for rcut.
    
    Usage: g_syms, g_crds, g_shift = build_ghosts(symbols, coords, a, b, c, rcut)
    
    Notes: Returns parallel lists. g_shift[k] is the (na,nb,nc) cell shift
           and the original atom index for ghost k, as a tuple
           (na, nb, nc, orig_idx). This lets the caller skip the
           self-image term (same atom, (0,0,0) shift) while still
           allowing an atom to contact its OWN images in adjacent cells.
              
    """
    
    na, nb, nc = replicate_counts(a, b, c, rcut)
    
    g_syms  = []
    g_crds  = []
    g_shift = []
    
    for ia in range(-na, na+1):
        for ib in range(-nb, nb+1):
            for ic in range(-nc, nc+1):
            
                ox = ia*a[0] + ib*b[0] + ic*c[0]
                oy = ia*a[1] + ib*b[1] + ic*c[1]
                oz = ia*a[2] + ib*b[2] + ic*c[2]
                
                for k in range(len(coords)):
                
                    g_syms.append(symbols[k])
                    g_crds.append([coords[k][0]+ox, coords[k][1]+oy, coords[k][2]+oz])
                    g_shift.append((ia, ib, ic, k))
                    
    return g_syms, g_crds, g_shift


def classify_frame(symbols, coords, a, b, c, rin, dp):

    """ 
    
    Classifies a single frame by its worst (closest) interatomic contact,
    using explicit periodic ghost atoms (no minimum-image convention).
    
    Usage: badness = classify_frame(symbols, coords, a, b, c, rin, dp)
    
    Notes: symbols is a list of atom-type symbols (length natoms).
           coords is a list of [x,y,z] (length natoms).
           Returns:
              2 if any pair distance <  rin              (r.lt.rin)
              1 if any pair distance <  rin+dp           (r.lt.rin+dp)
              0 otherwise                                (r.ge.rin+dp)
           Pairs with no inner cutoff in rin are skipped.
           
           Each primary atom is checked against the full ghost set. The
           only excluded term is an atom paired with its own (0,0,0)
           image (i.e. itself); an atom CAN contact its own image in an
           adjacent cell, which matters at high density / small cells.
              
    """
    
    natoms  = len(coords)
    badness = 0
    
    # Wrap atoms into the primary cell; DFTB trajectories may be unwrapped
    
    coords = wrap_into_cell(coords, a, b, c)
    
    # The largest distance we care about sets the ghost-shell extent
    
    rcut = max(rin.values()) + dp
    
    g_syms, g_crds, g_shift = build_ghosts(symbols, coords, a, b, c, rcut)
    
    for i in range(natoms):
        for k in range(len(g_crds)):
        
            # Skip the self term: same atom, central (0,0,0) image
            
            if (g_shift[k][3] == i) and (g_shift[k][0] == 0) and (g_shift[k][1] == 0) and (g_shift[k][2] == 0):
                continue
                
            key = frozenset((symbols[i], g_syms[k]))
            
            if key not in rin:
                continue
                
            this_rin = rin[key]
            
            dx = coords[i][0] - g_crds[k][0]
            dy = coords[i][1] - g_crds[k][1]
            dz = coords[i][2] - g_crds[k][2]
            
            d = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if d < this_rin:
                return 2 # Worst possible - no need to keep checking
            elif d < this_rin + dp:
                badness = 1
                
    return badness


def read_input_cell(input_gen):

    """ 
    
    Reads the (fixed) cell from a single-frame DFTB+ .gen structure file.
    
    Usage: a, b, c = read_input_cell("case-0.indep-0.gen")
    
    Notes: Used for constant-volume (NVE/NVT) runs, where the cell does
           not change and DFTB+ does not write it to the trajectory. The
           lattice block is the last three lines of the .gen (the origin
           line precedes them).
              
    """
    
    ifstream = open(input_gen,'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    a = [float(x) for x in contents[-3].split()]
    b = [float(x) for x in contents[-2].split()]
    c = [float(x) for x in contents[-1].split()]
    
    return a, b, c


def parse_mdout_cells(mdout):

    """ 
    
    Parses per-step lattice vectors from a DFTB+ md.out file.
    
    Usage: cells = parse_mdout_cells("md.out")
    
    Notes: For a barostatted (NPT/NPH) run, each MD step block in md.out
           contains a "Lattice vectors (A)" header followed by three lines
           giving the a, b, c cell vectors (Cartesian, Angstrom). For a
           fixed-cell run the header is absent.
           
           Returns a list of (a, b, c) tuples, one per logged step, in
           order. An empty list means no lattice was found (i.e. not a
           barostatted run).
              
    """
    
    ifstream = open(mdout,'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    cells = []
    
    for i in range(len(contents)):
    
        if "Lattice vectors (A)" in contents[i]:
        
            if i+3 >= len(contents):
                # Truncated md.out (e.g. killed run); stop at the last complete block
                break
                
            a = [float(x) for x in contents[i+1].split()]
            b = [float(x) for x in contents[i+2].split()]
            c = [float(x) for x in contents[i+3].split()]
            
            cells.append((a, b, c))
            
    return cells


def detect_barostat(hsdfile):

    """ 
    
    Determines whether an MD run is barostatted (NPT/NPH) by inspecting
    the parsed DFTB+ input.
    
    Usage: is_npt = detect_barostat("dftb_pin.hsd")
    
    Notes: The authoritative signal is a "Barostat" block inside the
           VelocityVerlet driver. dftb_pin.hsd is preferred (it is the
           post-parse input with all defaults resolved). Returns True if a
           Barostat block is present, False otherwise. If the file does
           not exist, returns None (unknown) so the caller can decide.
              
    """
    
    if not os.path.isfile(hsdfile):
        return None
        
    ifstream = open(hsdfile,'r')
    contents = ifstream.read()
    ifstream.close()
    
    # A Barostat block looks like "Barostat = ..." or "Barostat {"
    
    for line in contents.split('\n'):
    
        stripped = line.strip()
        
        if stripped.startswith("Barostat") and (("=" in stripped) or ("{" in stripped)):
            return True
            
    return False


def resolve_cells(input_gen, nframes, mdout="md.out", hsd="dftb_pin.hsd"):

    """ 
    
    Determines the per-frame cell source for the trajectory, detecting the
    ensemble authoritatively from the input and validating it against the
    output.
    
    Usage: cells = resolve_cells("case-0.indep-0.gen", nframes)
    
    Notes: Detection logic, in order of authority:
    
           1. Ensemble is determined from the input (dftb_pin.hsd, else
              dftb_in.hsd): a Barostat block => NPT, otherwise NVT/NVE.
              
           2. NPT: the per-step lattice MUST be present in md.out. The
              number of lattice entries must equal the number of frames.
              A missing lattice stream or a count mismatch is a hard error
              (a barostatted run misread as fixed-cell would silently
              corrupt every distance).
              
           3. NVT/NVE: the fixed input cell is read once from the input
              .gen and replicated. If md.out unexpectedly contains lattice
              entries, that contradiction is warned about (but the input
              ensemble is trusted).
              
           4. If the input files are missing so the ensemble cannot be
              determined, fall back to md.out content: lattice present =>
              NPT, absent => NVT. This preserves function without the
              parsed input, but is the last resort.
              
    """
    
    # 1. Authoritative ensemble detection from the input
    
    is_npt = detect_barostat(hsd)
    
    if is_npt is None:
        is_npt = detect_barostat("dftb_in.hsd")
        
    # 4. Last resort: infer from md.out content if input is unavailable
    
    if is_npt is None:
    
        print("WARNING: could not find", hsd, "or dftb_in.hsd to determine ensemble.")
        print("         Falling back to md.out content for NPT/NVT detection.")
        
        probe = []
        if os.path.isfile(mdout):
            probe = parse_mdout_cells(mdout)
            
        is_npt = (len(probe) > 0)
        
    # 2. NPT: require and validate the md.out lattice stream
    
    if is_npt:
    
        print("Detected NPT/NPH run (Barostat in input); reading time-varying cells from", mdout)
        
        if not os.path.isfile(mdout):
            print("ERROR: in resolve_cells, run is NPT but", mdout, "is missing.")
            print("       Cannot recover the time-varying cell. Exiting.")
            exit()
            
        cells = parse_mdout_cells(mdout)
        
        if len(cells) == 0:
            print("ERROR: in resolve_cells, run is NPT but no 'Lattice vectors (A)'")
            print("       blocks were found in", mdout + ". Exiting.")
            exit()
            
        if len(cells) != nframes:
            print("ERROR: in resolve_cells, number of md.out lattice entries (" + str(len(cells)) + ")")
            print("       does not match number of trajectory frames (" + str(nframes) + ").")
            print("       Cannot safely pair cells with coordinates. Exiting.")
            exit()
            
        return cells
        
    # 3. NVT/NVE: fixed input cell, replicated
    
    print("Detected constant-volume run (no Barostat); using fixed input cell from", input_gen)
    
    if os.path.isfile(mdout):
    
        probe = parse_mdout_cells(mdout)
        
        if len(probe) > 0:
            print("WARNING: input indicates NVT/NVE but", mdout, "contains lattice entries.")
            print("         Trusting the input ensemble and using the fixed input cell.")
            
    a, b, c = read_input_cell(input_gen)
    
    return [(a, b, c)] * nframes


def generate_trajbads(*argv, **kwargs):

    """ 
    
    Generates the standard ChIMES_MD traj_bad.*.xyz files from a DFTB+
    MD run, by post-processing the trajectory.
    
    Usage: generate_trajbads("geo_end.xyz", "case-0.indep-0.gen",
                             "params.txt.reduced")
           generate_trajbads("geo_end.xyz", "case-0.indep-0.gen",
                             "params.txt.reduced", mdout="md.out")
    
    Notes: DFTB+ does not create these files natively, so they are built
           here from the trajectory itself.
           
           The trajectory (geo_end.xyz, set by OutputPrefix in
           dftb_in.hsd) is plain XYZ and does NOT carry the cell. The cell
           is resolved by resolve_cells:
              - barostatted (NPT) run: per-step lattice read from md.out
              - constant-volume run:  fixed cell from the input .gen
           
           Generates (all in NON_ORTHO ChIMES .xyz format):
           
           - traj_bad_r.ge.rin+dp_dftbfrq.xyz   (badness 0)
           - traj_bad_r.lt.rin+dp.xyz           (badness 1)
           - traj_bad_r.lt.rin.xyz              (badness 2)
           
           The "dftbfrq" tag is historical; for DFTB all three files share
           the same output frequency (the MDRestartFrequency set in
           dftb_in.hsd), unlike ChIMES MD.
           
           Inner cutoffs (per pair) and the penalty distance are read from
           the params file via parse_inner_cutoffs.
              
    """
    
    INFILE   = argv[0] # geo_end.xyz trajectory
    INPUTGEN = argv[1] # input .gen (cell source for constant-volume runs)
    PARAMS   = argv[2] # params.txt.reduced
    
    mdout = "md.out"
    if "mdout" in kwargs:
        mdout = kwargs["mdout"]
    
    # Grab the inner cutoffs and penalty distance
    
    rin, dp = parse_inner_cutoffs(PARAMS)
    
    # How many frames are there? ... let the helper figure it out
    
    FRAMES = helpers.count_xyzframes_general(INFILE)
    
    # Resolve the per-frame cells (NPT from md.out, else fixed input cell)
    
    cells = resolve_cells(INPUTGEN, FRAMES, mdout=mdout)
    
    IFSTREAM = open(INFILE,"r")
    
    # Create the three output files
    
    BAD0 = open("traj_bad_r.ge.rin+dp_dftbfrq.xyz","w") # badness 0
    BAD1 = open("traj_bad_r.lt.rin+dp.xyz",        "w") # badness 1
    BAD2 = open("traj_bad_r.lt.rin.xyz",           "w") # badness 2
    
    for i in range(FRAMES):
    
        # Read the first line to get the number of atoms in the frame
        
        ATOMS = IFSTREAM.readline()
        ATOMS = int(ATOMS.split()[0])
        
        # Skip the comment line (DFTB+ writes step/energy info here)
        
        IFSTREAM.readline()
        
        # Read the atom lines (XYZ: symbol x y z [extra columns])
        
        FRAME_SYMS  = []
        FRAME_CRDS  = []
        FRAME_LINES = []
        
        for j in range(ATOMS):
        
            LINE = IFSTREAM.readline().split()
            
            sym = LINE[0]
            crd = [float(LINE[1]), float(LINE[2]), float(LINE[3])]
            
            FRAME_SYMS.append(sym)
            FRAME_CRDS.append(crd)
            FRAME_LINES.append(sym + " " + ' '.join(LINE[1:4]))
            
        # Cell for this frame
        
        a, b, c = cells[i]
        
        # Classify the frame
        
        badness = classify_frame(FRAME_SYMS, FRAME_CRDS, a, b, c, rin, dp)
        
        # Route to the correct file
        
        if   badness == 2:
            OFSTREAM = BAD2
        elif badness == 1:
            OFSTREAM = BAD1
        else:
            OFSTREAM = BAD0
            
        # Write the frame in NON_ORTHO ChIMES .xyz format
        
        OFSTREAM.write(repr(ATOMS) + '\n')
        
        OFSTREAM.write("NON_ORTHO " + \
            ' '.join(map(str, a)) + " " + \
            ' '.join(map(str, b)) + " " + \
            ' '.join(map(str, c)) + '\n')
            
        for j in range(ATOMS):
            OFSTREAM.write(FRAME_LINES[j] + '\n')
            
    IFSTREAM.close()
    
    BAD0.close()
    BAD1.close()
    BAD2.close()
    
    return
