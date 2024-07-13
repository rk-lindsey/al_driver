# Global (python) modules

import glob # Warning: glob is unserted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Local modules

import chimes_run_md
import dftbplus_run_md
import lmp_run_md


def post_proc(my_ALC, my_case, my_indep, style, *argv, **kwargs):

    """ 
    
    Post-processes a ChIMES MD run
    
    Usage: run_md(1, 0, 0, <arguments>)
    
    Notes: See function definition in *_run_md.py for a full list of options. 
           Requrires config.CHIMES_MOLANAL (should contain molanal.new and findmolecules.pl)
           Expects to be called from ALC-my_ALC's base folder.
           Assumes job is being launched from ALC-X.
           Supports ~parallel learning~ via file structure:
                  ALC-X/CASE-1_INDEP-1/<md simulation/stuff>
           Expects input files named like:
                  case-1.indep-1.input.xyz and case-1.indep-1.run_md.in
           will run molanal on finished simulation.
           Will post-process the molanal output.
           Will generate clusters.
           Will save clusters to CASE-X_INDEP-0/CFG_REPO.
               
    """
    
    if style == "CHIMES":
        chimes_run_md.post_proc(my_ALC, my_case, my_indep, *argv, **kwargs)
    elif style == "DFTB":
        dftbplus_run_md.post_proc(my_ALC, my_case, my_indep, *argv, **kwargs)
    elif style == "LMP":
        lmp_run_md.post_proc(my_ALC, my_case, my_indep, *argv, **kwargs)        
    else:
        print("ERROR: Unknown post_proc style in run_md.py: ", style)
    
    return     


def run_md(my_ALC, my_case, my_indep, style, *argv, **kwargs):

    """ 
    
    Launches a ChIMES md simulation
    
    Usage: run_md(1, 0, 0, <arguments>)
    
    Notes: See function definition in *_run_md.py for a full list of options. 
           Requrires config.CHIMES_MD.
           Requrires config.CHIMES_MOLANAL (should contain molanal.new and findmolecules.pl)
           Expects to be called from ALC-my_ALC's base folder.
           Assumes job is being launched from ALC-X.
           Supports ~parallel learning~ via file structure:
                  ALC-X/CASE-1_INDEP-1/<md simulation/stuff>
           Expects input files named like:
                  case-1.indep-1.input.xyz and case-1.indep-1.run_md.in
           Returns a job_id for the submitted job.
               
    """
    
    md_jobid = None
    
    if style == "CHIMES":
        md_jobid = chimes_run_md.run_md(my_ALC, my_case, my_indep, *argv, **kwargs)
    elif style == "DFTB":
        md_jobid = dftbplus_run_md.run_md(my_ALC, my_case, my_indep, *argv, **kwargs)
    elif style == "LMP":
        md_jobid = lmp_run_md.run_md(my_ALC, my_case, my_indep, *argv, **kwargs)        
    else:
        print("ERROR: Unknown post_proc style in run_md.py: ", style)
    
    return md_jobid    
    
