import ROOT
import math
import sys
from nukeFunctions import *
import PlotUtils

from card import *
from lists import *
from otherFunctions import *

ROOT.TH1.AddDirectory(False)

oneNeutron = 0
moreOneNeutron = 1

short_run = 0
medium_run = 0

bins_Mupt = [0,75,150,250,325,400,475,550,700,850,1000,1250,1500,2500]
nBins_Mupt = len(bins_Mupt)-1
bins_Mupz = [0,1500,2000,2500,3000,3500,4000,4500,5000,6000,8000,10000,15000,20000]
nBins_Mupz = len(bins_Mupz)-1
numi_beam_angle_rad = -0.05887
M_mu = 105.6583

def makeRecoMCHistos(inFile, outputFile, potsh):
    print ''
    t_mc = getChainFile('NukeCCQETwoTrack', inFile)
    t_truth = getChainFile('Truth', inFile)
    pot_mc,pot_mc_total = getPOTFile(inFile)
    
    print 'Entries MC=',t_mc.GetEntries()
    pass_entries = 0

    i = 0

    mcwgt = mcweight.MCweight()
    
    # Get list of systematic universes to loop through
    systematicUniverses = defineSystematicUniverses(t_mc,'mc',toolName='NukeCCQETwoTrack') 

    # Get complete list of systematic universes and create reference MnvH2D for later use
    refSystematicUniversesTruth = defineSystematicUniverses(t_mc,'mc') 
    refMnvH2DTruth = HistWrapper('Mupt_VS_Mupz_ref',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),refSystematicUniversesTruth)
    # Get list of systematic universes to loop through 
    systematicUniversesTruth = defineSystematicUniverses(t_mc,'truth') 

    
    # Declare hists
    hists = []
    hists_t1 = []
    hists_t2 = []
    hists_t3 = []
    hists_t4 = []
    hists_t5 = []
    hists_tW = []
    Mupts = ['Mupt','MuptTrue']
    sigDefs = ['inclusive']
    
    for Mupt in Mupts:        
        hist = [HistWrapper(Mupt+'_VS_Mupz_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists.append(hist)
        hist_t1 = [HistWrapper(Mupt+'_VS_Mupz_t1_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_t1.append(hist_t1)
        hist_t2 = [HistWrapper(Mupt+'_VS_Mupz_t2_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_t2.append(hist_t2)
        hist_t3 = [HistWrapper(Mupt+'_VS_Mupz_t3_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_t3.append(hist_t3)
        hist_t4 = [HistWrapper(Mupt+'_VS_Mupz_t4_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_t4.append(hist_t4)
        hist_t5 = [HistWrapper(Mupt+'_VS_Mupz_t5_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_t5.append(hist_t5)
        hist_tW = [HistWrapper(Mupt+'_VS_Mupz_tW_'+sigDef+'_reco',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses) for sigDef in sigDefs]
        hists_tW.append(hist_tW)
  
    for sigDef in ['inclusive']:
        exec("hist_Mupt_Mupz_{0}_truth = HistWrapper('Mupt_VS_Mupz_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))

        exec("hist_Mupt_Mupz_t1_{0}_truth = HistWrapper('Mupt_VS_Mupz_t1_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_t1_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth = HistWrapper('Mupt_VS_Mupz_t2_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_t2_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth = HistWrapper('Mupt_VS_Mupz_t3_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_t3_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth = HistWrapper('Mupt_VS_Mupz_t4_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_t4_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth = HistWrapper('Mupt_VS_Mupz_t5_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_t5_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth = HistWrapper('Mupt_VS_Mupz_tW_{0}_truth',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth_addKinematicCuts = HistWrapper('Mupt_VS_Mupz_tW_{0}_truth_addKinematicCuts',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))

    entry = 0
    nentries = t_mc.GetEntries()
    timeNow = time.time()
            
    for e in t_mc:
        if entry%10000 == 0:
            print "%d/%d"%(entry,nentries)
            #print time.time() - timeNow 
            timeNow = time.time()

        entry += 1
        if entry > 10000 and short_run: break
        if entry > 100000 and medium_run: break
            
        #mat = findMat(e.mc_vtx,e.mc_targetZ)            
        #proc = findProc(e.mc_intType)

        single_sample = e.SingleTrackSample

        #print muon_pt_beam,muon_pz_beam
            
        #target = -1
        #if target1_cut(e.vtx[2]): target = 0
        #elif target2_cut(e.vtx[2]): target = 1
        #elif target3_cut(e.vtx[2]): target = 2
        #elif target4_cut(e.vtx[2]): target = 3
        #elif target5_cut(e.vtx[2]): target = 4
        #else: continue

        for systematicUniverseClass in systematicUniverses:
            #print len(systematicUniverses[systematicUniverseClass])
            for i,systematicUniverse in enumerate(systematicUniverses[systematicUniverseClass]):
                systematicUniverse.setEntry(entry)
                
                muon_theta = e.NukeCCQETwoTrack_muon_theta
                muon_p     = e.NukeCCQETwoTrack_muon_p
                muon_e     = systematicUniverse.getRecoMuonE()
                if muon_e > 0:
                    muon_p = sqrt( muon_e*muon_e - M_mu*M_mu )
                else:
                    muon_p = 0.0 
                    
                muon_pt_beam = math.sin(muon_theta)*muon_p;
                muon_pz_beam = math.cos(muon_theta)*muon_p;
                #ENu = systematicUniverse.getNeutrinoE()
                Mupt = muon_pt_beam

                #EMu = systematicUniverse.getRecoMuonE()
                EMu = e.NukeCCQETwoTrack_muon_enu

                #nu = systematicUniverse.getRecoHadronE()
                Mupz = muon_pz_beam

                #ENuTrue = systematicUniverse.getTrueNeutrinoE()
                true_muon_px   = e.mc_primFSLepton[0]
                true_muon_py   = e.mc_primFSLepton[1]
                true_muon_pz   = e.mc_primFSLepton[2]
                MuptTrue   = GetTransverseMomentumWRTBeam( true_muon_px, true_muon_py, true_muon_pz )

                wgt = systematicUniverse.getWeight()

                if not pass_cuts(e): continue
                if not pass_neutron_cuts(e): continue

                #Implement cuts
                #if EMu <= 1.8: continue # minimum EMu requirement
                if e.NukeCCQETwoTrack_recoilE > 500: continue # minimum EMu requirement
                #if not (toolName == 'NukeCC' or toolName == 'MECAna') and systematicUniverse.vertexShiftCorrect() == -1: continue # vertex shift requirement
                
                for j,mp in enumerate([Mupt, MuptTrue]):                    
                    hists[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                if target1_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_t1[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                elif target2_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_t2[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                elif target3_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_t3[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                elif target4_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_t4[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                elif target5_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_t5[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

                elif targetW_cut(e.vtx[2]):
                    for j,mp in enumerate([Mupt, MuptTrue]):                    
                        hists_tW[j][0].univHist(systematicUniverseClass,i).Fill(mp,Mupz,wgt)

    entry = 0
    nentries = t_truth.GetEntries()
    timeNow = time.time()
    print 'Entries TRUTH=',t_truth.GetEntries()

    for e in t_truth:
        if entry%10000 == 0:
            print "%d/%d"%(entry,nentries)
            #print time.time() - timeNow 
            timeNow = time.time()

        entry += 1
        if entry > 10000 and short_run: break
        if entry > 100000 and medium_run: break

        #mat = findMat(e.mc_vtx,e.mc_targetZ)            
        #proc = findProc(e.mc_intType)

        #single_sample = e.SingleTrackSample

        #print muon_pt_beam,muon_pz_beam
            
        #target = -1
        #if target1_cut(e.vtx[2]): target = 0
        #elif target2_cut(e.vtx[2]): target = 1
        #elif target3_cut(e.vtx[2]): target = 2
        #elif target4_cut(e.vtx[2]): target = 3
        #elif target5_cut(e.vtx[2]): target = 4
        #else: continue

        # Loop over systematics
        for systematicUniverseClass in systematicUniversesTruth:
            for i,systematicUniverse in enumerate(systematicUniverses[systematicUniverseClass]):
                systematicUniverse.setEntry(entry)

                true_muon_px   = e.mc_primFSLepton[0]
                true_muon_py   = e.mc_primFSLepton[1]
                true_muon_pz   = e.mc_primFSLepton[2]
                MuptTrue   = GetTransverseMomentumWRTBeam( true_muon_px, true_muon_py, true_muon_pz )
                MupzTrue   = GetLongitudinalMomentumWRTBeam( true_muon_px, true_muon_py, true_muon_pz )

                
                wgt = systematicUniverse.getWeight()
    
                hist_Mupt_Mupz_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                if target1_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t1_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target2_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t2_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target3_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t3_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target4_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t4_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target5_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t5_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif targetW_cut(e.mc_vtx[2]): hist_Mupt_Mupz_tW_inclusive_truth.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)

                if not truthKinematicCuts(e): continue
         
                hist_Mupt_Mupz_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                if target1_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t1_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target2_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t2_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target3_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t3_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target4_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t4_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif target5_cut(e.mc_vtx[2]): hist_Mupt_Mupz_t5_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)
                elif targetW_cut(e.mc_vtx[2]): hist_Mupt_Mupz_tW_inclusive_truth_addKinematicCuts.univHist(systematicUniverseClass,i).Fill(MuptTrue,MupzTrue,wgt)


    outputFile.cd()
    potsh.SetBinContent(1,pot_mc)
    potsh.SetBinContent(3,pot_mc_total)
    outputFile.cd()

    # Write hists to output file, but before doing so, create any missing error bands and fill them with CV
    for sigDef in ['inclusive']:
        exec("hist_Mupt_Mupz_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth_addKinematicCuts.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DTruth.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_truth_addKinematicCuts.univHist('CV',0).Write()".format(sigDef))


    outputFile.cd()
    
    for hs in hists:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_t1:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_t2:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_t3:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_t4:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_t5:
        for h in hs:
            h.univHist('CV',0).Write()
    for hs in hists_tW:
        for h in hs:
            h.univHist('CV',0).Write()

def makeRecoDataHistos(inFile, outputFile, potsh):
    #t_data = getChainFile('NukeCCQETwoTrack', '/minerva/data/users/jchaves/googoo/pruned_6A_minerva_00022010-00022020.root')
    t_data = getChainFile('NukeCCQETwoTrack', inFile)
    pot_data,pot_data_total = getPOTFile(inFile)

    # Get complete list of systematic universes and create reference MnvH2D for later use
    refSystematicUniversesData = defineSystematicUniverses(t_data,'mc') 
    refMnvH2DData = HistWrapper('Mupt_VS_Mupz_ref',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),refSystematicUniversesData)

    # Get list of systematic universes to loop through 
    systematicUniverses = defineSystematicUniverses(t_data,'data',toolName='NukeCCQETwoTrack') 
    
    for sigDef in ['inclusive']:
        exec("hist_Mupt_Mupz_{0}_data = HistWrapper('Mupt_VS_Mupz_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_data = HistWrapper('Mupt_VS_Mupz_t1_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_data = HistWrapper('Mupt_VS_Mupz_t2_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_data = HistWrapper('Mupt_VS_Mupz_t3_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_data = HistWrapper('Mupt_VS_Mupz_t4_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_data = HistWrapper('Mupt_VS_Mupz_t5_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_data = HistWrapper('Mupt_VS_Mupz_tW_{0}_data',nBins_Mupt,array('d',bins_Mupt),nBins_Mupz,array('d',bins_Mupz),systematicUniverses)".format(sigDef))

    entry = 0
    nentries = t_data.GetEntries()
    timeNow = time.time()
    print 'Entries DATA=',t_data.GetEntries()

    # Loop over entries in the chain
    for e in t_data:
        if entry%10000 == 0:
            print "%d/%d"%(entry,nentries)
            #print time.time() - timeNow 
            timeNow = time.time()

        entry += 1
        if entry > 10000 and short_run: break
        if entry > 100000 and medium_run: break
    
        #mat = findMat(e.mc_vtx,e.mc_targetZ)            
        #proc = findProc(e.mc_intType)

        single_sample = e.SingleTrackSample

        #print muon_pt_beam,muon_pz_beam
            
        #target = -1
        #if target1_cut(e.vtx[2]): target = 0
        #elif target2_cut(e.vtx[2]): target = 1
        #elif target3_cut(e.vtx[2]): target = 2
        #elif target4_cut(e.vtx[2]): target = 3
        #elif target5_cut(e.vtx[2]): target = 4
        #else: continue
    
        # Loop over systematics
        for systematicUniverseClass in systematicUniverses:
            for i,systematicUniverse in enumerate(systematicUniverses[systematicUniverseClass]):
                systematicUniverse.setEntry(entry)

                muon_theta = e.NukeCCQETwoTrack_muon_theta
                muon_p     = e.NukeCCQETwoTrack_muon_p
                
                muon_pt_beam = math.sin(muon_theta)*muon_p;
                muon_pz_beam = math.cos(muon_theta)*muon_p;
                #ENu = systematicUniverse.getNeutrinoE()
                Mupt = muon_pt_beam

                #EMu = systematicUniverse.getRecoMuonE()
                EMu = e.NukeCCQETwoTrack_muon_enu

                #nu = systematicUniverse.getRecoHadronE()
                Mupz = muon_pz_beam

                
                #Implement cuts
                #if EMu <= 1.8: continue # minimum EMu requirement
                #if not (toolName == 'NukeCC' or toolName == 'MECAna') and systematicUniverse.vertexShiftCorrect() == -1: continue # vertex shift requirement

                if not pass_cuts(e): continue
                if e.NukeCCQETwoTrack_recoilE > 500: continue # minimum EMu requirement
                if not pass_neutron_cuts(e): continue

                
                hist_Mupt_Mupz_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                if target1_cut(e.vtx[2]): hist_Mupt_Mupz_t1_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                elif target2_cut(e.vtx[2]): hist_Mupt_Mupz_t2_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                elif target3_cut(e.vtx[2]): hist_Mupt_Mupz_t3_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                elif target4_cut(e.vtx[2]): hist_Mupt_Mupz_t4_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                elif target5_cut(e.vtx[2]): hist_Mupt_Mupz_t5_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)
                elif targetW_cut(e.vtx[2]): hist_Mupt_Mupz_tW_inclusive_data.univHist(systematicUniverseClass,i).Fill(Mupt,Mupz)

    outputFile.cd()
    potsh.SetBinContent(2,pot_data)

    outputFile.cd()

    for sigDef in ['inclusive']:
        exec("hist_Mupt_Mupz_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t1_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t2_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t3_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t4_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_t5_{0}_data.univHist('CV',0).Write()".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_data.univHist('CV',0).AddMissingErrorBandsAndFillWithCV(refMnvH2DData.univHist('CV',0))".format(sigDef))
        exec("hist_Mupt_Mupz_tW_{0}_data.univHist('CV',0).Write()".format(sigDef))

def pass_neutron_cuts(e):
   if oneNeutron and e.neutron3d_N != 1: return False
   if moreOneNeutron and e.neutron3d_N == 0: return False
   if moreOneNeutron and e.neutron3d_N > 3: return False
   return True

def truthKinematicCuts(e):
    return True

def main():
    playlist = '6A'

    #pot_mc,pot_data,pot_mc_total = getPOT(playlist)
    #t_mc,t_data = getChains('NukeCCQETwoTrack', playlist)
    #t_truth = getChains('Truth', playlist)[0]

    #OPTS_VEC = setup()
    #OPTS_VEC.gridness = 0

    #inFile = sys.argv[1] if len(sys.argv) > 1 else ''
    #print inFile
    #outName = inFile.split('/')[-1].replace('pruned','systematics').replace('*','.root')
    #print outName

    outName = 'systematics_6A_minerva.root'
    outputFile = ROOT.TFile( outName , "recreate" )    
    outputFile.cd()
    potsh = ROOT.TH1F("potsh","",3,0,3)

    inFile = '/minerva/data/users/jchaves/googoo/pruned_6A_minerva_00022*'
    makeRecoDataHistos(inFile, outputFile, potsh)

    inFile = '/minerva/data/users/jchaves/googoo/pruned_6A_minerva_00126*'
    makeRecoMCHistos(inFile, outputFile, potsh)
    
    potsh.Write()
                
    outputFile.Close()

    #print 'Pass n=',pass_entries


if __name__ == "__main__":
    main()
