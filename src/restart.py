# Global (python) modules

import os

class restart:

    def __init__(self):
    
        """ 

        Class controlling driver restart capability

        Usage: my_restart_class = restart.restart()

        Notes: Searches for "restart.dat" in the base ALC directory.
               If no "restart.dat" file is found, assumes a fresh start.
               Functionality is not supported for user-modified restart files.
                  
        """
    
        self.last_ALC           = -1
        self.BUILD_AMAT         = False
        self.SOLVE_AMAT         = False
        self.RUN_MD             = False
        self.POST_PROC          = False
        self.CLUSTER_EXTRACTION = False
        self.CLUENER_CALC       = False
        self.CLU_SELECTION      = False
        self.CLEANSETUP_QM      = False
        self.INIT_QMJOB         = False
        self.ALL_QMJOBS         = False
        self.ALL_FAILED_QMJOBS  = False 
        self.THIS_ALC           = False
        
        self.restart_stream     = None
    
        # Checks for a pre-existing restart file, uses to initialize self
        
        if os.path.isfile("restart.dat"):    # Then read/initialize
        
            ifstream = open("restart.dat",'r')
            contents = ifstream.readlines()
            ifstream.close()
            
            # Check if empty

            if len(contents) == 0:
            
                # Set up the restart file 

                self.restart_stream = open("restart.dat",'w+')
                self.restart_stream.flush()

                return
                
            
            # Find index of "ALC: X" in contents for the last attempted ALC
            
            last_ALC_index = [i for i, s in enumerate(contents) if ("ALC:" in s) and ("COMPLETE" not in s)][-1]
            self.last_ALC  = int(contents[last_ALC_index].split()[1])
            
            # Truncate "contents" so it only contains entries for the last attempted ALC
            
            contents = contents[last_ALC_index:]
            
            for i in range(len(contents)):
                contents[i] = contents[i].rstrip()
            
            # Set remaning logicals
            
            if "BUILD_AMAT: COMPLETE" in contents:    
                self.BUILD_AMAT = True    
            if "SOLVE_AMAT: COMPLETE" in contents:    
                self.SOLVE_AMAT = True    
            if "RUN_MD: COMPLETE" in contents:
                self.RUN_MD = True    
            if "POST_PROC: COMPLETE" in contents:    
                self.POST_PROC = True
            if "CLUSTER_EXTRACTION: COMPLETE" in contents:    
                self.CLUSTER_EXTRACTION = True
            if "CLUENER_CALC: COMPLETE" in contents:    
                self.CLUENER_CALC = True
            if "CLU_SELECTION: COMPLETE" in contents:
                self.CLU_SELECTION = True    
            if "CLEANSETUP_QM: COMPLETE" in contents:    
                self.CLEANSETUP_QM = True
            if "INIT_QMJOB: COMPLETE" in contents:    
                self.INIT_QMJOB = True
            if "ALL_QMJOBS: COMPLETE" in contents:    
                self.ALL_QMJOBS = True
            if "ALL_FAILED_QMJOBS: COMPLETE" in contents:
                self.ALL_FAILED_QMJOBS = True                    
            if "THIS_ALC: COMPLETE" in contents:
                self.THIS_ALC = True    
                
            print("")
            print("Restart has set the following:    ")
            print("    self.last_ALC           ",self.last_ALC)    
            print("    self.BUILD_AMAT         ",self.BUILD_AMAT) 
            print("    self.SOLVE_AMAT         ",self.SOLVE_AMAT) 
            print("    self.RUN_MD             ",self.RUN_MD)    
            print("    self.POST_PROC          ",self.POST_PROC)  
            print("    self.CLUSTER_EXTRACTION ",self.CLUSTER_EXTRACTION)
            print("    self.CLUENER_CALC       ",self.CLUENER_CALC)
            print("    self.CLU_SELECTION      ",self.CLU_SELECTION)
            print("    self.CLEANSETUP_QM      ",self.CLEANSETUP_QM)
            print("    self.INIT_QMJOB         ",self.INIT_QMJOB)
            print("    self.ALL_QMJOBS         ",self.ALL_QMJOBS)
            print("    self.ALL_FAILED_QMJOBS  ",self.ALL_FAILED_QMJOBS)
            print("    self.THIS_ALC           ",self.THIS_ALC)    
            print("")
            
            # Open the restart file for writing, in append mode
            
            
            self.restart_stream = open("restart.dat",'a+')
            self.restart_stream.flush()
            
            
        else:
            # Set up the restart file 
            
            self.restart_stream = open("restart.dat",'w+')
            self.restart_stream.flush()
            
        return
        
        
    def __del__(self):
    
        if self.restart_stream:
            if not self.restart_stream.closed:
                self.restart_stream.close()
            
    def reinit_vars(self):            
            
        self.BUILD_AMAT         = False
        self.SOLVE_AMAT         = False
        self.RUN_MD         = False
        self.POST_PROC         = False
        self.CLUSTER_EXTRACTION     = False
        self.CLUENER_CALC     = False
        self.CLU_SELECTION     = False
        self.CLEANSETUP_QM     = False
        self.INIT_QMJOB             = False
        self.ALL_QMJOBS             = False
        self.ALL_FAILED_QMJOBS  = False
        self.THIS_ALC         = False            
            
    def update_file(self, txt_str):
        self.restart_stream.write(txt_str)
        self.restart_stream.flush()

            

    def update_ALC_list(self, *argv):
        
        ALC_LIST = argv[0]

        ALC_LIST = [int(a) for a in ALC_LIST] # added, for "9, 10, 11" (str order will be "10", "11", "9")

        ALC_LIST = sorted(set(ALC_LIST)) # Ascending sort preserving only unique values

        ALC_LIST = [str(a) for a in ALC_LIST]
        
        # Check if restart file was empty (i.e. self.last_ALC never got updated from -1)
        
        if self.last_ALC == -1:
            return     ALC_LIST
        
        # Cases:
        #
        # 1. Restart's last ALC is greater than the greatest alc in the list 
        #    - quit with error
        # 2. Restart's last ALC is equal to the greatest alc in the list, and it completed 
        #    - quit with message
        # 3. Restart's last ALC is less than the greatest alc in the list, but was completed 
        #    - start on next ALC
        # 4. Restart's last ALC is less than or equal to the greatest ALC in the list, but was not completed
        #    - start on the current ALC ... restart checks will skip completed steps
                
        # Case 1
        
        if int(ALC_LIST[-1]) < self.last_ALC:
        
            print("ERROR: Last attempted ALC (in restart) is greater than largest requested ALC:")
            print("       Last attempted ALC:", self.last_ALC)
            print("       Requested ALC list:", ALC_LIST)
            print("...Exiting.")
            
            exit()
            
        # Case 2

        if (int(ALC_LIST[-1]) == self.last_ALC) and (self.THIS_ALC):
        
            print("ERROR: Last attempted ALC (in restart) is equal to largest requested ALC, and has completed:")
            print("       Last attempted ALC:", self.last_ALC)
            print("       Requested ALC list:", ALC_LIST)
            print("...Exiting.")
            
            exit()
            
        # Case 3
        
        if (int(ALC_LIST[-1]) > self.last_ALC) and (self.THIS_ALC):
            
            # Get the index of ALC_LIST item matching self.last_ALC
            
            idx = ALC_LIST.index(repr(self.last_ALC))
            
            # Update ALC_LIST to only include entries > idx
            
            idx += 1
            
            ALC_LIST = ALC_LIST[idx:]
            
            self.reinit_vars()
            
            return ALC_LIST
            
        # Case 4
        
        if (int(ALC_LIST[-1]) >= self.last_ALC) and (not self.THIS_ALC):
            
            # Get the index of ALC_LIST item matching self.last_ALC
            
            idx = ALC_LIST.index(repr(self.last_ALC))
            
            # Update ALC_LIST to include all entries >= idx
            
            ALC_LIST = ALC_LIST[idx:]
            
            return ALC_LIST
            
            
        
                
            


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
