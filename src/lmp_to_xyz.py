import sys
import helpers
from math import floor


def lmp_to_xyzf(units, trjfile, logfile):  # , argv):
    """
    Units are either: "REAL" or "METAL" -- Ancillary support for units metal

    Expects the following custom format: ATOMS id type element xu yu zu <anything else>
    Prints only coordinates, and forces IF line has fx fy fz entries...
    Converts from REAL or METAL units to chimes_lsq and chimes_md units

    WARNING: Assumes thermo and dump output frequency are the same
    WARNING: Assumes thermo style has first X columns:
             step time ke pe etotal temp press pxx pyy pzz pxy pxz pyz vol c_ke_tensor[1] c_ke_tensor[2] c_ke_tensor[3] c_ke_tensor[4] c_ke_tensor[5] c_ke_tensor[6]
             ... note c_ke_tensor is created via compute ke_tensor all temp
    WARNING: Assumes dump style contains at least: "element", "xu", "yu", "zu", "fx", "fy", "fz"
    WARNING: Assumes (and expects) an orthorhombic box
    WARNING: Optional frame skip. no longer supported - would be specified as an optional additional arg:
             <optional: frame skip>

    Takes about 1 minute per 1000 frames for 12500 atoms
    """

    natoms = int(helpers.head(trjfile, 4)[-1])
    outfile = trjfile + ".xyzf"
    ofstream = open(outfile, "w")

    skip = 1

    # No longer supporting frame skipping ... can figure out how to add this back in in an al_driver compatible manner latter
    # if len(sys.argv) == 5:
    # 	SKIP = int(sys.argv[4])

    print("\tProcessing files:         ")
    print("\t    trjfile:              " + trjfile)
    print("\t    logfile:              " + logfile)
    print("\tWriting output to:        " + outfile)
    print("\tWill use units:           " + units)
    print("\tCounted atoms:            " + str(natoms))

    # Specify conversion factors to get things in ChIMES xyzf file units:

    econv  = 1.0  # For lammps units real (kcal/mol) to kcal/mol
    fconv  = 1.0 / 1.88973 / 627.509551  # For lammps units real (Kcal/mol/Ang) to H/Bohr
    sconv  = 0.000101325  # From lammps units real (atm) to GPa
    gascon = 8.31446261815324  # m^3 Pa / K / mol
    mole   = 6.02e23

    if units == "METAL":

        print("WARNING: Metal units functionality untested - check your results carefully and report back!")

        econv = 1.0 / 27.211399  # For lammps units metal (eV) to kcal/mol
        fconv = 1.0 / 1.88973 / 27.211399  # For lammps units metal (eV/Ang) to H/Bohr
        sconv = 0.0001  # For lammps units metal (bar) to GPa

    # Count the number of stats lines in the log file - this should match the number of frames in the traj file

    stats_start = int(helpers.getlineno("Step", logfile)[-1]) + 1  # Index of first thermo output line
    stats_end   = None
    try:
        stats_end = int(helpers.getlineno("Loop", logfile)[-1]) - 1  # Index of last thermo output line
    except:
        try:
            stats_end = int(helpers.getlineno("ERROR", logfile)[-1]) - 1  # Index of last thermo output line
        except:
            stats_end = int(helpers.wc_l(logfile))  # Index of last thermo output line
    nstat_lines = stats_end - stats_start + 1

    # Count the number of frames in the lammps file

    frames = int(helpers.wc_l(trjfile) / (natoms + 9))

    # Check that the number of lines/frames match

    if frames != nstat_lines:
        print("Warning: Number of frames and number of stats lines in log.lammps do not match!")
        print("Frames:", frames)
        print("Stats: ", nstat_lines)
        print("Taking smaller of the two.")
        if frames < nstat_lines:
            nstat_lines = frames
        else:
            frames = nstat_lines
    else:
        print("\tCounted frames:           " + str(frames))
        print("\tPrinting every nth frame: " + str(skip))

    # Grab the energy and stress data from the logfile

    stats = helpers.head(logfile, stats_end + 1)[-nstat_lines:]

    energy  = []
    stensor = []

    for i in range(len(stats)):

        line = stats[i].split()

        energy.append(line[3])  # Potential energy
        ptensor = line[7:13]  # Pressure tensor, not yet stress tensor!
        ttensor = line[14:20]  # Temperature tensor, needed to compute the stress tensor
        vol = line[13]

        # Handle energy

        energy[-1] = str(float(energy[-1]) * econv)

        # Handle stress

        for j in range(6):

            ptensor[j]  = float(ptensor[j]) * sconv  # Convert to  GPa

            ttensor[j]  = float(ttensor[j])
            ttensor[j]  = (3 / 2 * gascon / mole * ttensor[j])  # Convert ttensor to KE (units: J)
            ttensor[j] /= (float(vol) / 1e30) * 1e-9  # Convert KE to kinetic (IG) pressure (units: GPa)
            ttensor[j]  = (ptensor[j] - ttensor[j])  # Convert IG pressure to cold (Virial) pressure (units: GPa)

        stensor.append([str(x) for x in ttensor])

    # Process the file

    ifstream = open(trjfile, "r")

    printed = 0

    for i in range(frames):

        if (i + 1) % skip == 0:
            ofstream.write(str(natoms) + "\n")
            printed += 1

        # Ignore un-neded headers

        ifstream.readline()  # ITEM: TIMESTEP
        ifstream.readline()  # <timestep>
        ifstream.readline()  # ITEM: NUMBER OF ATOMS
        ifstream.readline()  # <atoms>
        ifstream.readline()  # ITEM: BOX BOUNDS xy xz yz pp pp pp

        # Save/print the box lengths

        tmp_lx = ifstream.readline().split()
        tmp_ly = ifstream.readline().split()
        tmp_lz = ifstream.readline().split()


        # Determine if we're working with an orthorhombic or non-orthrhombic box

        if len(tmp_lx) == 3: # Then its non-orthorhombic
          
            if (i + 1) % skip == 0:
                ofstream.write("NON_ORTHO" + " " + ' '.join(tmp_lx) + " " + ' '.join(tmp_ly) + " " + ' '.join(tmp_lz))
                           
        elif len(tmp_lx) == 2: # Then orthorhombic

            lx = str(float(tmp_lx[1]) - float(tmp_lx[0]))
            ly = str(float(tmp_ly[1]) - float(tmp_ly[0]))
            lz = str(float(tmp_lz[1]) - float(tmp_lz[0]))

            if (i + 1) % skip == 0:
                ofstream.write(lx + " " + ly + " " + lz + "\n")
        else:
            print("ERROR: Unrecognized box dimension style in lammps traj file")
            exit(0)

        line = ifstream.readline()  # ITEM: ATOMS id type element xu yu zu
        line = line.split()

        keys = ["element", "xu", "yu", "zu", "fx", "fy", "fz"]
        locs = [None] * len(keys)

        for j in range(len(keys)):

            try:
                locs[j] = line.index(keys[j]) - 2
            except:
                locs[j] = -1
                # print "Warning: Property keys",keys[j],"not found ... ignoring"

        print_f = True

        if locs[0] == -1:
            print("Error: id missing from file")
            exit()

        if (locs[1] == -1) or (locs[2] == -1) or (locs[3] == -1):
            print("Error: xu, yu, or zu missing from file")
            exit()

        if (locs[4] == -1) or (locs[5] == -1) or (locs[6] == -1):
            if print_f and (i == 0):
                print("Warning: fx, fy, or fz missing from file")
            print_f = False

            if i == 0:
                print("Will not print forces")

        # Write the coordinates

        for j in range(natoms):

            line = ifstream.readline().split()

            if (i + 1) % skip == 0:

                tmp = (
                    line[locs[0]]
                    + " "
                    + line[locs[1]]
                    + " "
                    + line[locs[2]]
                    + " "
                    + line[locs[3]]
                )

                if print_f:
                    tmp += (
                        " "
                        + str(float(line[locs[4]]) * fconv)
                        + " "
                        + str(float(line[locs[5]]) * fconv)
                        + " "
                        + str(float(line[locs[6]]) * fconv)
                    )

                ofstream.write(tmp + "\n")

    ofstream.close()
    ifstream.close()

    print("Printed frames:           ", printed)


if __name__ == "__main__":

    import sys

    # Called with lmp_to_xyzf(units, trjfile, logfile

    lmp_to_xyzf(*sys.argv[1:])
