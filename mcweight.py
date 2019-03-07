#!/usr/bin/env python

import os, ROOT, sys, uuid

from array import *
#from lists import *
import math

#import MCReweight

class MCweight(object):
    
    def __init__(self):
        
        mparalocation = os.getenv("MPARAMFILESROOT")
        dir_data = mparalocation+"/data/Reweight/"
        #lowrecoil_wt = MCReweight.weight_2p2h(dir_data+"/fit-mec-2d-noScaleDown-penalty00300-best-fit")
        rpaWeightHistsFile_new = ROOT.TFile(dir_data+"/outNievesRPAratio-nu12C-20GeV-20170202.root")
       
        self.hRPArelratio = rpaWeightHistsFile_new.Get( "hrelratio" )
        self.hRPAnonrelratio = rpaWeightHistsFile_new.Get( "hnonrelratio" )
        
        #dump contents of RPA weights TFile to a dictionary of keys to the objects in the file
        keyDict = {}
        for key in rpaWeightHistsFile_new.GetListOfKeys(): keyDict[key.GetName()] = key.ReadObjectAny(ROOT.TClass.GetClass("TArrayD"))
        self.rpapolyrel_temp = ROOT.TPython.ObjectProxy_FromVoidPtr(keyDict["rpapolyrel"],"TArrayD")
        self.rpapolyrel = self.rpapolyrel_temp.GetArray()
        self.rpapolynonrel_temp = ROOT.TPython.ObjectProxy_FromVoidPtr(keyDict["rpapolynonrel"],"TArrayD")
        self.rpapolynonrel = self.rpapolynonrel_temp.GetArray()
        
        self.hRPArelratio.SetDirectory(0)
        self.hRPAnonrelratio.SetDirectory(0)


    def getWeightQ2(self, mc_Q2, relORnonrel):
        
        if mc_Q2 < 0.0: return 1.0
        if mc_Q2 > 9.0: return 1.0
        
        """
        ## this one returns just the polynomial Q2 version
        ## for special tests.  Poor answer for baseline MINERvA QE events.
        ## No uncertainty assigned to this usecase at this time.
        ##double gevmev = 0.001;  // minerva sends in MeV.
        """
        Q2gev = mc_Q2
        powerQ2 = 1.0
        thisrwtemp = 0.0
        
        for ii in range(10):
            if relORnonrel: thisrwtemp += self.rpapolyrel[ii]*powerQ2
            else: thisrwtemp += self.rpapolynonrel[ii]*powerQ2
            powerQ2 *= Q2gev
    
        return thisrwtemp

        """    
        def getTrueQ0(self):
            mc_incomingPartVec = self.chain.mc_incomingPartVec
            mc_primFSLepton = self.chain.mc_primFSLepton
            q0 = mc_incomingPartVec[3] - mc_primFSLepton[3]
            return q0/1000

        def getTrueQ3(self):
            mc_incomingPartVec = self.chain.mc_incomingPartVec
            mc_primFSLepton = self.chain.mc_primFSLepton
            px = mc_primFSLepton[0] - mc_incomingPartVec[0]
            py = mc_primFSLepton[1] - mc_incomingPartVec[1]
            pz = mc_primFSLepton[2] - mc_incomingPartVec[2]
            q3 = math.sqrt( px**2 + py**2 + pz**2 )
            return q3/1000

        def getNonResonantPionWeight(self):
            isGenieNonRes1pi = self.chain.truth_genie_wgt_Rvn1pi[2] < 1.0 or self.chain.truth_genie_wgt_Rvp1pi[2] < 1.0
            if isGenieNonRes1pi:  return 0.43#errors are +/- 3%ish
            else:                 return 1
            """
        
    def getRPAWeightSource(self,mc_q0,mc_q3,weights=0):
    ## the construction here is that the histogram bins
    ## line up in mev-sized steps e.g. from 0.018 to 0.019
    ## and the value stored is the value at bin-center.
        
        gevlimit = 3. ## upper limit for 2d
        rpamevlimit = gevlimit*1000.
        Q2gev = mc_q3**2-mc_q0**2
        q3bin = mc_q3*1000.
        q0bin = mc_q0*1000.
        if mc_q0 >= gevlimit: q0bin = rpamevlimit - 1
        if mc_q3 >= gevlimit: q3bin = rpamevlimit - 1
        
    ## Nieves does not calculate anything below binding energy.
    ## I don't know what GENIE does, but lets be soft about this.
    ## Two things lurking here at once.
    ## One, we are taking out a 10 MeV offset between GENIE and Valencia.
    ## Second, we are protecting against being asked for a weight that is too low in q0.
    ## It actually shouldn't happen for real GENIE events,
    ## but this protection does something that doesn't suck, just in case.
    ## you would see the artifact in a plot for sure, but better than writing 1.0.

    ##DGR - conclusion from discussion between Rik, Clarence Wret, and Dan is this offset needs to be 27 and not 10 for the NX era (GENIE version 2.12.X).
    ##DGR update. Eroica based analysis still wants 10 so I will keep it commented out
    #    q0offsetValenciaGENIE = 10
        q0offsetValenciaGENIE = 27
        if mc_q0 < 0.018: q0bin = 18+q0offsetValenciaGENIE
        
        q3bin_processed = int(q3bin)
        q0bin_processed = int(q0bin-q0offsetValenciaGENIE)
        thisrwtemp = self.hRPArelratio.GetBinContent(q3bin_processed,q0bin_processed)
        
    ## now trap bogus entries.  Not sure why they happen, but set to 1.0 not 0.0
        if thisrwtemp <= 0.001: thisrwtemp = 1.0
        
    ## events in genie but not in valencia should get a weight
    ## related to a similar q0 from the bulk distribution.
        if mc_q0 < 0.15 and thisrwtemp > 0.9:
            q3bin_processed = int(q3bin+150)
            q0bin_processed = int(q0bin-q0offsetValenciaGENIE)
            thisrwtemp = self.hRPArelratio.GetBinContent(q3bin_processed, q0bin_processed)
            
        if Q2gev >= 9.0:
            thisrwtemp = 1.0
        elif Q2gev > 3.0:
      ## hiding option, use the Q2 parameterization everywhere
      ## } else if(Q2gev > 3.0 || rwRPAQ2) {
      ## turn rwRPAQ2 all the way on to override the 2D histogram
      ## illustrates the old-style Q2 suppression many folks still use.
            
            thisrwtemp = self.getWeightQ2(Q2gev,True)
                
        if not (thisrwtemp >= 0.001 and thisrwtemp <= 2.0): thisrwtemp = 1.0
        
    ## hiding option, turn off the enhancement.
    ##if(rwoffSRC && thisrwtemp > 1.0)thisrwtemp = 1.0;

        if weights == 0: return thisrwtemp
    ## if this was called without passing an array,
    ## the user didn't want us to calculate the +/- 1-sigma bounds
    ## so the above line returned before even trying.
                
        weights[0] = thisrwtemp
                
        if thisrwtemp < 1.0:
      ## make the suppression stronger or weaker to muon capture uncertainty
      ## rwRPAonesig is either +1 or -1, which is 0.25 (25%).
      ## possible to be re-written to produce 2 and 3 sigma.
      
            weights[1] = thisrwtemp + 1.0 * (0.25)*(1.0 - thisrwtemp)
            weights[2] = thisrwtemp - 1.0 * (0.25)*(1.0 - thisrwtemp)
      
        else:
            weights[1] = thisrwtemp
            weights[2] = thisrwtemp
    
    ##std::cout << "check " << thisrwtemp << " " << weights[1] << " " << weights[2] << std::endl;
            
    ## Construct the rest of the error bands on the low Q2 suppression.
    ## this involves getting the weight from the non-relativistic ratio
            
    ##if (type == 2){
            
        thisrwEnhP1 = 1.0
        thisrwEnhM1 = 1.0
    
    ## make enhancement stronger or weaker to Federico Sanchez uncertainty
    ## this does NOT mean two sigma, its overloading the option.
        thisrwextreme = self.hRPAnonrelratio.GetBinContent(q3bin,q0bin-q0offsetValenciaGENIE)
    ## now trap bogus entries.  Not sure why they happen, but set to 1.0 not 0.0
        if thisrwextreme <= 0.001: thisrwextreme = 1.0
    
        if mc_q0 < 0.15 and thisrwextreme > 0.9:
            thisrwextreme = self.hRPAnonrelratio.GetBinContent(q3bin+150, q0bin-q0offsetValenciaGENIE)
    
    ##std::cout << "ext " << thisrwextreme << " " << thisrwtemp << std::endl;
            
    ## get the same for the Q2 dependent thing,
    ## but from the nonrelativistic polynomial
    
        if Q2gev >= 9.0:
            thisrwextreme = 1.0
        elif Q2gev > 3.0:
            thisrwextreme = self.getWeightQ2(Q2gev,False)
    
        if not (thisrwextreme >= 0.001 and thisrwextreme <= 2.0): thisrwextreme = 1.0
    
        RelToNonRel = 0.6
    
    ## based on some distance between central value and extreme
        thisrwEnhP1 = thisrwtemp + RelToNonRel * (thisrwextreme-thisrwtemp)
        thisrwEnhP1max = thisrwextreme
    
        if Q2gev < 0.9: thisrwEnhP1 += 1.5*(0.9 - Q2gev)*(thisrwEnhP1max - thisrwEnhP1)
    ## sanity check, don't let the upper error bound go above the nonrel limit.
        if thisrwEnhP1 > thisrwEnhP1max: thisrwEnhP1 = thisrwEnhP1max
    ## don't let positive error bound be closer than 3% above the central value
    ## will happen at very high Q2 and very close to Q2 = 0
        if thisrwEnhP1 < thisrwtemp + 0.03: thisrwEnhP1 = thisrwtemp + 0.03
    
        thisrwEnhM1 = thisrwtemp - RelToNonRel * (thisrwextreme-thisrwtemp)
    ## don't let negative error bound be closer than 3% below the central value
        if thisrwEnhM1 > thisrwtemp - 0.03: thisrwEnhM1 = thisrwtemp - 0.03
    ## even still, don't let the lower error bound go below 1.0 at high-ish Q2
        if Q2gev > 1.0 and thisrwEnhM1 < 1.0: thisrwEnhM1 = 1.0
    
    ## whew.  so now return the main weight
    ## and return the array of all five weights in some array
    ## thisrwtemp, thisrwSupP1, thisrwSupM1, thisrwEnhP1, thisrwEnhM1
        
        weights[3] = thisrwEnhP1;
        weights[4] = thisrwEnhM1;
    
    ## still return the central value
        return thisrwtemp;
  
    def getRPAWeight(self, intType, targetZ, q0, q3):

        if not intType == 1:  return 1 # Only calculate RPA weight if event is CCQE
        if targetZ < 6:       return 1 # Not sure what this one is about
        
        #q0 = self.getTrueQ0()
        #q3 = self.getTrueQ3()

        return self.getRPAWeightSource(q0,q3) 


    def get2p2hWeight(self, intType, q0, q3):

        #if not (self.chain.mc_intType == 1 or self.chain.mc_intType == 8):
        #if not (intType == 1 or intType == 8):
        if not (intType == 8):
            return 1 # Only calculate 2p2h weight if event is CCQE (mc_intType == 1) or MEC (mc_intType == 8)

        #q0 = self.getTrueQ0()
        #q3 = self.getTrueQ3()

    # I should be pulling these values from $MPARAMFILES/Reweight/fit-mec-2d-noScaleDown-penalty00300-best-fit.txt
        norm = 10.5798
        meanq0 = 0.254032
        meanq3 = 0.50834
        sigmaq0 = 0.0571035
        sigmaq3 = 0.129051
        corr = 0.875287
    #1 #unused fit parameters?
    #948.715
    #0.111931
        
        z = (q0-meanq0)**2/(sigmaq0**2) + (q3-meanq3)**2/(sigmaq3**2) - 2*corr*(q0-meanq0)*(q3-meanq3)/(sigmaq0*sigmaq3)
        return norm*math.exp(-0.5*z/(1-corr**2)) + 1


