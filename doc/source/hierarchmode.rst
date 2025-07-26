.. _page-hierarch:

***************************************
Hierarchical Fitting Mode
***************************************

.. figure:: hierarchy.pdf
  :width: 500
  :align: center

  **Fig. 1:** The ChIMES parameter hierarchy for a Si, O, H, and N-containing system.


Machine-learned interatomic models offer near quantum-accurate predictions for complex phenomena with orders-of-magnitude greater computational efficiency. However, they often struggle when applied to systems containing many element types, due to the near-exponential growth in the number of parameters required as the number of elements increases. However, the inherent nature of ChIMES parameters allows for **hierarchical fitting strategy**, where parameters are grouped into "families" that can be learned **independently** and then **combined** to model multi-element complex systems.

For example, Fig. 1 shows the ChIMES parameter hierarchy for an up-to-4-body model describing interactions in a Si, O, H, and N-containing system. Each "tile" represents a family of parametrs, e.g., the H tile contains the 1-through 4-body parameters for H, HH, HHH, and HHHH interactions. Tiles on the same row (e.g. H and N) can be fit indepent of one another; tiles containing two or more atoms describe *only* simultaneous cross-interactions between the indicated atom types, e.g., the HN tile *only* contains parameters for HN, HHN, HNN, HHHN, HHNN, and HNNN interactions. Practically, this means simulating an H- and N- containing system requires all the parameters contained in the H, N, and HN tiles. 

Fitting row-1 tiles requires no special treatment. However, fitting tiles on row-2 and above requires pre-processing training data during each learning iteration to remove contributions from the relavant lower row tiles. For example, an HN tile fit would require H and N tile contributions to be removed from the training data. Additionally, parameter sets must be combined into a cohesive file before running dynamics. *The ALD can perform these tasks automatically.*

This section provides an overview of how to configure the ALD for a hierarchical fitting strategy, within the context of a liquid C/N system. Before proceding, ensure you have read through and fully understand the :ref:`page-basic`.

=================================
Why Use Hierarchical Fitting?
=================================
1. **Scalability** – Easier optimization of smaller parameter subsets.
2. **Transferability** – Enables reuse of parameters across systems.
3. **Interpretability** – Clear attribution of interactions to specific atom types or combinations.

===========================================
Full vs Partial Hierarchical Fitting
===========================================
ChIMES supports two hierarchical strategies:

**Full Hierarchical Fitting**

In this mode, you explicitly provide previously learned parameter files for **all monatomic species** (e.g., ``C.params.txt``, ``N.params.txt``). The system learns only the **cross-interactions**, building on a robust foundation of species-specific parameters.

Requirements:

1. All relevant parameter files must be specified via ``HIERARCH_PARAM_FILES``.
2. The training data must be preprocessed to subtract contributions from the specified parameters.


Use when:

1. You have confidence in existing atomic models.
2. You want to learn only new interactions (e.g., mixing terms).

**Partial Hierarchical Fitting**

In this mode, you specify parameter files for **some** species (e.g., only `C.params.txt`). The system will use the provided parameters as fixed and then fit both the missing species (e.g., `N`) and all relevant cross-interactions.

Use when:

1. You only want to transfer part of the model.
2. You want to let the system learn remaining interactions on its own.

**Important**

- In both modes, consistency between the training system and provided parameter files is essential (e.g., same order, cutoffs, `TYPEIDX`).

For additional information on strategies and benefits of hierarchical fitting, see: 

* R. K. Lindsey*, A. D. Oladipupo, S. Bastea, B. A. Steele, F. W. Kuo, N. Goldman. Hierarchical Transfer Learning: An Agile and Equitable Strategy for Machine-Learning Interatomic Models Under Review: npj Comput. Mater. (2025)
-------
====================================================
Example: Hierarchical Fit for Solid C/N System
====================================================

.. Note::

    Files for this example are located in:
    ``./<al_driver base folder>/examples/hierarch_fit``

This example demonstrates a 3-iteration hierarchical fit for a solid carbon-nitrogen (C/N) system (approx. 75% C, 6000 K, 3.5 g/cc) using up-to-4-body interactions. The setup mirrors the structure described in the :ref:`page-basic` but introduces the hierarchical mechanism.Given the substantial increase in number of fitting parameters and system complexity relative to pure carbon case the basic fitting example, this case will take substantially longer to run.The neccesary input files and directory tree structure are provided in the example folder, i.e.:

**Directory Structure**

.. code-block:: bash
    :emphasize-lines: 4,14-16

    $ tree
    .
    ├── ALC-0_BASEFILES
    │   ├── 20.3percN_3.5gcc.temps
    │   ├── 20.3percN_3.5gcc.xyzf
    │   ├── fm_setup.in
    │   └── traj_list.dat
    ├── CHIMESMD_BASEFILES
    │   ├── base.run_md.in
    │   ├── bonds.dat
    │   ├── case-0.indep-0.input.xyz
    │   ├── case-0.indep-0.run_md.in
    │   └── run_molanal.sh
    ├── HIERARCH_PARAMS
    │   ├── C.params.txt.reduced
    │   └── N.params.txt.reduced
    └── QM_BASEFILES
        ├── 6000.INCAR
        ├── C.POTCAR
        ├── N.POTCAR
        ├── KPOINTS
        └── POTCAR

Comparing with the ``ALC-0_BASEFILES`` folder provided in the :ref:`page-basic`, the primary difference is the ``HIERARCH_PARAMS`` directory, i.e., which contains parameters for the C and N tiles, and the ``.temps`` file, which provides a single temperature for each frame in the corresponding ``.xyzf`` file, are highlighted.


-----------------
Input Files
-----------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ALC-0_BASEFILES Files 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Warning ::

    The ``ALC-0_BASEFILES/fm_setup.in`` requires a few special edits for hierarchical learning mode:

    * ``fm_setup.in`` should have ``# HIERARC #`` set ``true``
    * All 1- through *n*\-body interactions described in in the reference (``HIERARCH_PARAM_FILES``) files must be explicitly excluded
    * Orders in the ``ALC-0_BASEFILES/fm_setup.in`` file should be greater or equal to those in the reference (``HIERARCH_PARAM_FILES``) files
    * ``TYPEIDX`` and ``PAIRIDX`` entries in the base fm_setup.in file must be consistent with respect to the ``HIERARCH_PARAM_FILES`` files
    * ``SPECIAL XB`` cutoffs must be set to ``SPECIFIC N``, where *N* is the number of **NON**-excluded *X*\B interaction types 
    
    For additional information on how to configure these options, see the `ChIMES LSQ manual <https://chimes-lsq.readthedocs.io/en/latest/>`_.


.. Note ::

    Users must create a new folder, ``HIERARCH_PARAMS`` in their ``ALL_BASE_FILES`` directory and place in it the pure-C and pure-N parameter files, i.e.: 

    .. code-block:: bash 
    
        $: ls -l <my_fit>/ALL_BASE_FILES/HIERARCH_PARAMS
        -rw------- 1 rlindsey rlindsey 169630 May  1 10:55 C.params.txt.reduced
        -rw------- 1 rlindsey rlindsey 160015 May  1 10:55 N.params.txt.reduced

    Hierarchical fitting also requires special options in ``ALL_BASE_FILES/ALC-0_BASEFILES/fm_setup.in`` to ensure base the parameter types (e.g., in {C,N}.params.txt.reduced) are properly excluded from the fit. First, one must ensure that requested polynomial orders are greater or equal to those in the reference  ``ALL_BASE_FILES/HIERARCH_PARAMS`` parameter files. Next, add the highlighted lines to ``fm_setup.in``:

    .. code-block:: bash 
        :emphasize-lines: 9,10 
        
            # Snippet from ALL_BASE_FILES/ALC-0_BASEFILES/fm_setup.in

            # PAIRTYP # 
                    CHEBYSHEV 25 10 4 -1 1
            # CHBTYPE #
                    MORSE
            # SPLITFI #
                    false
            # HIERARC #     
                    true
        
    Users must also specify which interactions to exclude from the fit (i.e., interactions fully described by the ALL_BASE_FILES/HIERARCH_PARAMS files. For the present C/N fitting example, those lines would look like:

    .. code-block:: bash 
    
        ####### TOPOLOGY VARIABLES #######
    
        EXCLUDE 1B INTERACTION: 2
        C
        N
    
        EXCLUDE 2B INTERACTION: 2
        C C
        N N
    
        EXCLUDE 3B INTERACTION: 2
        C C C
        N N N
    
        EXCLUDE 4B INTERACTION: 2
        C C C C
        N N N N
    
    Users must also ensure that the ``fm_setup.in`` topolgy contents are consistent with those in the ALL_BASE_FILES/HIERARCH_PARAMS files. For the present C/N fitting example, those would be the highlighted lines below:
        
    .. code-block:: bash     
        :emphasize-lines: 5,6,9,10
        
        # NATMTYP # 
                2
    
        # TYPEIDX #     # ATM_TYP #     # ATMCHRG #     # ATMMASS # 
        1               C               0.0             12.0107
        2               N               0.0             14.0067
    
        # PAIRIDX #     # ATM_TY1 #     # ATM_TY1 #     # S_MINIM #     # S_MAXIM #     # S_DELTA #     # MORSE_LAMBDA #        # USEOVRP #     # NIJBINS #     # NIKBINS #     # NJKBINS #
        1               C               C               0.98            5.0             0.01            1.4                     false           0               0               0
        2               N               N               0.86            8.0             0.01            1.09                    false           0               0               0
        3               C               N               1.0             5.0             0.01            1.34                    false           0               0               0
    
    Users must explicitly define how many (and which) many-body interactions will be fit, and the corresponding outer cutoffs to use. Note that the option ``ALL`` cannot be used when performing hierarchical fits.
    
    .. code-block:: bash 
    
        SPECIAL 3B S_MAXIM: SPECIFIC 2
        CCCNCN   CC CN CN 5.0 5.0 5.0
        CNCNNN   CN CN NN 5.0 5.0 5.0
    
        SPECIAL 4B S_MAXIM: SPECIFIC 3
        CCCCCNCCCNCN    CC CC CN CC CN CN 4.5 4.5 4.5 4.5 4.5 4.5
        CCCNCNCNCNNN    CC CN CN CN CN NN 4.5 4.5 4.5 4.5 4.5 4.5
        CNCNCNNNNNNN    CN CN CN NN NN NN 4.5 4.5 4.5 4.5 4.5 4.5
    
.. Note ::
    
    Each training trajectory file in ALL_BASE_FILES/ALC-0_BASEFILES needs a corresponding .temps file that gives the temperature for each frame this ensures the right tempertaure corrections is done for each frame. 
    


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The config.py File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `config.py` file is given below:

.. code-block :: python
    :linenos:
    :emphasize-lines: 55-57
    
    ################################
    ##### General variables
    ################################

    EMAIL_ADD     = "lindsey11@llnl.gov" # driver will send updates on the status of the current run ... If blank (""), no emails are sent

    ATOM_TYPES = ['C', 'N']
    NO_CASES = 1

    DRIVER_DIR     = "/p/lustre2/rlindsey/al_driver/src/"
    WORKING_DIR    = "/p/lustre2/rlindsey/al_driver/examples/hierarch_fit"
    CHIMES_SRCDIR  = "/p/lustre2/rlindsey/chimes_lsq/src/"

    ################################
    ##### General HPC options
    ################################

    HPC_ACCOUNT = "TG-CHM"
    HPC_PYTHON  = "/scratch/projects/compilers/intel24.0/oneapi/intelpython/python3.9/bin/python"
    HPC_SYSTEM  = "TACC"
    HPC_PPN     = 48 
    HPC_EMAIL     = False 
    N_HYPER_SET = 1

    ################################
    ##### ChIMES LSQ
    ################################

    ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
    CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
    CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
    CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"

    # Generic weight settings

    WEIGHTS_FORCE =   1.0

    REGRESS_ALG   = "dlasso"
    REGRESS_VAR   = "1.0E-5"
    REGRESS_NRM   = True

    # Job submitting settings (avoid defaults because they will lead to long queue times)

    CHIMES_BUILD_NODES = 2
    CHIMES_BUILD_QUEUE = "pdebug"
    CHIMES_BUILD_TIME  = "01:00:00"

    CHIMES_SOLVE_NODES = 2
    CHIMES_SOLVE_QUEUE = "pdebug"
    CHIMES_SOLVE_TIME  = "01:00:00"

    ################################
    ##### Molecular Dynamics
    ################################

    MD_STYLE        = "CHIMES"
    CHIMES_MD_MPI   = CHIMES_SRCDIR + "../build/chimes_md"

    MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
    MOLANAL_SPECIES = ["C1", "N1"]

    ################################
    ##### Hierarchical fitting block
    ################################

    DO_HIERARCH = True
    HIERARCH_PARAM_FILES = ['C.params.txt.reduced', 'N.params.txt.reduced']
    HIERARCH_EXE = CHIMES_MD_SER

    ################################
    ##### Single-Point QM
    ################################

    QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
    VASP_EXE = "/usr/gapps/emc-vasp/vasp.5.4.4/build/gam/vasp"
    
The primary difference between the present ``config.py`` and that provided in :ref:`page-basic` documentation are the highlighted lines 55--57, which specify hierarchical fitting should be performed (line 55), the name of all parameter files that the present model should be built upon (line 56), and the executable to use when evaluating contributions from the parameter files specified on line 56 (line 57); for this example, we're using ChIMES_MD. Note that this executable should be compiled for serial runs to prevent issues with the queueing system. As in the example provided in :ref:`page-basic` documentation, contents of the ``config.py`` file must be modified to reflect your e-mail address and absolute paths prior to running this example. Make sure to update paths, email, and queue settings based on your environment. For Patial Hierarchical fitting you only specify either 'C.params.txt.reduced' if you want to learn both N and cross terms.


------------------------------------------
Running
------------------------------------------

Same procedure as in the basic example, depending on standard queuing times for your system, the ALD could take quite some time (e.g., hours) finish. For this reason it is generally, it is recommended to run the ALD from within a screen session on your HPC system. To do so, log into your HPC system and execute the following commands:


1. Configure `config.py`

2. Run `/path/to/your/ald/installation/main.py`

.. code-block :: bash

    $: cd /path/to/my/example/files
    $: screen 
    $: unbuffer python3 /path/to/your/ald/installation/main.py 0 1 2 3 | tee driver-0.log


3. Inspect output files.

When using hierarchical fitting:

- Check that contributions from provided parameters are correctly subtracted.

- Verify convergence of the newly learned terms.

------------------------------------------
In-Depth Setup and Options
------------------------------------------

For a complete explanation of:
- File preparation
- Order settings
- Parameter exclusion
- Advanced options

See the core documentation: :ref:`page-basic`.

**Pro Tip:** Start with full transfer when possible for better stability, then explore partial fitting as needed.


