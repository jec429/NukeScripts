import ROOT
from math import sqrt,sin,cos
import time
import mcweight
import os

TARGET1OFFSET = 0.43
TARGET2OFFSET = 0.35
TARGET3OFFSET = 0.51
TARGET4OFFSET = 0.00
TARGET5OFFSET = 0.20

tracker_face = 5990
tracker_back = 8340
numi_beam_angle_rad = -0.05887


ROOT.TH1.AddDirectory(False)


def isInHexagon( x, y, apothem ):
   lenOfSide = apothem*(2/sqrt(3)); 
   slope     = (lenOfSide/2.0)/apothem;
   xp        = abs(x);
   yp        = abs(y);
   
   if( (xp*xp + yp*yp) < apothem*apothem ):             return True;
   elif( xp <= apothem and yp*yp < lenOfSide/2.0 ):     return True; 
   elif( xp <= apothem and yp < lenOfSide-xp*slope ):   return True;

   return False

def target_true_vtx_z(z, target, targetz):
    fudge = 5;
    if ((target == -1 or target == 1) and z < 4478.016 + TARGET1OFFSET + 25.75 / 2 + fudge and z > 4478.016 + TARGET1OFFSET - 25.75 / 2 - fudge): return True;
    elif ((target == -1 or target == 2) and z < 4698.824 + TARGET2OFFSET + 25.75 / 2 + fudge and z > 4698.824 + TARGET2OFFSET - 25.75 / 2 - fudge): return True;
    elif ((target == -1 or target == 4) and z < 5644.74 + TARGET4OFFSET + 25.75 / 2 + fudge and z > 5644.74 + TARGET4OFFSET - 25.75 / 2 - fudge): return True;
    elif ((target == -1 or target == 5) and z < 5774.32 + TARGET5OFFSET + 25.75 / 2 + fudge and z > 5774.32 + TARGET5OFFSET - 25.75 / 2 - fudge): return True;
    elif ((target == -1 or target == 6) and z > 5170 and z < 5440): return True;
    elif (target == -1 or target == 3):
	if (targetz == 6 and z < 4940.82 + TARGET3OFFSET + 76.3 / 2  and z > 4940.82 + TARGET3OFFSET - 76.3 / 2): return True;
	elif (z < 4915.595 + TARGET3OFFSET + 25.75 / 2 + fudge and z > 4915.595 + TARGET3OFFSET - 25.75 / 2 - fudge): return True;  
    return False;

def is_scintillator(mc_vtx, targetz):
    if (target_true_vtx_z(mc_vtx[2], -1, targetz)): return False;
    if not isInHexagon(mc_vtx[0], mc_vtx[1], 850.0): return False;
    return True;

def passVertexZCut( x, y, z, apothem ):
   if isInHexagon(x,y,apothem):
      if z >= 4467.19 and z <= 4510.09 :   return True;
      elif z >= 4688.26 and z <= 4731.16 : return True;
      elif z >= 4892.41 and z <= 4972.00 : return True;
      elif z >= 5630.80 and z <= 5664.80 : return True;
      elif z >= 5756.71 and z <= 5801.24 : return True;
      #elif z >= tracker_face and z <= tracker_back : return True;
   return False;

def target1_cut(z):   
   if z > 4510 and z < 4520:
      return True
   else:
      return False

def target1_scint_cut(z):
   if z > 4530 and z < 4570:
      return True
   else:
      return False

def target2_cut(z):
   if z > 4730 and z < 4740:
      return True
   else:
      return False

def target2_scint_cut(z):
   if z > 4750 and z < 4790:
      return True
   else:
      return False

def target3_cut(z):
   if z > 4990 and z < 5010:
      return True
   else:
      return False

def target3_scint_cut(z):
   if z > 5010 and z < 5060:
      return True
   else:
      return False

def target4_cut(z):
   if z > 5450 and z < 5460:
      return True
   else:
      return False

def target4_scint_cut(z):
   if z > 5470 and z < 5510:
      return True
   else:
      return False

def target5_cut(z):
   if z > 5670 and z < 5690:
      return True
   else:
      return False

def target5_scint_cut(z):
   if z > 5690 and z < 5730:
      return True
   else:
      return False

def pass_cuts(e):
   if e.vtx[2] < 4467.19: return False
   if e.vtx[2] > 6000: return False
   if e.muon_muonutils_isrockmuon==1: return False
   if e.NukeCCQETwoTrack_muon_theta > 0.35: return False
   if e.improved_nmichel > 0: return False
   if not isInHexagon(e.vtx[0],e.vtx[1],850): return False
   
   #if e.NukeCCQETwoTrack_proton_E != -1: return False
   #if e.FailContainedProng == 0: return False
   #if not passVertexZCut(e.vtx[0],e.vtx[1],e.vtx[2],850): return False

   #if e.NukeCCQETwoTrack_muon_q2 > 40e3: return False

   return True

def getChains(cname,playlist):
   t_mc   = ROOT.TChain(cname)
   t_data = ROOT.TChain(cname)
   t_mc.Add('/minerva/data/users/jchaves/googoo/pruned_'+playlist+'_minerva_00126*.root')
   #t_data.Add('~/data/googoo/pruned_NukeCCQETwoTrack_minerva_run00022*-00022*.root')
   t_data.Add('/minerva/data/users/jchaves/googoo/pruned_'+playlist+'_minerva_00022*-00022*.root')
   return t_mc, t_data
   
def getPOT(playlist):
   pot_mc_t = 0.0
   pot_mc_u = 0.0
   pot_data = 0.0

   t_mc, t_data = getChains('Meta', playlist)
   
   for e in t_mc:
      pot_mc_u += e.POT_Used
   for e in t_mc:
      pot_mc_t += e.POT_Total
   for e in t_data:
      pot_data += e.POT_Used
   print pot_mc_t,pot_mc_u,pot_data

   return pot_mc_u,pot_data,pot_mc_t

def getTrueQ0(entry):
   mc_incomingPartVec = entry.mc_incomingPartVec
   mc_primFSLepton = entry.mc_primFSLepton
   q0 = mc_incomingPartVec[3] - mc_primFSLepton[3]
   return q0/1000

def getTrueQ3(entry):
   mc_incomingPartVec = entry.mc_incomingPartVec
   mc_primFSLepton = entry.mc_primFSLepton
   px = mc_primFSLepton[0] - mc_incomingPartVec[0]
   py = mc_primFSLepton[1] - mc_incomingPartVec[1]
   pz = mc_primFSLepton[2] - mc_incomingPartVec[2]
   q3 = sqrt( px**2 + py**2 + pz**2 )
   return q3/1000

def getNonResonantPionWeight(entry):
   isGenieNonRes1pi = entry.truth_genie_wgt_Rvn1pi[2] < 1.0 or entry.truth_genie_wgt_Rvp1pi[2] < 1.0
   if isGenieNonRes1pi:  return 0.43#errors are +/- 3%ish
   else:                 return 1

def GetTransverseMomentumWRTBeam( px, py, pz ):
    py_prime = -1.0 *sin( numi_beam_angle_rad )*pz + cos( numi_beam_angle_rad )*py;
    pt       = sqrt( px*px + py_prime*py_prime );
    return pt

def GetLongitudinalMomentumWRTBeam( px, py, pz ):
    pz_prime = cos( numi_beam_angle_rad )*pz + sin( numi_beam_angle_rad )*py
    return pz_prime
