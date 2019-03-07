import ROOT
import PlotUtils

import math,os

class CVEvent(object):

  # Get instances of 2p2h and RPA weighters
  # It is important that this happen outside __init__() so that these implementations are common to all instances of CVEvent and its derived classes
  fitPath = '{0}/data/Reweight'.format(os.environ['MPARAMFILESROOT'])
  weight_cv_2p2h = PlotUtils.weight_2p2h('{0}/fit-mec-2d-noScaleDown-penalty00300-best-fit'.format(fitPath)) 
  weight_nn_2p2h = PlotUtils.weight_2p2h('{0}/fit-mec-2d-nn-only-noScaleDown-penalty00300-best-fit'.format(fitPath)) 
  weight_np_2p2h = PlotUtils.weight_2p2h('{0}/fit-mec-2d-np-only-noScaleDown-penalty02000-best-fit'.format(fitPath)) 
  weight_qe_2p2h = PlotUtils.weight_2p2h('{0}/fit-qe-gaussian-noScaleDown-penalty02000-best-fit'.format(fitPath)) 
  weight_cv_and_var_RPA = PlotUtils.weightRPA('{0}/outNievesRPAratio-nu12C-20GeV-20170202.root'.format(fitPath))

  ## # Open files and pull out objects for muon fuzz and other business from Lu's original analysis
  ## rockMuonHistsFile = ROOT.TFile('$CONDOR_DIR_INPUT/analysis/externalInputs/rockmuon_mc_c.root')
  ## rpaWeightHistsFile_old = ROOT.TFile('$CONDOR_DIR_INPUT/analysis/externalInputs/outNievesRPA-Carbon3GeV.root')
  ## rpaWeightHistsFile_new = ROOT.TFile('$CONDOR_DIR_INPUT/analysis/externalInputs/outNievesRPAratio-nu12C-20GeV-20170202.root')

  ## h_rock_tracker = rockMuonHistsFile.Get( "hr_fuzz_tracker" )
  ## h_rock_ecal = rockMuonHistsFile.Get( "hr_fuzz_ecal" )
  ## h_rock_hcal = rockMuonHistsFile.Get( "hr_fuzz_hcal" )
  ## h_rpa_weight = rpaWeightHistsFile_old.Get( "hrelratio" )
  ## hRPArelratio = rpaWeightHistsFile_new.Get( "hrelratio" )
  ## hRPAnonrelratio = rpaWeightHistsFile_new.Get( "hnonrelratio" )
  ## 
  ## h_rock_tracker.SetDirectory(0)
  ## h_rock_ecal.SetDirectory(0)
  ## h_rock_hcal.SetDirectory(0)
  ## h_rpa_weight.SetDirectory(0)
  ## hRPArelratio.SetDirectory(0)
  ## hRPAnonrelratio.SetDirectory(0)

  def __init__(self,chain,Truth=False,treeName='NukeCC'):
    self.chain = chain
    self.Truth = Truth
    self.treeName = treeName

  def getBackgroundWeight(self):
    return 1

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

  def getNonResonantPionWeight_Old(self):
    return 1+(57.0/50)*(self.chain.truth_genie_wgt_Rvn1pi[2]-1)

  def getRPAWeight(self,var=0):

    ## Variations
    #0 CV value
    #1 hq2pos
    #2 hq2neg
    #3 lq2pos
    #4 lq2neg

    if not self.chain.mc_intType == 1:  return 1 # Only calculate RPA weight if event is CCQE
    if self.chain.mc_targetZ < 6:       return 1 # Intranuclear correlations don't occur in hydrogen
  
    q0 = self.getTrueQ0()
    q3 = self.getTrueQ3()

    if var == 0: return CVEvent.weight_cv_and_var_RPA.getWeight(q0,q3)
    if var == 1: return CVEvent.weight_cv_and_var_RPA.getWeightHighQ2(q0,q3,1)
    if var == 2: return CVEvent.weight_cv_and_var_RPA.getWeightHighQ2(q0,q3,-1)
    if var == 3: return CVEvent.weight_cv_and_var_RPA.getWeightLowQ2(q0,q3,1)
    if var == 4: return CVEvent.weight_cv_and_var_RPA.getWeightLowQ2(q0,q3,-1)

    print "I'm inside getRPAWeight, but I shouldn't have gotten this far!"
    return
   
  def getRPAWeight_Old(self):

    if not self.chain.mc_intType == 1: return 1.0

    q3 = math.sqrt( (self.chain.mc_incomingE-self.chain.mc_primFSLepton[3]) ** 2 + self.chain.mc_Q2 )/1000.
    
    tmp_q3 = q3
    tmp_q0 = ( self.chain.mc_incomingE - self.chain.mc_primFSLepton[3] )/1000.

    if tmp_q3 > 1.2:        tmp_q3 = 1.2
    if tmp_q0 > 1.2:        tmp_q0 = 1.2
    if tmp_q0 < 17.0/1000:  tmp_q0 = 17.0/1000    

    q0q3bin = CVEvent.h_rpa_weight.FindFixBin(tmp_q3,tmp_q0)
    wgt = CVEvent.h_rpa_weight.GetBinContent(q0q3bin)

    return(wgt if 1.0e-6 < wgt and wgt < 2.0 else 1.0)

  def getMinosEffWeight(self):
    if eval('self.chain.%s_minos_trk_p/1000'%self.treeName) < 3.0:  return 0.966#0.971*0.995
    else:                                       return 0.990#0.994*0.995
 
  def get2p2hWeight(self,var=0):

    ## Variations
    #0 CV value
    #1 nn+pp pairs only
    #2 np pair only
    #3 qe 1p1h variation
    #4 wgt = 1

    if var == 4: return 1.0
    
    # Only proceed to calculate 2p2h weight if event is CCQE (mc_intType == 1) or MEC (mc_intType == 8)
    if not (self.chain.mc_intType == 1 or self.chain.mc_intType == 8): return 1.0 
   
    applyOn2p2h = True if (var == 0 or var == 1 or var ==2) else False
    applyOn1p1h = True if (var == 3) else False

    # Target analysis
    target = self.chain.mc_targetNucleon
    isnnorpp = True if (target-2000000200 == 0 or target-2000000200 == 2) else False 
    isnp = True if (target-2000000200 == 1) else False

    ## Handle the various permutations in which a weight shouldn't be applied
    # If CCQE and don't apply 1p1h, don't apply weights
    if self.chain.mc_intType == 1 and not applyOn1p1h: return 1.0
    # If MEC and don't apply 2p2h, don't apply weights
    if self.chain.mc_intType == 8 and not applyOn2p2h: return 1.0
    # If MEC and do apply 1p1h, don't apply weights
    if self.chain.mc_intType == 8 and applyOn1p1h: return 1.0
    # Variation 1 is for nn/pp only interactions
    if var == 1 and not isnnorpp: return 1.0
    # Variation 2 is for np only interactions
    if var == 2 and not isnp: return 1.0

    q0 = self.getTrueQ0()
    q3 = self.getTrueQ3()

    #return self.weight_2p2h.getWeight(q0,q3)

    if var == 0: return CVEvent.weight_cv_2p2h.getWeight(q0,q3)
    if var == 1: return CVEvent.weight_nn_2p2h.getWeight(q0,q3)
    if var == 2: return CVEvent.weight_np_2p2h.getWeight(q0,q3)
    if var == 3: return CVEvent.weight_qe_2p2h.getWeight(q0,q3)
    
    print "I'm inside get2p2hWeight, but I shouldn't have gotten this far!"
    return

  def getWeight(self):
    #return 1.0
    minosWeight = 1.0 if self.Truth else self.getMinosEffWeight()
    return self.getBackgroundWeight() * minosWeight * self.getNonResonantPionWeight() * self.getRPAWeight() * self.get2p2hWeight() * self.chain.wgt

  def getRobWeight(self):
    return self.getWeight()

  def getLuWeight(self,newRPA=False,newNonResPi=False,weight_2p2h=False):
    localRPAWeight = self.getRPAWeight() if newRPA else self.getRPAWeight_Old()
    localNonResPiWeight = self.getNonResonantPionWeight() if newNonResPi else self.getNonResonantPionWeight_Old()
    weight_2p2h = self.get2p2hWeight() if weight_2p2h else 1.0
    minosWeight = 1.0 if self.Truth else self.getMinosEffWeight()
    return self.getBackgroundWeight() * minosWeight * localRPAWeight * localNonResPiWeight * self.chain.wgt

  def getInt(self,branch_name):
    return self.chain.GetInt(branch_name,chain.entry)

  def getDouble(self,branch_name):
    return self.chain.GetValue(branch_name,chain.entry)

  def getVecElem(self,branch_name,i):
    return self.chain.GetValue(branch_name,chain.entry,i)

  def shortName(self):
    return "cv"

  def latexName(self):
    return "Central value"

  def setEntry(self,entry):
    self.entry = entry
    self.chain.LoadTree(entry)

  def getTrueNeutrinoE(self):
    Enu_true = self.chain.mc_incomingE
    return Enu_true/1000

  def getNeutrinoE(self):
    #Enu = eval('self.chain.%s_E'%self.treeName)
    Enu = self.getRecoMuonE() + self.getRecoHadronE()
    return Enu

  def getTrueMuonE(self):
    Emu = self.chain.mc_primFSLepton[3]
    return Emu/1000

  def getTrueHadronE(self):
    Ehad_true = (self.chain.mc_incomingE-self.chain.mc_primFSLepton[3])
    return Ehad_true/1000

  def getHadronE(self):
    # add Lu's modifications to get final Ehadron?
    Ehad = eval('self.chain.%s_nu_energy_recoil'%self.treeName)
    return Ehad/1000

  def fuzzCorrect(self):
    # lifted directly from Lu's code...not so sure what's going on here 
    frac_tracker = [0.977,0.917,0.793,0.60,0.271]
    frac_ecal = [0.996,0.98,0.937,0.826,0.469]
    frac_hcal = [0.999,0.998,0.991,0.965,0.749]
    upper = [0.3,0.5,1,2,9999]
    lower = [0,0.3,0.5,1,2]
    Ehad = eval('self.chain.%s_nu_energy_recoil'%self.treeName)
    Ecorr_tracker = self.chain.E_corr_tracker_lu
    Ecorr_ecal = self.chain.E_corr_ecal_lu
    Ecorr_hcal = self.chain.E_corr_hcal_lu
    for i in range(5):
      if Ehad/1000 < upper[i] and Ehad/1000 >= lower[i]:
        E_fuzz = Ecorr_tracker*frac_tracker[i] + Ecorr_ecal*frac_ecal[i] + Ecorr_hcal*frac_hcal[i]
    if Ehad - E_fuzz < 0: #I guess E_fuzz has units of MeV, not GeV
      E_fuzz = 0;
    
    return E_fuzz

  def rockMuonCorrect(self):
    # lifted directly from Lu's code...not so sure what's going on here
    angle = math.cos(self.chain.primary_track_minerva_theta)
    Ehad_cylinder = eval('self.chain.%s_nu_energy_recoil'%self.treeName)-self.fuzzCorrect()
  
    E_all = Ehad_cylinder + 1 # start with E_all that is by definition > Ehad_cylinder, so loop is entered 
    while E_all >= Ehad_cylinder:
      corr_tracker = CVEvent.h_rock_tracker.GetRandom()
      corr_ecal = CVEvent.h_rock_ecal.GetRandom()
      corr_hcal = CVEvent.h_rock_hcal.GetRandom()
      E_tracker = corr_tracker*self.chain.muon_length_tracker/angle*0.43
      #E_ecal=corr_ecal*self.chain.muon_length_ecal/angle
      E_ecal = 0
      E_hcal = corr_hcal*self.chain.muon_length_hcal/angle*0.05
      E_all = (E_tracker+E_ecal+E_hcal)/1.5678*1.60504

    return E_all;

  def vertexShiftCorrect(self):
    # lifted directly from Lu's code...not so sure what's going on here
    
    z_mod_25 = 5911.2 ## Z center of module 25
    z_mod_75 = 8172.7 ## Z center of module 75
    
    ## vertex module
    reco_vtx = eval('self.chain.%s_vtx'%self.treeName)
    vtx_m = int(round(25.0+50.0/(z_mod_75-z_mod_25)*(reco_vtx[2]-z_mod_25)))
    new_vtx_m = vtx_m
    
    ## # of module gaps
    gap = 0

    ## step upstream in detector
    m = vtx_m - 1
    while m > 0:
      ## project muon to module
      pz = z_mod_25 + (m-25)/50.0*(z_mod_75-z_mod_25)
      trackStartPos = self.chain.primary_track_minerva_start_position
      trackEndPos = self.chain.primary_track_minerva_end_position
      mx = trackStartPos[0] - trackEndPos[0]
      my = trackStartPos[1] - trackEndPos[1]
      mz = trackStartPos[2] - trackEndPos[2]
      dz = pz - trackEndPos[2]
      px = trackEndPos[0] + mx/mz*dz
      py = trackEndPos[1] + my/mz*dz
      pu = px/2.0 - py*math.sqrt(3.0)/2.0 ## v.dot(u_hat)
      pv = px/2.0 + py*math.sqrt(3.0)/2.0 ## v.dot(v_hat)
      ## sum (recoil) energy in module, in cone upstream of muon
      nrg = 0.0
      strip_pitch = 16.74
      sx = 64.0 + px/strip_pitch
      su = 64.0 + pu/strip_pitch
      sv = 64.0 + pv/strip_pitch
     
      recoil_clus_id_module = self.chain.recoil_clus_id_module
      recoil_clus_id_time = self.chain.recoil_clus_id_time 
      recoil_clus_id_type = self.chain.recoil_clus_id_type
      recoil_clus_id_energy = self.chain.recoil_clus_id_energy
      recoil_clus_id_view = self.chain.recoil_clus_id_view
      recoil_clus_id_strip = self.chain.recoil_clus_id_strip     
 
      for h in range(self.chain.n_recoil_clus_id):
        
        if not recoil_clus_id_module[h] == m:   continue
        if -20.0 > recoil_clus_id_time[h]:      continue
        if recoil_clus_id_time[h] > 35.0:       continue
        if recoil_clus_id_type[h] == 5:         continue
        if recoil_clus_id_type[h] == 2:         continue
        if recoil_clus_id_energy[h] <= 1.5:     continue
        
        if(( recoil_clus_id_view[h] == 1 and abs( recoil_clus_id_strip[h] - sx ) < 0.5 * ( vtx_m - m ) ) or
           ( recoil_clus_id_view[h] == 2 and abs( recoil_clus_id_strip[h] - su ) < 0.5 * ( vtx_m - m ) ) or
           ( recoil_clus_id_view[h] == 3 and abs( recoil_clus_id_strip[h] - sv ) < 0.5 * ( vtx_m - m ) )):
     
          nrg += recoil_clus_id_energy[h]
      
      ## if energy > threshold, shift vertex upstream
      if nrg > 0.0:
        reco_vtx[0] = px
        reco_vtx[1] = py
        reco_vtx[2] = pz
        new_vtx_m = m
        gap = 0
      
      ## else we have a gap
      else:
        gap += 1
        if gap > 2: break
      
      m -= 1 
    ## End while loop 
    
    ## correct muon energy and nu
    MEU = 3.0 ## approximate energy deposition of muon in active scintillator of one plane
    n_planes = 2 * ( vtx_m - new_vtx_m )
    vtx_shift_correction = 1.222 * MEU * n_planes
  
    if reco_vtx[2] < 5990: return -1
 
    return vtx_shift_correction  

  def getRecoMuonE(self):
    #Emu_nom = eval('self.chain.%s_leptonE[3]'%self.treeName)
    #fuzzCorrection = self.fuzzCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
    #rockMuonCorrection = self.rockMuonCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
    #vertexShiftCorrection = self.vertexShiftCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
    
    #return (Emu_nom + fuzzCorrection + rockMuonCorrection + vertexShiftCorrection)/1000

    Emu_nom = eval('self.chain.%s_leptonE[3]'%self.treeName)
    
    return Emu_nom
    
    

  def getRecoMuonELessFuzzAndRockMuonCorrections(self):
    Emu_nom = eval('self.chain.%s_leptonE[3]'%self.treeName)
    vertexShiftCorrection = self.vertexShiftCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0

    return (Emu_nom + vertexShiftCorrection)/1000
 
  def getRecoHadronE(self):
    Ehad_nom = eval('self.chain.%s_nu_energy_recoil'%self.treeName)
    fuzzCorrection = self.fuzzCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
    rockMuonCorrection = self.rockMuonCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
    vertexShiftCorrection = self.vertexShiftCorrect() if not (self.treeName == 'NukeCC' or self.treeName == 'MECAna') else 0
 
    return (Ehad_nom - fuzzCorrection - rockMuonCorrection - vertexShiftCorrection)/1000
 
class MuonEShiftEvent(CVEvent):

  def __init__(self,chain,nsigma,treeName='NukeCC'):
    CVEvent.__init__(self,chain,treeName=treeName)
    self.nsigma = nsigma

  # We override just the function which corresponds to the variable
  # we're shifting. In this case, I'm supposing that the hadronic
  # energy scale uncertainty is 15%. The call to Event::getHadronE()
  # forces the use of the function in the base class, ie the
  # unshifted version read from disk
  def getRecoMuonE(self):
    oldE = super(MuonEShiftEvent,self).getRecoMuonE()
    return (1+0.02*self.nsigma)*oldE

  def shortName(self):
    return "EMuonScale"

  def latexName(self):
    return "Muon Energy Scale"

class SU_2p2hShiftEvent(CVEvent):

  def __init__(self,chain,var,treeName='NukeCC',Truth=False):
    CVEvent.__init__(self,chain,treeName=treeName,Truth=Truth)
    self.var = var

  # Overwrite get2p2hWeight() method of the base class to instead get the weight corresponding to a systematic universe variation
  def get2p2hWeight(self):
    return super(SU_2p2hShiftEvent,self).get2p2hWeight(self.var)

  def shortName(self):
    return "2p2hSysUniv"

  def latexName(self):
    return "2p2h Systematic Universe"

class RPAShiftEvent(CVEvent):

  def __init__(self,chain,var,treeName='NukeCC',Truth=False):
    CVEvent.__init__(self,chain,treeName=treeName,Truth=Truth)
    self.var = var 

  # Overwrite getRPAWeight() method of the base class to instead get the weight corresponding to a systematic universe variation
  def getRPAWeight(self):
    return super(RPAShiftEvent,self).getRPAWeight(self.var)

  def shortName(self):
    return "RPASysUniv"

  def latexName(self):
    return "RPA Systematic Universe"

##--------------------------------------------------------------------------
## Examples below, throw out?

# An example of a vertical shift, where we just change the weight
class NormShiftEvent(CVEvent):

  def __init__(self,chain,nsigma):
    CVEvent.__init__(self,chain)
    self.nsigma = nsigma

  def getWeight(self):
    return (1+0.10*self.nsigma)*super(NormShiftEvent,self).getWeight()

  def shortName(self):
    return "norm"

  def latexName(self):
    return "Normalization"

class MuonERangeCurvatureShiftEvent(CVEvent):

  def __init__(self,chain,nsigma):
    CVEvent.__init__(self,chain)
    self.nsigma = nsigma

  def getTrueMuonE(self):
    muon_E_shift = eval('self.chain.%s_minosRangeCurveShift'%self.treeName)
    shift_val = self.nsigma*muon_E_shift
    return shift_val+super(MuonERangeCurvatureShiftEvent,self).getTrueMuonE()

# An example of a lateral shift, where we have to change the value of
# one variable (in this case, hadronic energy). We need to give the
# number of sigma to the constructor
class HadronEShiftEvent(CVEvent):

  def __init__(self,chain,nsigma):
    CVEvent.__init__(self,chain)
    self.nsigma = nsigma

  # We override just the function which corresponds to the variable
  # we're shifting. In this case, I'm supposing that the hadronic
  # energy scale uncertainty is 15%. The call to Event::getHadronE()
  # forces the use of the function in the base class, ie the
  # unshifted version read from disk
  def getHadronE(self):
    oldE = super(HadronEShiftEvent,self).getHadronE()
    #print 'HadronEShiftEvent getHadronE: ' , (1+0.15*self.nsigma)*oldE
    #return (1+0.15*self.nsigma)*super(HadronEShiftEvent,self).getHadronE()
    return (1+0.15*self.nsigma)*oldE

  def shortName(self):
    return "EhadScale"

  def latexName(self):
    return "Hadronic Energy Scale"

