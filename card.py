from lists import *
from classes import *
from inputs import *

def defineSystematicUniverses(chain,dataSwitch,toolName='NukeCCQETwoTrack'):

  truth = True if dataSwitch == 'truth' else False

  systematicUniverses = {} 
  systematicUniverses["CV"] = []
  systematicUniverses["CV"].append( CVEvent(chain,Truth=truth,treeName=toolName) )

  # In the case of data, we don't assess any of the systematics on the data directly. We'll fill in the CV for all SUs and they will become meaningful as we extract the cross section/flux
  if dataSwitch == 'data': return systematicUniverses

  # Reco and true systematics 
  systematicUniverses["2p2hVariation"] = []
  systematicUniverses["2p2hVariation"].append( SU_2p2hShiftEvent(chain,1,Truth=truth,treeName=toolName) )
  systematicUniverses["2p2hVariation"].append( SU_2p2hShiftEvent(chain,2,Truth=truth,treeName=toolName) )
  systematicUniverses["2p2hVariation"].append( SU_2p2hShiftEvent(chain,3,Truth=truth,treeName=toolName) )
  systematicUniverses["RPAVariation"] = []
  systematicUniverses["RPAVariation"].append( RPAShiftEvent(chain,1,Truth=truth,treeName=toolName) )
  systematicUniverses["RPAVariation"].append( RPAShiftEvent(chain,2,Truth=truth,treeName=toolName) )
  systematicUniverses["RPAVariation"].append( RPAShiftEvent(chain,3,Truth=truth,treeName=toolName) )
 
  # Reco-only systematics
  if not truth:
    systematicUniverses["MuonEnergyScale"] = [] 
    systematicUniverses["MuonEnergyScale"].append( MuonEShiftEvent(chain,-1,treeName=toolName) )
    systematicUniverses["MuonEnergyScale"].append( MuonEShiftEvent(chain,+1,treeName=toolName) )
    #systematicUniverses["MuonEnergyScale"].append( MuonEShiftEvent(chain,-1.8,treeName=toolName) )
    #systematicUniverses["MuonEnergyScale"].append( MuonEShiftEvent(chain,+1.8,treeName=toolName) )
 
  #  systematicUniverses.append( HadronEShiftEvent(chain,-1) )
  #  systematicUniverses.append( HadronEShiftEvent(chain,+1) )
 
  return systematicUniverses
 
bins_nuE = [0,1,2,3,4,5,7,9,12,15,18,22,36,50,75,100,120]
nBins_nuE = len(bins_nuE)-1
bins_nu = [0,0.3,0.5,1,2,5]
nBins_nu = len(bins_nu)-1

