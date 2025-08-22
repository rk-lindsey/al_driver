import sys
import os
import helpers

#### WARNING: NO SUPPORT FOR SPECIAL **INNER** CUTOFF SPECIFICATION
#### WARNING: SUPPORT ONLY FOR CHEBY INTERACTIONS; NO CHARGE FITTING; FIXED CHARGES OK BUT UNTESTED

class bool_block:

    def __init__(self):
        self.keys = [["USECOUL:", None], ["FITCOUL:", None], ["USEPOVR:", None], ["FITPOVR:", None], ["USE3BCH:", None],  ["USE4BCH:", None], ["EXCLD1B:", "false"], ["EXCLD2B:", "false"]]
        
    def set_block(self,param_data):
        for i in range(len(param_data)):
            for j in range(len(self.keys)):
                if self.keys[j][0] in param_data[i]:
                    if "EXCLD" in self.keys[j][0]:
                        if "EXCLD1B" in self.keys[j][0]:
                            self.keys[j][1] = ' '.join(param_data[i].split()[1:])
                        elif "EXCLD2B" in self.keys[j][0]:
                            self.keys[j][1] = ' '.join(param_data[i].split()[1:])
                        else:
                            print("ERROR: Unrecognized header exclusion type:", self.keys[j][0])
                            print("Allowed header exclusion types are EXCLD1B and EXCLD2B")
                    else:
                        self.keys[j][1] = param_data[i].split()[-1]
    def print_block(self,to="stdout"):

        if to == "stdout":
            for j in range(len(self.keys)):
                if self.keys[j][1] is not None:
                    print(self.keys[j][0] + " " + self.keys[j][1])
            print("")
    
        else:
            for j in range(len(self.keys)):
                if self.keys[j][1] is not None:
                    try:
                    	to.write(self.keys[j][0] + " " + self.keys[j][1] + '\n')
                    except:
                    	to.write(self.keys[j][0] + " " + ' '.join(self.keys[j][1]) + '\n')                    
            to.write("\n")

class complexity_block:
    def __init__(self):
        self.O2B = None
        self.O3B = None
        self.O4B = None
        
    def set_block(self,param_data):
    
        for i in range(len(param_data)):
            if "PAIRTYP: " in param_data[i]:
            
                tmp =  param_data[i].split()
                self.O2B = tmp[2]
                self.O3B = tmp[3]
                self.O4B = tmp[4]
                
                break
                
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("PAIRTYP: CHEBYSHEV " + self.O2B + " " + self.O3B + " " + self.O4B + " -1 1\n")
        else:
            to.write("PAIRTYP: CHEBYSHEV " + self.O2B + " " + self.O3B + " " + self.O4B + " -1 1" + '\n\n')                
                
class atm_types_block:

    def __init__(self):
        self.ntype = None
        self.type  = []
        self.chrg  = []
        self.mass  = []
        
    def set_block(self,param_data):
    
        type_line = None
    
        for i in range(len(param_data)):
        
            if "ATOM TYPES: " in param_data[i]:
                self.ntype = param_data[i].split()[-1]
                
            if "TYPEIDX" in param_data[i]:
                type_line = i+1
                break
                
        for i in range(int(self.ntype)):
            line = param_data[type_line+i].split()
            self.type.append(line[1])
            self.chrg.append(line[2])
            self.mass.append(line[3])
            
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("ATOM TYPES: " + self.ntype)
            print("")
            print("# TYPEIDX #    # ATM_TYP #    # ATMCHRG #    # ATMMASS #")
            for i in range(int(self.ntype)):
                print(str(i) + "\t" + self.type[i] + "\t" + self.chrg[i] + "\t" + self.mass[i])
            print("")    
        else:
            to.write("ATOM TYPES: " + self.ntype + '\n')
            to.write('\n')
            to.write("# TYPEIDX #    # ATM_TYP #    # ATMCHRG #    # ATMMASS #\n")
            for i in range(int(self.ntype)):
                to.write(str(i) + "\t" + self.type[i] + "\t" + self.chrg[i] + "\t" + self.mass[i] + '\n')
            to.write('\n')                
            

class pair_types_block:

    def __init__(self):
        self.npair = None
        self.type1 = []
        self.type2 = []
        self.rmin  = []
        self.rmax  = []
        self.xform = []
        self.lambd = []
        
    def set_block(self,param_data):
    
        type_line = None
    
        for i in range(len(param_data)):
        
            if "ATOM PAIRS: " in param_data[i]:
                self.npair = param_data[i].split()[-1]
                
            if "PAIRIDX" in param_data[i]:
                type_line = i+1
                break

        for i in range(int(self.npair)):
            line = param_data[type_line+i].split()
            self.type1.append(line[1])
            self.type2.append(line[2])
            self.rmin .append(line[3])
            self.rmax .append(line[4])
            self.xform.append(line[-2])
            self.lambd.append(line[-1])
            
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("ATOM PAIRS: " + self.npair)
            print("")
            print("# PAIRIDX #    # ATM_TY1 #    # ATM_TY1 #    # S_MINIM #    # S_MAXIM #    # S_DELTA #    # CHBDIST #    # MORSE_LAMBDA #")
            for i in range(int(self.npair)):
                print(str(i) + "\t" + self.type1[i] + "\t" + self.type2[i] + "\t" + self.rmin[i] + "\t" + self.rmax[i] + "\t0.01\t" + self.xform[i] + "\t" + self.lambd[i])
            print("")
        else:
            to.write("ATOM PAIRS: " + self.npair + '\n')
            to.write('\n')
            to.write("# PAIRIDX #    # ATM_TY1 #    # ATM_TY1 #    # S_MINIM #    # S_MAXIM #    # S_DELTA #    # CHBDIST #    # MORSE_LAMBDA #\n")
            for i in range(int(self.npair)):
                to.write(str(i) + "\t" + self.type1[i] + "\t" + self.type2[i] + "\t" + self.rmin[i] + "\t" + self.rmax[i] + "\t0.01\t" + self.xform[i] + "\t" + self.lambd[i] + '\n')    
            to.write('\n')

class fcut_block:

    def __init__(self):
        self.type = None
        self.vars = []
        
    def set_block(self,param_data):
        for i in range(len(param_data)):
            if "FCUT TYPE: " in param_data[i]:
            
                tmp =  param_data[i].split()
                self.type = tmp[2]
                self.vars = tmp[3:]
                
                break        
                
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("FCUT TYPE:  " + self.type + " " + ' '.join(self.vars) + '\n')
        else:
            to.write("FCUT TYPE:  " + self.type + " " + ' '.join(self.vars) + '\n\n')                
    

class special3bmax_block:

    def __init__(self):
    
        self.specific = None
        self.all      = None
        self.all_cut  = None
        self.number   = None
        self.cluster  = []
        self.pair1    = []
        self.pair2    = []
        self.pair3    = []
        self.cut1     = []
        self.cut2     = []
        self.cut3     = []    

    def set_block(self,param_data):
    
        type_line = None

        for i in range(len(param_data)):
        
            if "SPECIAL 3B S_MAXIM: " in param_data[i]:
                tmp = param_data[i].split()
                
                if tmp[-2] == "ALL":
                    self.specific = False
                    self.all      = True
                    self.number   = 0
                    self.all_cut  = tmp[-1]
                elif tmp[-2] == "SPECIFIC":
                    self.specific = True
                    self.all      = False
                    self.number   = tmp[-1]
                    type_line     = i+1
                break
            

        if self.specific:
            for i in range(int(self.number)):
                line = param_data[type_line+i].split()
                self.cluster.append(line[0])
                self.pair1  .append(line[1])
                self.pair2  .append(line[2])
                self.pair3  .append(line[3])
                self.cut1   .append(line[4])
                self.cut2   .append(line[5])
                self.cut3   .append(line[6])

    def print_block(self,to="stdout"):
    
        if to == "stdout":
            
            if self.all:
                print("SPECIAL 3B S_MAXIM: ALL " + self.all_cut)
            elif self.specific:
                print("SPECIAL 3B S_MAXIM: SPECIFIC " + self.number)
                for i in range(int(self.number)):
                    print(self.cluster[i] + " " + self.pair1[i] + " " + self.pair2[i] + " " + self.pair3[i] + " " + "{:.4f}".format(float(self.cut1[i])) + " " + "{:.4f}".format(float(self.cut2[i])) + " " + "{:.4f}".format(float(self.cut3[i])))  
            print("")
        else:
            if self.all:
                to.write("SPECIAL 3B S_MAXIM: ALL " + self.all_cut + '\n')
            elif self.specific:
                to.write("SPECIAL 3B S_MAXIM: SPECIFIC " + self.number + '\n')
                for i in range(int(self.number)):
                    to.write(self.cluster[i] + " " + self.pair1[i] + " " + self.pair2[i] + " " + self.pair3[i] + " " + "{:.4f}".format(float(self.cut1[i])) + " " + "{:.4f}".format(float(self.cut2[i])) + " " + "{:.4f}".format(float(self.cut3[i])) + '\n')
            to.write('\n')
                

class special4bmax_block:

    def __init__(self):
    
        self.specific = None
        self.all      = None
        self.all_cut  = None
        self.number   = None
        self.cluster  = []
        self.pair1    = []
        self.pair2    = []
        self.pair3    = []
        self.pair4    = []
        self.pair5    = []
        self.pair6    = []        
        self.cut1     = []
        self.cut2     = []
        self.cut3     = []
        self.cut4     = []
        self.cut5     = []
        self.cut6     = []            

    def set_block(self,param_data):
    
        type_line = None
        
        for i in range(len(param_data)):
        
            if "SPECIAL 4B S_MAXIM: " in param_data[i]:
                tmp = param_data[i].split()
    
                if tmp[-2] == "ALL":
                    self.specific = False
                    self.all      = True
                    self.number   = 0
                    self.all_cut  = tmp[-1]
                elif tmp[-2] == "SPECIFIC":
                    self.specific = True
                    self.all      = False
                    self.number   = tmp[-1]
                    type_line     = i+1
                break
            

        if self.specific:
            for i in range(int(self.number)):
                line = param_data[type_line+i].split()
                self.cluster.append(line[0 ])
                self.pair1  .append(line[1 ])
                self.pair2  .append(line[2 ])
                self.pair3  .append(line[3 ])
                self.pair4  .append(line[4 ])
                self.pair5  .append(line[5 ])
                self.pair6  .append(line[6 ])
                self.cut1   .append(line[7 ])
                self.cut2   .append(line[8 ])
                self.cut3   .append(line[9 ])
                self.cut4   .append(line[10])
                self.cut5   .append(line[11])
                self.cut6   .append(line[12])

    def print_block(self,to="stdout"):
    
        if to == "stdout":
            
            if self.all:
                print("SPECIAL 4B S_MAXIM: ALL " + self.all_cut)
            elif self.specific:
                print("SPECIAL 4B S_MAXIM: SPECIFIC " + self.number)
                for i in range(int(self.number)):
                    print(self.cluster[i] + " " + self.pair1[i] + " " + self.pair2[i] + " " + self.pair3[i] + " " + self.pair4[i] + " " + self.pair5[i] + " " + self.pair6[i] \
                     + " " + "{:.4f}".format(float(self.cut1[i])) + " " + "{:.4f}".format(float(self.cut2[i])) + " " + "{:.4f}".format(float(self.cut3[i])) + " " + "{:.4f}".format(float(self.cut4[i])) + " " + "{:.4f}".format(float(self.cut5[i])) + " " + "{:.4f}".format(float(self.cut6[i]))) 
            print("")
        else:
            if self.all:
                to.write("SPECIAL 4B S_MAXIM: ALL " + self.all_cut + '\n')
            elif self.specific:
                to.write("SPECIAL 4B S_MAXIM: SPECIFIC " + self.number + '\n')
                for i in range(int(self.number)):
                    to.write(self.cluster[i] + " " + self.pair1[i] + " " + self.pair2[i] + " " + self.pair3[i] + " " + self.pair4[i] + " " + self.pair5[i] + " " + self.pair6[i] \
                    + " " + "{:.4f}".format(float(self.cut1[i])) + " " + "{:.4f}".format(float(self.cut2[i])) + " " + "{:.4f}".format(float(self.cut3[i])) + " " + "{:.4f}".format(float(self.cut4[i])) + " " + "{:.4f}".format(float(self.cut5[i])) + " " + "{:.4f}".format(float(self.cut6[i])) + '\n')    
            to.write('\n')            

class clu_count_block:

    def __init__(self):
    
        self.ntrips = None
        self.nquads = None    
        
    def set_block(self,param_data):
    
        for i in range(len(param_data)):
        
            if "ATOM PAIR TRIPLETS: " in param_data[i]:
                self.ntrips = param_data[i].split()[-1]
        
            if "ATOM PAIR QUADRUPLETS: " in param_data[i]:
                self.nquads = param_data[i].split()[-1]
                break
                
    def print_block(self,to="stdout"):
    
        if to == "stdout":    
            print("ATOM PAIR TRIPLETS: "    + self.ntrips)
            print("ATOM PAIR QUADRUPLETS: " + self.nquads)
            print("")
        else:
            to.write("ATOM PAIR TRIPLETS: "       + self.ntrips + '\n')
            to.write("ATOM PAIR QUADRUPLETS: "    + self.nquads + '\n\n')

class params_2b:

    def __init__(self, pairidx, order):
    
        self.order  = str(order)
        self.idx    = str(pairidx)
        self.atm1   = None
        self.atm2   = None
        self.params = []
        
    def set_block(self,param_data):
    
        key = "PAIRTYPE PARAMS: " + self.idx 
    
        type_line = None
        
        for i in range(len(param_data)):
        
            if key in param_data[i]:
                tmp = param_data[i].split()
                
                self.atm1 = tmp[-2]
                self.atm2 = tmp[-1]
                type_line     = i+2
                break
        
        for i in range(int(self.order)):
            self.params.append(param_data[type_line+i].split()[-1])
    
    
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("PAIRTYPE PARAMS: " + self.idx + " " + self.atm1 + " " + self.atm2)
            print("")
            for i in range(int(self.order)):
                print(str(i) + " " + self.params[i])
            print("")
        else:
            to.write("PAIRTYPE PARAMS: " + self.idx + " " + self.atm1 + " " + self.atm2 + '\n') 
            to.write("\n")
            for i in range(int(self.order)):
                to.write(str(i) + " " + self.params[i] + '\n')
            to.write('\n')
                
class params_3b:

    def __init__(self, tripidx):
    
        self.npar   = None
        self.nuniq  = None
        self.excl   = False
        self.idx    = str(tripidx)
        self.atms   = []
        self.pairs  = []
        self.totidx = []
        self.power1 = []
        self.power2 = []
        self.power3 = []
        self.eqvidx = []
        self.powidx = []
        self.params = []
        
    def set_block(self,param_data):
    
        key1 = "TRIPLETTYPE PARAMS:"
        key2 = "INDEX: " + self.idx + " ATOMS:"
        ntoken = 6 # How many entries are we expecting in the key 2 line
    
        type_line = None
        
        for i in range(len(param_data)):
        
            if key1 in param_data[i]: # Found "TRIPLETTYPE PARAMS", now need to determine if its the right type
                 if key2 in param_data[i+1]: # Confirmed its the right 3b type
                 
                    tmp = param_data[i+1].split() # INDEX: 0 ATOMS: C C C
                 
                    self.atms.append(tmp[3])
                    self.atms.append(tmp[4])
                    self.atms.append(tmp[5])
                    
                    tmp = param_data[i+2].split() # PAIRS: CC CC CC UNIQUE: 665 TOTAL: 3332
                    
                    self.pairs.append(tmp[1])
                    self.pairs.append(tmp[2])
                    self.pairs.append(tmp[3])
                    
                    if "EXCLUDED" in tmp[4]:
                        self.excl = True
                    else:
                        self.excl = False    
                        self.nuniq = tmp[5]
                        self.npar  = tmp[7]
                    
                    type_line = i+5
                    break
        
        if not self.excl:    
            for i in range(int(self.npar)):
        
                tmp = param_data[type_line+i].split()
                self.totidx.append(tmp[0])
                self.power1.append(tmp[1])
                self.power2.append(tmp[2])
                self.power3.append(tmp[3])
                self.eqvidx.append(tmp[4])
                self.powidx.append(tmp[5])
                self.params.append(tmp[6])
                    
                    
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("TRIPLETTYPE PARAMS:")
            print("   INDEX: " + self.idx + " ATOMS: " + ' '.join(self.atms))
            if self.excl:
                print("   PAIRS: " + ' '.join(self.pairs) + " EXCLUDED:")
                print("")
                return    
            else:
                print("   PAIRS: " + ' '.join(self.pairs) + " UNIQUE: " + self.nuniq + " TOTAL: " + self.npar)    
            print("     index  |  powers  |  equiv index  |  param index  |       parameter ")
            print("   ----------------------------------------------------------------------------")
            for i in range(int(self.npar)):
                print(self.totidx[i] + " " + self.power1[i] + " " + self.power2[i] + " " + self.power3[i] + " " + self.eqvidx[i] + " " + self.powidx[i] + " " + self.params[i])            
            print("")
        else:
            to.write("TRIPLETTYPE PARAMS:\n")
            to.write("   INDEX: " + self.idx + " ATOMS: " + ' '.join(self.atms) + '\n')
            if self.excl:
                to.write("   PAIRS: " + ' '.join(self.pairs) + " EXCLUDED: \n")
                to.write('\n')
                return    
            else:    
                to.write("   PAIRS: " + ' '.join(self.pairs) + " UNIQUE: " + self.nuniq + " TOTAL: " + self.npar + '\n')        
            to.write("     index  |  powers  |  equiv index  |  param index  |       parameter " + '\n')
            to.write("   ----------------------------------------------------------------------------" + '\n')

            for i in range(int(self.npar)):
                to.write(self.totidx[i] + " " + self.power1[i] + " " + self.power2[i] + " " + self.power3[i] + " " + self.eqvidx[i] + " " + self.powidx[i] + " " + self.params[i] + '\n')    
            to.write('\n')    
                            

class params_4b:

    def __init__(self, quadidx):
    
        self.npar   = None
        self.nuniq  = None
        self.excl   = False 
        self.idx    = str(quadidx)
        self.atms   = []
        self.pairs  = []
        self.totidx = []
        self.power1 = []
        self.power2 = []
        self.power3 = []
        self.power4 = []
        self.power5 = []
        self.power6 = []        
        self.eqvidx = []
        self.powidx = []
        self.params = []
        
    def set_block(self,param_data):
    
        key1 = "QUADRUPLETYPE PARAMS:"
        key2 = "INDEX: " + self.idx + " ATOMS:"
        ntoken = 7 # How many entries are we expecting in the key 2 line
    
        type_line = None
        
        for i in range(len(param_data)):
        
            if key1 in param_data[i]:
                 if key2 in param_data[i+1]:
                 
                    tmp = param_data[i+1].split() # INDEX: 0 ATOMS: C C C C
    
                    self.atms.append(tmp[3])
                    self.atms.append(tmp[4])
                    self.atms.append(tmp[5])
                    self.atms.append(tmp[6])
                    
                    tmp = param_data[i+2].split() # PAIRS: CC CC CC CC CC CC UNIQUE: 865 TOTAL: 15152
        
                    for j in range(6):
                         self.pairs.append(tmp[j+1])
                        
                    if "EXCLUDED" in tmp[7]:
                        self.excl = True
                    else:
                        self.excl = False
                        self.nuniq = tmp[8]
                        self.npar  = tmp[10]
                    
                    type_line = i+5
                    break
                    
        if not self.excl:
                    
            for i in range(int(self.npar)):
        
                tmp = param_data[type_line+i].split()
                self.totidx.append(tmp[0])
                self.power1.append(tmp[1])
                self.power2.append(tmp[2])
                self.power3.append(tmp[3])
                self.power4.append(tmp[4])
                self.power5.append(tmp[5])
                self.power6.append(tmp[6])            
                self.eqvidx.append(tmp[7])
                self.powidx.append(tmp[8])
                self.params.append(tmp[9])
                    
                    
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("QUADRUPLETYPE PARAMS: ")
            print("   INDEX: " + self.idx + " ATOMS: " + ' '.join(self.atms))
            if self.excl:
                print("   PAIRS: " + ' '.join(self.pairs) + " EXCLUDED:")
                print("")
                return
            else:
                print("   PAIRS: " + ' '.join(self.pairs) + " UNIQUE: " + self.nuniq + " TOTAL: " + self.npar)
            print("     index  |  powers  |  equiv index  |  param index  |       parameter ")
            print("   ----------------------------------------------------------------------------")
            for i in range(int(self.npar)):
                print(self.totidx[i] + " " + self.power1[i] + " " + self.power2[i] + " " + self.power3[i] \
                + " " + self.power4[i] + " " + self.power5[i] + " " + self.power6[i] \
                + " " + self.eqvidx[i] + " " + self.powidx[i] + " " + self.params[i])        
            print("")    
        else:
            to.write("QUADRUPLETYPE PARAMS:\n")
            to.write("   INDEX: " + self.idx + " ATOMS: " + ' '.join(self.atms) + '\n')
            if self.excl:
                to.write("   PAIRS: " + ' '.join(self.pairs) + " EXCLUDED:\n")
                to.write('\n')
                return    
            else:
                to.write("   PAIRS: " + ' '.join(self.pairs) + " UNIQUE: " + self.nuniq + " TOTAL: " + self.npar + '\n')        
            to.write("     index  |  powers  |  equiv index  |  param index  |       parameter " + '\n')
            to.write("   ----------------------------------------------------------------------------" + '\n')
            for i in range(int(self.npar)):
                to.write(self.totidx[i] + " " + self.power1[i] + " " + self.power2[i] + " " + self.power3[i] \
                + " " + self.power4[i] + " " + self.power5[i] + " " + self.power6[i] \
                + " " + self.eqvidx[i] + " " + self.powidx[i] + " " + self.params[i] + '\n')
            to.write('\n')        

class params_2b_block:

    def __init__(self, npair, order): # test_clu_count_block
    
        self.npair = npair
        self.order = order
        self.par2b = [None]*int(self.npair)
                
    def set_block(self,param_data):
    
        for i in range(int(self.npair)):
            self.par2b[i] = params_2b(i, self.order)                    
            self.par2b[i].set_block(param_data)
            
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("PAIR CHEBYSHEV PARAMS\n")
        else:
            to.write("PAIR CHEBYSHEV PARAMS\n\n")
        
        for i in range(int(self.npair)):
            self.par2b[i].print_block(to)

class params_3b_block:

    def __init__(self, ntrips): # test_clu_count_block
    
        self.ntrips = ntrips
        self.par3b  = [None]*int(self.ntrips)
                
    def set_block(self,param_data):
    
        for i in range(int(self.ntrips)):
            self.par3b[i] = params_3b(i)                    
            self.par3b[i].set_block(param_data)
            
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("TRIPLET CHEBYSHEV PARAMS\n")
        else:
            to.write("TRIPLET CHEBYSHEV PARAMS\n\n")
        
        for i in range(int(self.ntrips)):
            self.par3b[i].print_block(to)
            
class params_4b_block:

    def __init__(self, nquads): # test_clu_count_block

        self.nquads = nquads
        self.par4b  = [None]*int(self.nquads)
        
    def set_block(self,param_data):
    
        for i in range(int(self.nquads)):
            self.par4b[i] = params_4b(i)                    
            self.par4b[i].set_block(param_data)
            
    def print_block(self,to="stdout"):
        if to == "stdout":
            print("QUADRUPLET CHEBYSHEV PARAMS\n")
        else:
            to.write("QUADRUPLET CHEBYSHEV PARAMS\n\n")
        for i in range(int(self.nquads)):    
            self.par4b[i].print_block(to)
class map_2b_block:

    def __init__(self):
        self.npair    = None
        self.labels   = []
        self.clusters = []
        
    type_line = None
        
    def set_block(self,param_data):
        for i in range(len(param_data)):
            if "PAIRMAPS:" in param_data[i]:
            
                tmp =  param_data[i].split()
                self.npair = tmp[-1]
                
                type_line = i+1
                break
                
        for i in range(int(self.npair)):
    
            tmp =  param_data[i+type_line].split()
    
            self.labels  .append(tmp[0])
            self.clusters.append(tmp[1])
                
    def print_block(self,to="stdout"):
    
        if to == "stdout":
            print("\nPAIRMAPS: " + self.npair)
            for i in range(int(self.npair)):
                print(self.labels[i] + " " + self.clusters[i])
            print("")
        else:
            to.write("PAIRMAPS: " + self.npair + '\n')
            for i in range(int(self.npair)):
                to.write(self.labels[i] + " " + self.clusters[i] + '\n')
            to.write("\n")            
    

class map_3b_block:

    def __init__(self):
        self.ntrip      = 0
        self.labels     = []
        self.eff_labels = []
        self.clusters   = []
        self.sort_clus  = []
        
    type_line = None
        
    def set_block(self,param_data):
        for i in range(len(param_data)):
            if "TRIPMAPS:" in param_data[i]:
            
                tmp =  param_data[i].split()
                self.ntrip = tmp[-1]
                
                type_line = i+1
                break
                
        for i in range(int(self.ntrip)):
    
            tmp =  param_data[i+type_line].split()
                
            self.labels  .append(tmp[0])
            self.clusters.append(tmp[1])
            
        
        idx=-1
        
        for i in range(int(self.ntrip)):
            if int(self.labels[i])<0:
                idx += 1
                self.eff_labels.append(str(idx))
            else:
                idx = int(self.labels[i])
                self.eff_labels.append(self.labels[i])
                
        #print "Sorted the lables",self.labels
        #print "Set eff labels:",self.eff_labels
        #print "For:",self.clusters                
                
        
        return
        
        if False:
                
            
            # Figure out how many unique types there are and what the labels should have been
        
            for i in range(int(self.ntrip)):
                self.sort_clus.append(''.join(sorted(self.clusters[i])))
            self.sort_clus = list(set(self.sort_clus))
            
            print("SAN:",self.sort_clus) 
            
            for i in range(int(self.ntrip)):
                for j in range(len(self.sort_clus)):
                    if ''.join(sorted(self.clusters[i])) == self.sort_clus[j]:
                        self.eff_labels.append(str(j))
            print("Sorted the lables",self.labels)
            print("Set eff labels:",self.eff_labels)
            print("For:",self.clusters)
                    
    def print_block(self,to="stdout"):
    
        if self.ntrip == 0:
            return    
    
        if to == "stdout":
            print("TRIPMAPS: " + self.ntrip)
            for i in range(int(self.ntrip)):
                #print self.labels[i] + " " + self.clusters[i]
                print(self.eff_labels[i] + " " + self.clusters[i])
            print("")
        else:
            to.write("TRIPMAPS: " + self.ntrip + '\n')
            for i in range(int(self.ntrip)):
                #to.write(self.labels[i] + " " + self.clusters[i] + '\n')
                to.write(self.eff_labels[i] + " " + self.clusters[i] + '\n')
            to.write("\n")    
class map_4b_block:

    def __init__(self):
        self.nquad    = 0
        self.labels   = []
        self.eff_labels = []
        self.clusters   = []
        self.sort_clus  = []        
        
    type_line = None
        
    def set_block(self,param_data):
        for i in range(len(param_data)):
            if "QUADMAPS:" in param_data[i]:
            
                tmp =  param_data[i].split()
                self.nquad = tmp[-1]
                
                type_line = i+1
                break
                
        for i in range(int(self.nquad)):
    
            tmp =  param_data[i+type_line].split()
    
            self.labels  .append(tmp[0])
            self.clusters.append(tmp[1])
            
        idx=-1
        
        for i in range(int(self.nquad)):
            if int(self.labels[i])<0:
                idx += 1
                self.eff_labels.append(str(idx))
            else:
                idx = int(self.labels[i])
                self.eff_labels.append(self.labels[i])
                
        #print "Sorted the lables",self.labels
        #print "Set eff labels:",self.eff_labels
        #print "For:",self.clusters                
                
        
        return    
        
        if False:        
            
            # Figure out how many unique types there are and what the labels should have been
            
            for i in range(int(self.nquad)):
                self.sort_clus.append(''.join(sorted(self.clusters[i])))
            self.sort_clus = list(set(self.sort_clus))
            
            for i in range(int(self.nquad)):
                for j in range(len(self.sort_clus)):
                    if ''.join(sorted(self.clusters[i])) == self.sort_clus[j]:
                        self.eff_labels.append(str(j))            
                
    def print_block(self,to="stdout"):
    
        if self.nquad == 0:
            return
    
        if to == "stdout":
            print("QUADMAPS: " + self.nquad)
            for i in range(int(self.nquad)):
                print(self.labels[i] + " " + self.clusters[i])
            print("")
        else:
            to.write("QUADMAPS: " + self.nquad + '\n')
            for i in range(int(self.nquad)):
                to.write(self.labels[i] + " " + self.clusters[i] + '\n')
            to.write("\n")    


class energy_offset_block:

    def __init__(self):
        self.number = "0"
        self.index  = []
        self.type   = []
        self.value  = []
        
        
    type_line = None
    
    def set_block(self,param_data, types):
        for i in range(len(param_data)):
            if "NO ENERGY OFFSETS:" in param_data[i]:
                tmp =  param_data[i].split()
                self.number = tmp[-1]
                
                type_line = i+1
                break
        
        for i in range(int(self.number)):
        
            tmp =  param_data[i+type_line].split()
    
            self.index.append(tmp[-2])
            self.value.append(tmp[-1])
            
            self.type.append(types[int(self.index[i])-1])

    def print_block(self,to="stdout"):
    
        if self.number == 0:
            return
    
        if to == "stdout":
            print("NO ENERGY OFFSETS: " + self.number)
            for i in range(int(self.number)):
                print("ENERGY OFFSET " + self.index[i] + " " + self.value[i])
            print("")
        else:
            to.write("NO ENERGY OFFSETS: " + self.number + '\n')
            for i in range(int(self.number)):
                to.write("ENERGY OFFSET " + self.index[i] + " " + self.value[i] + '\n')
            to.write("\n")        
    
        
class param_file():

    def __init__(self,template,name=""):
    
        self.name             = name

        self.bool_block       = bool_block()
        self.comp_block       = complexity_block()
        self.atm_types_block  = atm_types_block()
        self.pair_types_block = pair_types_block()
        self.fcut_block       = fcut_block()    
        self.s3b_block        = special3bmax_block()
        self.s4b_block        = special4bmax_block()
        self.clu_count_block  = clu_count_block()           
        self.maps_2b          = map_2b_block()
        self.maps_3b          = map_3b_block()
        self.maps_4b          = map_4b_block()
        self.eoffset_block    = energy_offset_block()
        
        self.bool_block      .set_block(template)
        self.comp_block      .set_block(template)
        self.atm_types_block .set_block(template)
        self.pair_types_block.set_block(template)
        self.fcut_block      .set_block(template)
        self.s3b_block       .set_block(template)
        self.s4b_block       .set_block(template)
        self.clu_count_block .set_block(template)
        self.maps_2b         .set_block(template)
        self.maps_3b         .set_block(template)
        self.maps_4b         .set_block(template)        
        self.eoffset_block   .set_block(template,self.atm_types_block.type)
        
        self.params_2b        = params_2b_block(self.pair_types_block.npair,self.comp_block.O2B)
        self.params_3b        = params_3b_block(self.clu_count_block.ntrips)               
        self.params_4b        = params_4b_block(self.clu_count_block.nquads)    
                
        self.params_2b       .set_block(template)
        self.params_3b       .set_block(template)
        self.params_4b       .set_block(template)        
        
        
        
    def print_file(self, to="stdout"):
    
        self.bool_block      .print_block(to)
        self.comp_block      .print_block(to)
        self.atm_types_block .print_block(to)
        self.pair_types_block.print_block(to)
        self.fcut_block      .print_block(to)
        self.s3b_block       .print_block(to)
        self.s4b_block       .print_block(to)
        self.clu_count_block .print_block(to)
        self.params_2b       .print_block(to)
        self.params_3b       .print_block(to)
        self.params_4b       .print_block(to)
        self.maps_2b         .print_block(to)
        self.maps_3b         .print_block(to)
        self.maps_4b         .print_block(to)
        self.eoffset_block   .print_block(to)
        
        if to == "stdout":
            print("ENDFILE\n")
        else:
            to.write("ENDFILE\n\n")
            
    def update_from(self, other):
        
        # Update the bool block -- see below for rules
        
        if self.bool_block.keys[0][1] != other.bool_block.keys[0][1]:
            print("ERROR: USECOUL mismatch")
        if self.bool_block.keys[1][1] != other.bool_block.keys[1][1]:
            print("ERROR: FITCOUL mismatch")
        try:
            if self.bool_block.keys[2][1] != other.bool_block.keys[2][1]:
               print("     WARNING: USEPOVER mismatch - setting false!") 
               self.bool_block.keys[2][1] = helpers.bool2str(False) 
        except:
            print("     USEPOVER not found in at least one file - setting both false!")
            self.bool_block.keys[2][1] = helpers.bool2str(False) 
        try:
            if self.bool_block.keys[3][1] != other.bool_block.keys[3][1]:
               print("     WARNING: FITPOVER mismatch - setting false!")  
               self.bool_block.keys[3][1] = helpers.bool2str(False) 	
        except:       
           print("     FITPOVER not found in at least one file - setting both false!")
           self.bool_block.keys[3][1] = helpers.bool2str(False) 
        if self.bool_block.keys[4][1] != other.bool_block.keys[4][1]:
            print("     WARNING: USE3BCH mismatch - setting true!")
            self.bool_block.keys[4][1] = helpers.bool2str(True)
        if self.bool_block.keys[5][1] != other.bool_block.keys[5][1]:
            print("     WARNING: USE4BCH mismatch - setting true!")
            self.bool_block.keys[5][1] = helpers.bool2str(True)
           
        # Handle for EXCLD1B
            
        if   other.bool_block.keys[6][1] == "false": # Then there should be no exclusions
               self.bool_block.keys[6][1] = "false"
        elif self .bool_block.keys[6][1] == "false": # Unexpected - only update if new parameter file provides more info
               print("ERROR: Bad logic in update bool block")
               exit(0)
        else: # Save only the exclusions that exist in both
               self.bool_block.keys[6][1] = list(set(self.bool_block.keys[6][1]) & set(other.bool_block.keys[6][1]))
               self.bool_block.keys[6][1] = ' '.join(self.bool_block.keys[6][1]).split()
               self.bool_block.keys[6][1] = sorted(self.bool_block.keys[6][1], key=int)    

        # Handle for EXCLD2B
                
        if   other.bool_block.keys[7][1] == "false": # Then there should be no exclusions
               self.bool_block.keys[7][1] = "false"
        elif self .bool_block.keys[7][1] == "false": # Unexpected - only update if new parameter file provides more info
               print("ERROR: Bad logic in update bool block")
               exit(0)
        else: # Save only the exclusions that exist in both
               self.bool_block.keys[7][1] = list(set(self.bool_block.keys[7][1]) & set(other.bool_block.keys[7][1]))  
               self.bool_block.keys[7][1] = ' '.join(self.bool_block.keys[7][1]).split()
               self.bool_block.keys[7][1] = sorted(self.bool_block.keys[7][1], key=int)              
                  
            
        # Update the model complexity block -- see below for rules
        
        self_orders  = [int(self.comp_block.O2B), int(self.comp_block.O3B), int(self.comp_block.O4B)]
        other_orders = [int(other.comp_block.O2B), int(other.comp_block.O3B), int(other.comp_block.O4B)]
        
        if self_orders[0] != other_orders[0]: # O2B
            self.comp_block.O2B = str(max(self_orders[0], other_orders[0]))
            print("     WARNING: O2B mismatch - setting to", self.comp_block.O2B)
        if self_orders[1] != other_orders[1]: # O3B
            self.comp_block.O3B = str(max(self_orders[1], other_orders[1]))
            print("     WARNING: O3B mismatch - setting to", self.comp_block.O3B)
        if self_orders[2] != other_orders[2]: # O4B
            self.comp_block.O4B = str(max(self_orders[2], other_orders[2]))
            print("     WARNING: O4B mismatch - setting to", self.comp_block.O4B)                        
            
        # Update the atom types block 
        
        if int(self.atm_types_block.ntype) < int(other.atm_types_block.ntype):
            print("ERROR: template has fewer atom types than supplement")
            exit()
            
        for i in range(int(self.atm_types_block.ntype)):
            for j in range(int(other.atm_types_block.ntype)):
                if self.atm_types_block.type[i] == other.atm_types_block.type[j]:
                    self.atm_types_block.chrg[i] = other.atm_types_block.chrg[j]
                    self.atm_types_block.mass[i] = other.atm_types_block.mass[j]
                    
        # Update the pair types block
        
        if int(self.pair_types_block.npair) < int(other.pair_types_block.npair):
            print("ERROR: template has fewer atom pairs than supplement")
            exit()
            
        for i in range(int(self.pair_types_block.npair)):
            for j in range(int(other.pair_types_block.npair)):
            
                if sorted([self.pair_types_block.type1[i],self.pair_types_block.type2[i]]) == sorted([other.pair_types_block.type1[j],other.pair_types_block.type2[j]]):
                    self.pair_types_block.rmin [i] = other.pair_types_block.rmin [j]
                    self.pair_types_block.rmax [i] = other.pair_types_block.rmax [j]
                    self.pair_types_block.xform[i] = other.pair_types_block.xform[j]
                    self.pair_types_block.lambd[i] = other.pair_types_block.lambd[j]
                    
        # Update (check) the fcut_block -- see below for rules
        
        if self.fcut_block.type != other.fcut_block.type:
            print("ERROR: fcut type mismatch")
            exit()
        if self.fcut_block.vars != other.fcut_block.vars:
            print("ERROR: fcut vars mismatch")
            exit()
        
        # Update the special 3b outer cutoff block

        # Compare all other against all self
        # If it exists in self, update cutoffs
        # Otherwise, append it to self
        
        # WARNING: This relies on chimes_lsq always converting "SPECIAL XB: ALL" to specific!!!!

        if other.s3b_block.number is not None:
        
            for i in range(int(other.s3b_block.number)):
            
                found_match = False
            
                for j in range(int(self.s3b_block.number)):
                
                    if other.s3b_block.cluster[i] == self.s3b_block.cluster[j]:

                        found_match = True
                        break
                        
                if found_match:
                
                    # Update cutoffs
                    
                    self.s3b_block.cut1[j] = other.s3b_block.cut1[i]
                    self.s3b_block.cut2[j] = other.s3b_block.cut2[i]
                    self.s3b_block.cut3[j] = other.s3b_block.cut3[i]
                    
                else:
                    # Append other to self
                    
                    self.s3b_block.number = str( int(self.s3b_block.number) + 1)
                    self.s3b_block.cluster.append(other.s3b_block.cluster[i])
                    self.s3b_block.pair1  .append(other.s3b_block.pair1  [i])
                    self.s3b_block.pair2  .append(other.s3b_block.pair2  [i])
                    self.s3b_block.pair3  .append(other.s3b_block.pair3  [i])
                    self.s3b_block.cut1   .append(other.s3b_block.cut1   [i])
                    self.s3b_block.cut2   .append(other.s3b_block.cut2   [i])
                    self.s3b_block.cut3   .append(other.s3b_block.cut3   [i])


        self.s3b_block.specific = True
        self.s3b_block.all      = False            

        # Update the special 4b outer cutoff block
        
        # Compare all other against all self
        # If it exists in self, update cutoffs
        # Otherwise, append it to self
        
        # WARNING: This relies on chimes_lsq always converting "SPECIAL XB: ALL" to specific!!!!
        
        if other.s4b_block.number is not None:
        
            for i in range(int(other.s4b_block.number)):
            
                found_match = False
            
                for j in range(int(self.s4b_block.number)):
                
                    if other.s4b_block.cluster[i] == self.s4b_block.cluster[j]:

                        found_match = True
                        break
                        
                if found_match:
                
                    # Update cutoffs
                    
                    self.s4b_block.cut1[j] = other.s4b_block.cut1[i]
                    self.s4b_block.cut2[j] = other.s4b_block.cut2[i]
                    self.s4b_block.cut3[j] = other.s4b_block.cut3[i]
                    self.s4b_block.cut4[j] = other.s4b_block.cut4[i]
                    self.s4b_block.cut5[j] = other.s4b_block.cut5[i]
                    self.s4b_block.cut6[j] = other.s4b_block.cut6[i]
                else:
                    # Append other to self
                    
                    self.s4b_block.number = str( int(self.s4b_block.number) + 1)
                    self.s4b_block.cluster.append(other.s4b_block.cluster[i])
                    self.s4b_block.pair1  .append(other.s4b_block.pair1  [i])
                    self.s4b_block.pair2  .append(other.s4b_block.pair2  [i])
                    self.s4b_block.pair3  .append(other.s4b_block.pair3  [i])
                    self.s4b_block.pair4  .append(other.s4b_block.pair4  [i])
                    self.s4b_block.pair5  .append(other.s4b_block.pair5  [i])
                    self.s4b_block.pair6  .append(other.s4b_block.pair6  [i])    
                    self.s4b_block.cut1   .append(other.s4b_block.cut1   [i])
                    self.s4b_block.cut2   .append(other.s4b_block.cut2   [i])
                    self.s4b_block.cut3   .append(other.s4b_block.cut3   [i])
                    self.s4b_block.cut4   .append(other.s4b_block.cut4   [i])
                    self.s4b_block.cut5   .append(other.s4b_block.cut5   [i])
                    self.s4b_block.cut6   .append(other.s4b_block.cut6   [i])    

        self.s4b_block.specific = True
        self.s4b_block.all      = False    
        
        
        # Update the cluster count block
        
        if self.clu_count_block.ntrips < other.clu_count_block.ntrips:
            print("ERROR: supplement file has more triplet types than template file")
            exit()
        if self.clu_count_block.nquads < other.clu_count_block.nquads:
            print("ERROR: supplement file has more quadruplet types than template file")
            exit()    
            
        # Update the maps ... actually, no updating should be necessary, since all possible pairs should already be in the template file        
            
        # Update the 2b maps
        
        if False:
        
            for i in range(int(self.maps_2b.npair)):
                
                # Check if this is even a possible pair for supplement model 
                
                skip = False
                
                for j in range(int(other.atm_types_block.ntype)):
                    for k in range(int(other.atm_types_block.ntype)):
                    
                        check = sorted(self.atm_types_block.type[j] + self.atm_types_block.type[k])

                        if check not in self.maps_2b.clusters:
                            skip = True # Then this cannot possibly be a mapped pair - skip!    

                if skip:
                    continue
                for j in range(int(other.maps_2b.npair)):
                    if self.maps_2b.clusters[i] == other.maps_2b.clusters[j]:
                        continue
        
                print("WARNING: No 2b map match found for template type",self.maps_2b.clusters[i],"... setting label to -1")
                self.maps_2b.labels[i] = -1
                
            # Update the 3b maps    
                    
            for i in range(int(self.maps_3b.ntrip)):
                
                # Check if this is even a possible pair for supplement model 
                
                skip = False
                
                for j in range(int(other.atm_types_block.ntype)):
                    for k in range(int(other.atm_types_block.ntype)):
                        for l in range(int(other.atm_types_block.ntype)):
                
                            check = sorted(
                            self.atm_types_block.type[j] + self.atm_types_block.type[k] + 
                            self.atm_types_block.type[j] + self.atm_types_block.type[l] +
                            self.atm_types_block.type[k] + self.atm_types_block.type[l])
                            
                            if check not in self.maps_3b.clusters:
                                skip = True # Then this cannot possibly be a mapped pair - skip!                

                if skip:
                    continue
                for j in range(int(other.maps_3b.ntrip)):
                    if self.maps_3b.clusters[i] == other.maps_3b.clusters[j]:
                        continue
                        
                print("WARNING: No 3b map match found for template type",self.maps_3b.clusters[i],"... setting label to -1")
                self.maps_3b.labels[i] = -1                
        
            # Update the 4b maps

            for i in range(int(self.maps_4b.nquad)):
                
                # Check if this is even a possible pair for supplement model 
                
                skip = False
                
                for j in range(int(other.atm_types_block.ntype)):
                    for k in range(int(other.atm_types_block.ntype)):
                        for l in range(int(other.atm_types_block.ntype)):
                            for m in range(int(other.atm_types_block.ntype)):

                                check = sorted(
                                self.atm_types_block.type[j] + self.atm_types_block.type[k] + 
                                self.atm_types_block.type[j] + self.atm_types_block.type[l] +
                                self.atm_types_block.type[j] + self.atm_types_block.type[m] +
                                self.atm_types_block.type[k] + self.atm_types_block.type[l] +
                                self.atm_types_block.type[k] + self.atm_types_block.type[m] +
                                self.atm_types_block.type[l] + self.atm_types_block.type[m])
                                
                                if check not in self.maps_4b.clusters:
                                    skip = True # Then this cannot possibly be a mapped pair - skip!            

                if skip:
                    continue
                for j in range(int(other.maps_4b.ntrip)):
                    if self.maps_4b.clusters[i] == other.maps_4b.clusters[j]:
                        continue
                        
                print("WARNING: No 4b map match found for template type",self.maps_4b.clusters[i],"... setting label to -1")
        
                self.maps_4b.labels[i] = -1    
            
        # Update 2b params
        
        for i in range(int(other.params_2b.npair)):
            
            for j in range(int(self.params_2b.npair)):
            
                if (other.params_2b.par2b[i].atm1 == self.params_2b.par2b[j].atm1) and (other.params_2b.par2b[i].atm2 == self.params_2b.par2b[j].atm2):
                    if other.params_2b.order > self.params_2b.order:
                        print("ERROR: Supplement has greater 2b orders than template")
                        print("template:",self.params_2b.order)
                        print("other:",other.params_2b.order)
                        exit()
                    elif other.params_2b.order < self.params_2b.order:
                        print("     WARNING: Template has more 2b params than other - setting extras to zero")
                    
                    for k in range(int(self.params_2b.order)):
                    
                        if k+1 <= int(other.params_2b.order):
                            self.params_2b.par2b[j].params[k] = other.params_2b.par2b[i].params[k]
                        else:
                            self.params_2b.par2b[j].params[k] = "0.0"
                    break
        # Update 3b params

        for i in range(int(other.params_3b.ntrips)):
            for j in range(int(self.params_3b.ntrips)):

                if other.params_3b.par3b[i].atms == self.params_3b.par3b[j].atms:
                            
                    if self.params_3b.par3b[j].excl: # This was an excluded type - need to update ALL associated info
                    
                        if not other.params_3b.par3b[i].excl:

                            self.params_3b.par3b[j].excl  = other.params_3b.par3b[i].excl    
                            self.params_3b.par3b[j].nuniq = other.params_3b.par3b[i].nuniq                    
                            self.params_3b.par3b[j].npar  = other.params_3b.par3b[i].npar

                            for k in range(int(other.maps_3b.ntrip)):
                                for l in range(int(self.maps_3b.ntrip)):
                                    if other.maps_3b.clusters[k] == self.maps_3b.clusters[l]:
                                        self.maps_3b.labels[l] = self.maps_3b.eff_labels[l]
                                    
                    elif int(other.params_3b.par3b[i].npar) > int(self.params_3b.par3b[j].npar):
                    
                        if self.params_3b.par3b[j].npar is not None:
                            print("ERROR: Supplement has more 3b params than template", other.params_3b.par3b[i].atms, other.params_3b.par3b[i].npar, self.params_3b.par3b[j].npar)
                            exit()                                    
                                    
                    else: # The supplement file was pruned, so there are fewer parameters than otherwise expected
    
                        self.params_3b.par3b[j].nuniq = other.params_3b.par3b[i].nuniq                    
                        self.params_3b.par3b[j].npar  = other.params_3b.par3b[i].npar

                    del self.params_3b.par3b[j].pairs [:]
                    del self.params_3b.par3b[j].totidx[:]
                    del self.params_3b.par3b[j].power1[:]
                    del self.params_3b.par3b[j].power2[:]
                    del self.params_3b.par3b[j].power3[:]
                    del self.params_3b.par3b[j].eqvidx[:]
                    del self.params_3b.par3b[j].powidx[:]
                    del self.params_3b.par3b[j].params[:]
                    
                    self.params_3b.par3b[j].pairs  = other.params_3b.par3b[i].pairs[:]

                    for k in range(int(other.params_3b.par3b[i].npar)):
                    
                        self.params_3b.par3b[j].totidx.append(other.params_3b.par3b[i].totidx[k])
                        self.params_3b.par3b[j].power1.append(other.params_3b.par3b[i].power1[k])
                        self.params_3b.par3b[j].power2.append(other.params_3b.par3b[i].power2[k])
                        self.params_3b.par3b[j].power3.append(other.params_3b.par3b[i].power3[k])
                        self.params_3b.par3b[j].eqvidx.append(other.params_3b.par3b[i].eqvidx[k])
                        self.params_3b.par3b[j].powidx.append(other.params_3b.par3b[i].powidx[k])
                        self.params_3b.par3b[j].params.append(other.params_3b.par3b[i].params[k])

        # Update 4b params
        
                
        for i in range(int(other.params_4b.nquads)):
            for j in range(int(self.params_4b.nquads)):

                if other.params_4b.par4b[i].atms == self.params_4b.par4b[j].atms:
                
                    if self.params_4b.par4b[j].excl: # This was an excluded type - need to update ALL associated info: # This was an excluded type - need to update ALL associated info
                    
                        if not other.params_4b.par4b[i].excl:                    
                            self.params_4b.par4b[j].excl  = other.params_4b.par4b[i].excl    
                            self.params_4b.par4b[j].nuniq = other.params_4b.par4b[i].nuniq                    
                            self.params_4b.par4b[j].npar  = other.params_4b.par4b[i].npar
                            
                            for k in range(int(other.maps_4b.nquad)):
                                for l in range(int(self.maps_4b.nquad)):
                                    if other.maps_4b.clusters[k] == self.maps_4b.clusters[l]:
                                        self.maps_4b.labels[l] = self.maps_4b.eff_labels[l]                
    
                    elif int(other.params_4b.par4b[i].npar) > int(self.params_4b.par4b[j].npar):
                    
                        if self.params_4b.par4b[j].npar is not None:
                            print("ERROR: Supplement has more 4b params than template")
                            exit()
                            
                                    
                    else: # The supplement file was pruned, so there are fewer parameters than otherwise expected
    
                        self.params_4b.par4b[j].nuniq = other.params_4b.par4b[i].nuniq                    
                        self.params_4b.par4b[j].npar  = other.params_4b.par4b[i].npar                                            

                    del self.params_4b.par4b[j].pairs [:]
                    del self.params_4b.par4b[j].totidx[:]
                    del self.params_4b.par4b[j].power1[:]
                    del self.params_4b.par4b[j].power2[:]
                    del self.params_4b.par4b[j].power3[:]
                    del self.params_4b.par4b[j].power4[:]
                    del self.params_4b.par4b[j].power5[:]
                    del self.params_4b.par4b[j].power6[:]
                    del self.params_4b.par4b[j].eqvidx[:]
                    del self.params_4b.par4b[j].powidx[:]
                    del self.params_4b.par4b[j].params[:]
                    
                    self.params_4b.par4b[j].pairs  = other.params_4b.par4b[i].pairs[:]

                    for k in range(int(other.params_4b.par4b[i].npar)):
                    
                        self.params_4b.par4b[j].totidx.append(other.params_4b.par4b[i].totidx[k])
                        self.params_4b.par4b[j].power1.append(other.params_4b.par4b[i].power1[k])
                        self.params_4b.par4b[j].power2.append(other.params_4b.par4b[i].power2[k])
                        self.params_4b.par4b[j].power3.append(other.params_4b.par4b[i].power3[k])
                        self.params_4b.par4b[j].power4.append(other.params_4b.par4b[i].power4[k])
                        self.params_4b.par4b[j].power5.append(other.params_4b.par4b[i].power5[k])
                        self.params_4b.par4b[j].power6.append(other.params_4b.par4b[i].power6[k])                        
                        self.params_4b.par4b[j].eqvidx.append(other.params_4b.par4b[i].eqvidx[k])
                        self.params_4b.par4b[j].powidx.append(other.params_4b.par4b[i].powidx[k])
                        self.params_4b.par4b[j].params.append(other.params_4b.par4b[i].params[k])    
                        
        # Update energy offsets
        
        if int(self.eoffset_block.number) == 0: # Then need to set up template
        
            self.eoffset_block.number = self.atm_types_block.ntype
            
            for i in range(int(self.eoffset_block.number)):
                self.eoffset_block.index.append(str(i+1))
                self.eoffset_block.type .append(self.atm_types_block.type[i])
                self.eoffset_block.value.append(str(0))
                        
        # Need to check if our atom type is in the template list and add/update as needed
        
        for j in range(int(other.eoffset_block.number)):
                
            found = False
                
            for i in range(int(self.eoffset_block.number)):
                
                
            
                if other.eoffset_block.type[j] == self.eoffset_block.type[i]:
                    self.eoffset_block.value[i] = other.eoffset_block.value[j]
                    found = True
            if not found:
                print("ERROR: No template energy offset match for supplement type", other.eoffset_block.type[j])
                exit()
                    


def main(base_file=None, new_files=None ):

    if (not base_file) and (not new_files) and (len(sys.argv) > 1):

        base_file = sys.argv[1]  # template
        new_files = sys.argv[2:] # supplements

    print("Building a hierarchical parameter files using:")
    print(" -", base_file, "as a template file (saving as", base_file + ".orig)")
    
    
    helpers.run_bash_cmnd("cp " + base_file + " " + base_file + ".orig")

    for i in range(len(new_files)):
        print(" -", new_files[i], "as a supplement file")
        
        # Read the first set of template/supplement files
        
        template   = helpers.readlines(base_file)
        supplement = helpers.readlines(new_files[i])
        
        # Remove comment lines

        template   = [x for x in template   if not x.startswith('!')]
        supplement = [x for x in supplement if not x.startswith('!')]
        
        # Set the output file name
        
        outname  = "hierarch." + str(i) + ".params.txt"
        ofstream = open(outname,'w')
        
        print("\t+ outname is:", outname)
        
        # Parse the template/supplement files
                
        template_file   = param_file(template, base_file)
        supplement_file = param_file(supplement, new_files[i])
        
        # Update the template with the supplemental info
        
        template_file.update_from(supplement_file)
        
        # Save the updated template to a new file
        
        template_file.print_file(to=ofstream)
        
        # Make next loop use the updated file as the new template
        
        ofstream.close()
        base_file = outname
    
    helpers.run_bash_cmnd("cp " + outname + " hierarch.params.txt")
            

if __name__ == "__main__":

    main()

        
