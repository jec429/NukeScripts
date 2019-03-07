import math
import ROOT

def isLowNu( Enu , nu ):
  
  if Enu < 3:
    if nu < 0.3:  return True
    else:         return False

  if Enu < 7:
    if nu < 0.5:  return True
    else:         return False
  
  if Enu < 12:
    if nu <1.0:   return True
    else:         return False

  if nu < 2.0:    return True
  else:           return False

def mapEToBinString(Enu):
  if    Enu < 3.0:  return 'ENu_2-3'
  elif  Enu < 7.0:  return 'ENu_3-7'
  elif  Enu < 12.0: return 'ENu_7-12'
  elif  Enu < 22.0: return 'ENu_12-22'

def passesRecoPreCuts( chain , treeName ):

  if treeName == 'CCInclusiveReco' and not chain.pass_canonical_cut == 1: return False
  if treeName == 'NukeCC' and not chain.NukeCC_pass_canonical_cut == 1:   return False
  if treeName == 'MECAna' and not chain.MECAna_pass_canonical_cut == 1:   return False
  if not eval('chain.%s_vtx[2]'%treeName) >= 5990:                        return False 
  if not eval('chain.%s_vtx[2]'%treeName) <= 8340:                        return False 
  if not eval('chain.%s_minos_trk_qp'%treeName) < 0:                      return False
  if not eval('chain.%s_minos_trk_eqp_qp'%treeName) > -0.3:               return False
  if not chain.phys_n_dead_discr_pair_upstream_prim_track_proj <= 1:      return False

  # Calculate reco_theta
  numi_rad = -0.05887
  pz_reco = math.cos(numi_rad)*eval('chain.%s_leptonE[2]'%treeName)+math.sin(numi_rad)*eval('chain.%s_leptonE[1]'%treeName)
  denom2_reco = math.pow(eval('chain.%s_leptonE[0]'%treeName),2) + math.pow(eval('chain.%s_leptonE[1]'%treeName),2) + math.pow(eval('chain.%s_leptonE[2]'%treeName),2) 
  reco_theta = math.acos(pz_reco/math.sqrt(denom2_reco))
  if not reco_theta < 0.35:                                               return False

  if eval('chain.%s_minos_trk_end_x'%treeName) >= -1219:                  return True
  A = eval('chain.%s_minos_trk_end_x'%treeName) + 1219
  B = eval('chain.%s_minos_trk_end_y'%treeName) + 393
  if math.pow(A,2) + math.pow(B,2) < 640000:                              return True

  return False # The final two conditions above are some pair of minos conditions which must both be False for an event to fail precuts 

def passesMCPreCuts( chain ):

  if not chain.mc_current == 1:                                           return False
  if not chain.mc_incoming == 14:                                         return False

  return True

def passesTruthPreCuts( chain ):
  
  # if not event.GetMCVtx2 >= 5990
  if not chain.mc_vtx[2] >= 5990:                                     return False # corresponds to module 27 - plane 1 
  if not chain.mc_vtx[2] <= 8340:                                     return False # corresponds to module 79 - plane 1
  if not chain.mc_vtx[0] > -850:                                      return False 
  if not chain.mc_vtx[0] <  850:                                      return False 
  if not chain.mc_vtx[0] >  1.732*chain.mc_vtx[1]-1699.99:            return False 
  if not chain.mc_vtx[0] < -1.732*chain.mc_vtx[1]+1699.99:            return False 
  if not chain.mc_vtx[0] > -1.732*chain.mc_vtx[1]-1699.99:            return False 
  if not chain.mc_vtx[0] <  1.732*chain.mc_vtx[1]+1699.99:            return False  # fiducial volume (all of the above, save CC cut)
  if not chain.mc_current == 1:                                       return False  # charged-current
  if not chain.mc_incoming == 14:                                     return False  # require incoming particle to be muon neutrino

  return True 

def passesTruthKinematicCuts( chain ):

  if not chain.mc_primFSLepton[3]/1000 > 1.8:                         return False  # require outgoing muon energy to be > 1.8 GeV

  # Calculate true_theta 
  numi_rad = -0.05887
  pz = math.cos(numi_rad)*chain.mc_primFSLepton[2]+math.sin(numi_rad)*chain.mc_primFSLepton[1]
  denom2 = math.pow(chain.mc_primFSLepton[0],2)+math.pow(chain.mc_primFSLepton[1],2)+math.pow(chain.mc_primFSLepton[2],2)  
  true_theta = math.acos(pz/math.sqrt(denom2)) 
  if not true_theta < 0.35:                                           return False  # require muon angle to be < 20.05 degrees

  return True

def passesTruthPreCutsVerbose( chain ):
  
  # if not event.GetMCVtx2 >= 5990
  if not chain.mc_vtx[2] >= 5990:                                     print 'failed cut 1'; return False # corresponds to module 27 - plane 1 
  if not chain.mc_vtx[2] <= 8340:                                     print 'failed cut 2'; return False # corresponds to module 79 - plane 1
  if not chain.mc_vtx[0] > -850:                                      print 'failed cut 3'; return False 
  if not chain.mc_vtx[0] <  850:                                      print 'failed cut 4'; return False 
  if not chain.mc_vtx[0] >  1.732*chain.mc_vtx[1]-1699.99:            print 'failed cut 5'; return False 
  if not chain.mc_vtx[0] < -1.732*chain.mc_vtx[1]+1699.99:            print 'failed cut 6'; return False 
  if not chain.mc_vtx[0] > -1.732*chain.mc_vtx[1]-1699.99:            print 'failed cut 7'; return False 
  if not chain.mc_vtx[0] <  1.732*chain.mc_vtx[1]+1699.99:            print 'failed cut 8'; return False  # fiducial volume (all of the above, save CC cut)
  if not chain.mc_current == 1:                                       print 'failed cut 9'; return False  # charged-current
  if not chain.mc_incoming == 14:                                     print 'failed cut 10'; return False  # require incoming particle to be muon neutrino
  print 'Emu: ' , chain.mc_primFSLepton[3]/1000 
  if not chain.mc_primFSLepton[3]/1000 > 1.8:                         print 'failed cut 11'; return False  # require outgoing muon energy to be > 1.8 GeV

  # Calculate true_theta 
  numi_rad = -0.05887
  pz = math.cos(numi_rad)*chain.mc_primFSLepton[2]+math.sin(numi_rad)*chain.mc_primFSLepton[1]
  denom2 = math.pow(chain.mc_primFSLepton[0],2)+math.pow(chain.mc_primFSLepton[1],2)+math.pow(chain.mc_primFSLepton[2],2)  
  true_theta = math.acos(pz/math.sqrt(denom2)) 
  print 'theta: ' , true_theta
  if not true_theta < 0.35:                                           print 'failed cut 12'; return False  # require muon angle to be < 20.05 degrees
 
  return True 

def makeMigrationMatricesForTuple( OPTS_VEC , tuplePath , outputFile , toolName ):

  chain = WrapChain( toolName )
  chain.Add( tuplePath )
  
  ################################################################ Declare chains above
  
  systematicUniverses = []
  systematicUniverses.append( CVEvent(chain,treeName=toolName) )
  #systematicUniverses.append( HadronEShiftEvent(chain,-1) )
  #systematicUniverses.append( HadronEShiftEvent(chain,+1) )
  #systematicUniverses.append( NormShiftEvent(chain,-1) )
  #systematicUniverses.append( NormShiftEvent(chain,+1) )
  
  ################################################################ Declare systematics objects above
  
  bins_nuE = [1,2,3,4,5,7,9,12,15,18,22,36,50]
  nBins_nuE = len(bins_nuE)-1

  bins_nu_1 = [0,0.3,0.5,1,2,5]
  bins_nu_2 = [i/10. for i in range(51)]
  nBins_nu_1 = len(bins_nu_1)-1
  nBins_nu_2 = len(bins_nu_2)-1
  
  hist_migrationMatrix_inclusive = HistWrapper("migrationMatrix_inclusive",nBins_nuE,array('d',bins_nuE),nBins_nuE,array('d',bins_nuE),systematicUniverses)
  hist_migrationMatrix_lowNu = HistWrapper("migrationMatrix_lowNu",nBins_nuE,array('d',bins_nuE),nBins_nuE,array('d',bins_nuE),systematicUniverses)
  hist_migrationMatrix_highNu = HistWrapper("migrationMatrix_highNu",nBins_nuE,array('d',bins_nuE),nBins_nuE,array('d',bins_nuE),systematicUniverses)

  migrationMatrices_nu = {}
  migrationMatrices_nu_bigBins = {}
  
  signalDefinitions = [
    'inclusive',
    'lowNu',
    'highNu'
  ]
  
  ENu_bins = [
    'ENu_2-3',
    'ENu_3-7',
    'ENu_7-12',
    'ENu_12-22'
  ]

  for signalDefinition,Enu_bin in itertools.product(signalDefinitions,ENu_bins):
    productString = '%s_%s'%(signalDefinition,Enu_bin)

    migrationMatrices_nu[productString] = HistWrapper("migrationMatrix_%s"%productString,nBins_nu_2,array('d',bins_nu_2),nBins_nu_2,array('d',bins_nu_2),systematicUniverses)
    migrationMatrices_nu_bigBins[productString] = HistWrapper("migrationMatrix_%s_bigBins"%productString,nBins_nu_1,array('d',bins_nu_1),nBins_nu_1,array('d',bins_nu_1),systematicUniverses)

  ################################################################ Declare hists above
  
  # Loop over entries in the chain
  for entry in range(chain.GetEntries()):
  
    if entry % 100000 == 0:
      print "entry #: " , entry

    if OPTS_VEC.test_bool == True and entry > 100001:
      continue
 
    chain.LoadTree(entry)
 
    # Implement pre-cuts
    if not passesRecoPreCuts(chain,toolName):    continue 
    if not passesMCPreCuts(chain):    continue

    # Loop over systematics
    for systematicUniverse in systematicUniverses:
      systematicUniverse.setEntry(entry)

      Enu = systematicUniverse.getNeutrinoE()
      Enu_true = systematicUniverse.getTrueNeutrinoE()
      Emu = systematicUniverse.getRecoMuonE()
      nu = systematicUniverse.getRecoHadronE()
      nu_true = systematicUniverse.getTrueHadronE()
 
      wgt = systematicUniverse.getWeight()

      #Implement cuts
      if Emu <= 1.8: continue # minimum Emu requirement
      if not (toolName == 'NukeCC' or toolName == 'MECAna') and systematicUniverse.vertexShiftCorrect() == -1: continue # vertex shift requirement

      hist_migrationMatrix_inclusive.eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(Enu,Enu_true,wgt)
      if isLowNu(Enu,nu):
        hist_migrationMatrix_lowNu.eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(Enu,Enu_true,wgt)
      else:
        hist_migrationMatrix_highNu.eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(Enu,Enu_true,wgt)

      if Enu < 2.0 or Enu >= 22.0: continue
      Enu_bin = mapEToBinString(Enu)

      migrationMatrices_nu['inclusive_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
      migrationMatrices_nu_bigBins['inclusive_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
      if isLowNu(Enu,nu):
        migrationMatrices_nu['lowNu_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
        migrationMatrices_nu_bigBins['lowNu_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
      else:
        migrationMatrices_nu['highNu_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
        migrationMatrices_nu_bigBins['highNu_%s'%Enu_bin].eventToUnivMap[systematicUniverseClass][systematicUniverse].Fill(nu,nu_true,wgt)
        
  print 'tuplePath: ', tuplePath
  
  outputFile.cd()

  for systematicUniverse in systematicUniverses:
    hist_migrationMatrix_inclusive.eventToUnivMap[systematicUniverseClass][systematicUniverse].Write()
    hist_migrationMatrix_lowNu.eventToUnivMap[systematicUniverseClass][systematicUniverse].Write()
    hist_migrationMatrix_highNu.eventToUnivMap[systematicUniverseClass][systematicUniverse].Write()
  
  for signalDefinition,Enu_bin in itertools.product(signalDefinitions,ENu_bins):
    productString = '%s_%s'%(signalDefinition,Enu_bin)
    migrationMatrices_nu[productString].eventToUnivMap[systematicUniverseClass][systematicUniverse].Write()
    migrationMatrices_nu_bigBins[productString].eventToUnivMap[systematicUniverseClass][systematicUniverse].Write()

def copyMetaTreeToOutput( OPTS_VEC , tuplePath , outputFile ):

  inputFile = ROOT.TFile( tuplePath )
 
  try:
    metaTree = inputFile.Get( "Meta" ).CloneTree()
  except:
    print "I couldn't find a Meta tree in this file. What's up with that? Not going to try to write it to output..."
    return

  outputFile.cd()
  metaTree.Write()
 
def constructOutputFilePath( tuplePath , outDir , toolName ):

  fileName = tuplePath.split('/')[-1]
  fileNameComponents = fileName.split('_')
  dataSwitch = fileNameComponents[1]
  playlistName = fileNameComponents[2]

  print 'fileNameComponents: ' , fileNameComponents
  
  if toolName == 'NukeCC' or toolName == 'MECAna':
    subPlaylistIt = fileNameComponents[-1].split('.')[0] + '_' + fileNameComponents[-3] + '_' + fileNameComponents[-2]
  else:
    subPlaylistIt = fileNameComponents[-1].split('.')[0] 
 
  outPath = "%shighNuHists_%s_%s_%s.root" % (outDir,dataSwitch,playlistName,subPlaylistIt)
 
  print 'Writing output to: ' , outPath
 
  return outPath

def extractDataSwitch( tuplePath ):

  fileName = tuplePath.split('/')[-1]
  fileNameComponents = fileName.split('_')
  dataSwitch = fileNameComponents[1]

  if dataSwitch == 'Data': dataSwitch = 'data'
  if dataSwitch == 'MC': dataSwitch = 'mc'

  return dataSwitch

