import ROOT
import math
from nukePlots import *

oneNeutron = 0
moreOneNeutron = 1

short_run = 0
playlist = '6A'

def main():    
    pot_mc,pot_data,pot_mc_total = getPOT(playlist)

    t_mc_0,t_data = getChains('NukeCCQETwoTrack', playlist)

    print 'Entries MC=',t_mc_0.GetEntries()
    pass_entries = 0

    bins = 100
    # Define histograms
    if True:
       hs_0 = makeHistos('0',bins,[0,1500]) # Muon pT
       hs_1 = makeHistos('1',bins,[0,1500]) # Muon pT
       hs_2 = makeHistos('2',bins,[0,1500]) # Muon pT
       hs_3 = makeHistos('3',bins,[0,1500]) # Muon pT
       hs_4 = makeHistos('4',bins,[0,2000]) # Recoil E
       hs_5 = makeHistos('5',bins,[0,2000]) # Recoil E
       #Pion Plots David Added
       hs_6 = makeHistos('6',bins,[0,2000]) # pi_p_E
       hs_7 = makeHistos('7',bins,[0,2000]) # pi_p_E
       hs_8 = makeHistos('8',bins,[0,2000]) # pi_p_E
       hs_9 = makeHistos('9',bins,[0,2000]) # pi_p_E
       hs_10 = makeHistos('10',bins,[0,2000]) # pi_m_E
       hs_11 = makeHistos('11',bins,[0,2000]) # pi_m_E
       hs_12 = makeHistos('12',bins,[0,2000]) # pi_m_E
       hs_13 = makeHistos('13',bins,[0,2000]) # pi_m_E
       hs_14 = makeHistos('14',bins,[0,2000]) # pi_0_E
       hs_15 = makeHistos('15',bins,[0,2000]) # pi_0_E
       hs_16 = makeHistos('16',bins,[0,2000]) # pi_0_E
       hs_17 = makeHistos('17',bins,[0,2000]) # pi_0_E
       hs_18 = makeHistos('18',5,[0,5]) # n_pi_p
       hs_19 = makeHistos('19',5,[0,5]) # n_pi_p
       hs_20 = makeHistos('20',5,[0,5]) # n_pi_p
       hs_21 = makeHistos('21',5,[0,5]) # n_pi_p
       hs_22 = makeHistos('22',5,[0,5]) # n_pi_m
       hs_23 = makeHistos('23',5,[0,5]) # n_pi_m
       hs_24 = makeHistos('24',5,[0,5]) # n_pi_m
       hs_25 = makeHistos('25',5,[0,5]) # n_pi_m
       hs_26 = makeHistos('26',5,[0,5]) # n_pi_0
       hs_27 = makeHistos('27',5,[0,5]) # n_pi_0
       hs_28 = makeHistos('28',5,[0,5]) # n_pi_0
       hs_29 = makeHistos('29',5,[0,5]) # n_pi_0
       #######################################

       hs_2d_0 = makeHistos2D('2d0',20,[0,3e6],20,[0,2000]) # Recoil E vs. Q2
       hs_2d_1 = makeHistos2D('2d1',20,[0,3e6],20,[0,2000]) # Recoil E vs. Q2
      
    i = 0
    entry = 0
    nentries = t_mc_0.GetEntries()
    timeNow = time.time()

    mcwgt = mcweight.MCweight()

    for e in t_mc_0:
        if entry%10000 == 0:
            print "%d/%d"%(entry,nentries)
            #print time.time() - timeNow 
            timeNow = time.time()

        i += 1
        entry += 1
        if entry > 10000 and short_run: break

        if not pass_cuts(e): continue
        if not pass_neutron_cuts(e): continue

        
        # Weights
        if True:
            # define mcweight
            tq0_genie, tq3_genie = [getTrueQ0(e)],[getTrueQ3(e)]

            #RPA weighting (need inputs from true generator value, tq0_genie[0] and tq3_genie[0] are true q0 and q3 in generator level)
            rpawgt = mcwgt.getRPAWeight(e.mc_intType, e.mc_targetZ, tq0_genie[0], tq3_genie[0])
          
            #2p2h weighting (need inputs from true generator value, tq0_genie[0] and tq3_genie[0] are true q0 and q3 in generator level)
            tpthwgt = mcwgt.get2p2hWeight(e.mc_intType, tq0_genie[0], tq3_genie[0])
          
            #Non-Resonance pion reduction weighting (it is commented out for my case, but you can edit for your usage)
            nonreswt = getNonResonantPionWeight(e)
      
            weight = pot_data/pot_mc * rpawgt * tpthwgt * nonreswt

        pass_entries += 1
            
        mat = findMat(e.mc_vtx,e.mc_targetZ)            
        proc = findProc(e.mc_intType)

        single_sample = e.SingleTrackSample

        muon_theta = e.NukeCCQETwoTrack_muon_theta
        muon_p     = e.NukeCCQETwoTrack_muon_p
      
        muon_pt_beam = math.sin(muon_theta)*muon_p;
        muon_pz_beam = math.cos(muon_theta)*muon_p;

        #print muon_pt_beam,muon_pz_beam
            
        target = -1
        if target1_cut(e.vtx[2]): target = 0
        elif target2_cut(e.vtx[2]): target = 1
        elif target3_cut(e.vtx[2]): target = 2
        elif target4_cut(e.vtx[2]): target = 3
        elif target5_cut(e.vtx[2]): target = 4
        else: continue
        
        genie_n_muons = 0
        genie_n_photons = 0
        genie_n_mesons = 0
        genie_n_heavy_baryons_plus_pi0s = 0
        genie_n_protons = 0

        # PION VARIABLES
        n_pi_p = 0
        n_pi_m = 0
        n_pi_0 = 0

        pi_p_Es = []
        pi_m_Es = []
        pi_0_Es = []
        # END PION VARIABLES

        #print 'N pdg=',e.mc_nFSPart
        for pdg,energy in zip(e.mc_FSPartPDG,e.mc_FSPartE):
            if abs(pdg) == 13 :
                genie_n_muons += 1;
            elif pdg == 22 and energy >10 :
                genie_n_photons += 1;
            # CHANGED SOME OF THESE TO COUNT PIONS AND TRACK THEIR ENERGIES
            elif pdg == 211:
                n_pi_p += 1;
                pi_p_Es.append(energy);
                genie_n_mesons += 1;
            elif pdg == -211:
                n_pi_m += 1;
                pi_m_Es.append(energy);
                genie_n_mesons += 1;
            elif pdg == 111:
                n_pi_0 += 1;
                pi_0_Es.append(energy);
                genie_n_mesons += 1;
            elif abs(pdg) == 321 or abs(pdg) == 323 or pdg == 130 or pdg == 310 or pdg == 311 or pdg == 313:
                genie_n_mesons += 1;
            # BELOW WAS LEFT UNCHANGED
            elif pdg == 3112 or pdg == 3122 or pdg == 3212 or pdg == 3222 or pdg == 4112 or pdg == 4122 or pdg == 4212 or pdg == 4222 or pdg == 411 or pdg == 421 or pdg == 111 :
                genie_n_heavy_baryons_plus_pi0s += 1;
            elif pdg == 2212 and energy > 1058.272: genie_n_protons += 1;

                
        #QElike = (e.genie_n_muons == 1 and e.genie_n_pions == 0 and e.genie_n_pi_zeros)
        QElike = genie_n_muons == 1 and genie_n_mesons == 0 and genie_n_heavy_baryons_plus_pi0s == 0 and genie_n_photons == 0 and genie_n_protons == 0
      
        # Fill target histos
        if True:
            if QElike:
                fillHistosMC(hs_4,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,target)
                #fillHistosMC2D(hs_2d_0,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,target)
                fillHistosMC2D(hs_2d_0,proc,mat,single_sample,1.0,e.NukeCCQETwoTrack_muon_q2,e.NukeCCQETwoTrack_recoilE,target)
                fillHistosMC2D(hs_2d_0,proc,mat,single_sample,1.0,e.NukeCCQETwoTrack_muon_q2,e.NukeCCQETwoTrack_recoilE,5)
            else:
                fillHistosMC(hs_5,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,target)
                #fillHistosMC2D(hs_2d_1,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,target)
                fillHistosMC2D(hs_2d_1,proc,mat,single_sample,1.0,e.NukeCCQETwoTrack_muon_q2,e.NukeCCQETwoTrack_recoilE,target)
                fillHistosMC2D(hs_2d_1,proc,mat,single_sample,1.0,e.NukeCCQETwoTrack_muon_q2,e.NukeCCQETwoTrack_recoilE,5)
            
            if e.NukeCCQETwoTrack_recoilE < 500:
                if QElike:
                    fillHistosMC(hs_0,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                    # No. PION PLOTS
                    fillHistosMC(hs_18,proc,mat,single_sample,e.wgt*weight,n_pi_p,target)
                    fillHistosMC(hs_22,proc,mat,single_sample,e.wgt*weight,n_pi_m,target)
                    fillHistosMC(hs_26,proc,mat,single_sample,e.wgt*weight,n_pi_0,target)
                    # PION ENERGY PLOTS
                    for pion_iter in range(n_pi_p):
                        fillHistosMC(hs_6,proc,mat,single_sample,e.wgt*weight,pi_p_Es[pion_iter],target)
                    for pion_iter in range(n_pi_m):
                        fillHistosMC(hs_10,proc,mat,single_sample,e.wgt*weight,pi_m_Es[pion_iter],target)
                    for pion_iter in range(n_pi_0):
                        fillHistosMC(hs_14,proc,mat,single_sample,e.wgt*weight,pi_0_Es[pion_iter],target)
                else:
                    fillHistosMC(hs_2,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                    # No. PION PLOTS
                    fillHistosMC(hs_20,proc,mat,single_sample,e.wgt*weight,n_pi_p,target)
                    fillHistosMC(hs_24,proc,mat,single_sample,e.wgt*weight,n_pi_m,target)
                    fillHistosMC(hs_28,proc,mat,single_sample,e.wgt*weight,n_pi_0,target)
                    # PION ENERGY PLOTS
                    for pion_iter in range(n_pi_p):
                        fillHistosMC(hs_8,proc,mat,single_sample,e.wgt*weight,pi_p_Es[pion_iter],target)
                    for pion_iter in range(n_pi_m):
                        fillHistosMC(hs_12,proc,mat,single_sample,e.wgt*weight,pi_m_Es[pion_iter],target)
                    for pion_iter in range(n_pi_0):
                        fillHistosMC(hs_16,proc,mat,single_sample,e.wgt*weight,pi_0_Es[pion_iter],target)
            else:
                if QElike:
                    fillHistosMC(hs_1,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                    # No. PION PLOTS
                    fillHistosMC(hs_19,proc,mat,single_sample,e.wgt*weight,n_pi_p,target)
                    fillHistosMC(hs_23,proc,mat,single_sample,e.wgt*weight,n_pi_m,target)
                    fillHistosMC(hs_27,proc,mat,single_sample,e.wgt*weight,n_pi_0,target)
                    # PION ENERGY PLOTS
                    for pion_iter in range(n_pi_p):
                        fillHistosMC(hs_7,proc,mat,single_sample,e.wgt*weight,pi_p_Es[pion_iter],target)
                    for pion_iter in range(n_pi_m):
                        fillHistosMC(hs_11,proc,mat,single_sample,e.wgt*weight,pi_m_Es[pion_iter],target)
                    for pion_iter in range(n_pi_0):
                        fillHistosMC(hs_15,proc,mat,single_sample,e.wgt*weight,pi_0_Es[pion_iter],target)
                else:
                    fillHistosMC(hs_3,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                    # No. PION PLOTS
                    fillHistosMC(hs_21,proc,mat,single_sample,e.wgt*weight,n_pi_p,target)
                    fillHistosMC(hs_25,proc,mat,single_sample,e.wgt*weight,n_pi_m,target)
                    fillHistosMC(hs_29,proc,mat,single_sample,e.wgt*weight,n_pi_0,target)
                    # PION ENERGY PLOTS
                    for pion_iter in range(n_pi_p):
                        fillHistosMC(hs_9,proc,mat,single_sample,e.wgt*weight,pi_p_Es[pion_iter],target)
                    for pion_iter in range(n_pi_m):
                        fillHistosMC(hs_13,proc,mat,single_sample,e.wgt*weight,pi_m_Es[pion_iter],target)
                    for pion_iter in range(n_pi_0):
                        fillHistosMC(hs_17,proc,mat,single_sample,e.wgt*weight,pi_0_Es[pion_iter],target)
    

    print 'Pass n=',pass_entries
    print 'Entries=',t_data.GetEntries()
    pass_entries = 0

    entry = 0
    nentries = t_data.GetEntries()
    for e in t_data:
      if entry%10000 == 0:
          print "%d/%d"%(entry,nentries)

      entry += 1
      if entry > 10000 and short_run: break

      if not pass_cuts(e): continue
      if not pass_neutron_cuts(e): continue
      
      pass_entries += 1
      single_sample = e.SingleTrackSample

      muon_theta = e.NukeCCQETwoTrack_muon_theta
      muon_p     = e.NukeCCQETwoTrack_muon_p
      
      muon_pt_beam = math.sin(muon_theta)*muon_p;
      muon_pz_beam = math.cos(muon_theta)*muon_p;
      
      target = -1
      if target1_cut(e.vtx[2]): target = 0
      elif target2_cut(e.vtx[2]): target = 1
      elif target3_cut(e.vtx[2]): target = 2
      elif target4_cut(e.vtx[2]): target = 3
      elif target5_cut(e.vtx[2]): target = 4
      else: continue
      
      # Fill target histos
      if True:
          fillHistosData(hs_4,single_sample,e.NukeCCQETwoTrack_recoilE,target)

          if e.NukeCCQETwoTrack_recoilE < 500:
              fillHistosData(hs_0,single_sample,muon_pt_beam,target)
          else:
              fillHistosData(hs_1,single_sample,muon_pt_beam,target)


    scale = pot_data/pot_mc
    print 'Pass n=',pass_entries

    '''
    draw_plots(hs_0[0][1],hs_2[0][1],hs_0[0][6],'t1')
    draw_plots(hs_1[0][1],hs_3[0][1],hs_1[0][6],'t1_bkg')
    draw_plots2(hs_4[0][1],hs_5[0][1],hs_4[0][6],'t1')
    
    draw_plots(hs_0[1][1],hs_2[1][1],hs_0[1][6],'t2')
    draw_plots(hs_1[1][1],hs_3[1][1],hs_1[1][6],'t2_bkg')
    draw_plots2(hs_4[1][1],hs_5[1][1],hs_4[1][6],'t2')
    
    draw_plots(hs_0[2][1],hs_2[2][1],hs_0[2][6],'t3')
    draw_plots(hs_1[2][1],hs_3[2][1],hs_1[2][6],'t3_bkg')
    draw_plots2(hs_4[2][1],hs_5[2][1],hs_4[2][6],'t3')
    
    draw_plots(hs_0[3][1],hs_2[3][1],hs_0[3][6],'t4')
    draw_plots(hs_1[3][1],hs_3[3][1],hs_1[3][6],'t4_bkg')
    draw_plots2(hs_4[3][1],hs_5[3][1],hs_4[3][6],'t4')
    
    draw_plots(hs_0[4][1],hs_2[4][1],hs_0[4][6],'t5')
    draw_plots(hs_1[4][1],hs_3[4][1],hs_1[4][6],'t5_bkg')
    draw_plots2(hs_4[4][1],hs_5[4][1],hs_4[4][6],'t5')
    
    draw_plots(hs_0[5][1],hs_2[5][1],hs_0[5][6],'all')
    draw_plots(hs_1[5][1],hs_3[5][1],hs_1[5][6],'all_bkg')
    draw_plots2(hs_4[5][1],hs_5[5][1],hs_4[5][6],'all')
    
    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[0][1],hs_8[0][1],'t1')
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[0][1],hs_9[0][1],'t1_bkg') 
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[1][1],hs_8[1][1],'t2')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[1][1],hs_9[1][1],'t2_bkg')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[2][1],hs_8[2][1],'t3')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[2][1],hs_9[2][1],'t3_bkg')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[3][1],hs_8[3][1],'t4')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[3][1],hs_9[3][1],'t4_bkg')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[4][1],hs_8[4][1],'t5')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[4][1],hs_9[4][1],'t5_bkg')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_6[5][1],hs_8[5][1],'all')    
    draw_plots_MCONLY('pi_p_Es_','#pi^{+} Energy[MeV]',hs_7[5][1],hs_9[5][1],'all_bkg')    

    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[0][1],hs_12[0][1],'t1')
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[0][1],hs_13[0][1],'t1_bkg') 
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[1][1],hs_12[1][1],'t2')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[1][1],hs_13[1][1],'t2_bkg')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[2][1],hs_12[2][1],'t3')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[2][1],hs_13[2][1],'t3_bkg')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[3][1],hs_12[3][1],'t4')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[3][1],hs_13[3][1],'t4_bkg')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[4][1],hs_12[4][1],'t5')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[4][1],hs_13[4][1],'t5_bkg')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_10[5][1],hs_12[5][1],'all')    
    draw_plots_MCONLY('pi_m_Es_','#pi^{-} Energy[MeV]',hs_11[5][1],hs_13[5][1],'all_bkg')    

    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[0][1],hs_16[0][1],'t1')
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[0][1],hs_17[0][1],'t1_bkg') 
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[1][1],hs_16[1][1],'t2')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[1][1],hs_17[1][1],'t2_bkg')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[2][1],hs_16[2][1],'t3')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[2][1],hs_17[2][1],'t3_bkg')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[3][1],hs_16[3][1],'t4')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[3][1],hs_17[3][1],'t4_bkg')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[4][1],hs_16[4][1],'t5')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[4][1],hs_17[4][1],'t5_bkg')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_14[5][1],hs_16[5][1],'all')    
    draw_plots_MCONLY('pi_0_Es_','#pi^{0} Energy[MeV]',hs_15[5][1],hs_17[5][1],'all_bkg')    
    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[0][1],hs_20[0][1],'t1')
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[0][1],hs_21[0][1],'t1_bkg')
    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[1][1],hs_20[1][1],'t2')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[1][1],hs_21[1][1],'t2_bkg')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[2][1],hs_20[2][1],'t3')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[2][1],hs_21[2][1],'t3_bkg')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[3][1],hs_20[3][1],'t4')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[3][1],hs_21[3][1],'t4_bkg')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[4][1],hs_20[4][1],'t5')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[4][1],hs_21[4][1],'t5_bkg')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_18[5][1],hs_20[5][1],'all')    
    draw_plots_MCONLY('n_pi_p_','No. #pi^{+}',hs_19[5][1],hs_21[5][1],'all_bkg')    

    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[0][1],hs_24[0][1],'t1')
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[0][1],hs_25[0][1],'t1_bkg') 
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[1][1],hs_24[1][1],'t2')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[1][1],hs_25[1][1],'t2_bkg')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[2][1],hs_24[2][1],'t3')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[2][1],hs_25[2][1],'t3_bkg')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[3][1],hs_24[3][1],'t4')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[3][1],hs_25[3][1],'t4_bkg')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[4][1],hs_24[4][1],'t5')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[4][1],hs_25[4][1],'t5_bkg')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_22[5][1],hs_24[5][1],'all')    
    draw_plots_MCONLY('n_pi_m_','No. #pi^{-}',hs_23[5][1],hs_25[5][1],'all_bkg')    

    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[0][1],hs_28[0][1],'t1')
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[0][1],hs_29[0][1],'t1_bkg') 
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[1][1],hs_28[1][1],'t2')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[1][1],hs_29[1][1],'t2_bkg')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[2][1],hs_28[2][1],'t3')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[2][1],hs_29[2][1],'t3_bkg')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[3][1],hs_28[3][1],'t4')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[3][1],hs_29[3][1],'t4_bkg')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[4][1],hs_28[4][1],'t5')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[4][1],hs_29[4][1],'t5_bkg')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_26[5][1],hs_28[5][1],'all')    
    draw_plots_MCONLY('n_pi_0_','No. #pi^{0}',hs_27[5][1],hs_29[5][1],'all_bkg')    
    '''
    
    draw_plots2D(hs_2d_0[0][1],hs_2d_1[0][1],hs_2d_0[0][6],'t1')
    draw_plots2D(hs_2d_0[1][1],hs_2d_1[1][1],hs_2d_0[1][6],'t2')
    draw_plots2D(hs_2d_0[2][1],hs_2d_1[2][1],hs_2d_0[2][6],'t3')
    draw_plots2D(hs_2d_0[3][1],hs_2d_1[3][1],hs_2d_0[3][6],'t4')
    draw_plots2D(hs_2d_0[4][1],hs_2d_1[4][1],hs_2d_0[4][6],'t5')
    draw_plots2D(hs_2d_0[5][1],hs_2d_1[5][1],hs_2d_0[5][6],'all')
    
    
def draw_plots(hs_0,hs_2,h_data,target):
    hs_0[0].SetFillColor(ROOT.kRed);
    hs_0[1].SetFillColor(ROOT.kOrange);
    hs_0[2].SetFillColor(ROOT.kGreen-3);
    hs_0[3].SetFillColor(ROOT.kMagenta);
    hs_0[4].SetFillColor(ROOT.kBlue);
    hs_0[5].SetFillColor(ROOT.kBlack);
    
    hs_2[0].SetFillColor(ROOT.kRed);
    hs_2[1].SetFillColor(ROOT.kOrange);
    hs_2[2].SetFillColor(ROOT.kGreen-3);
    hs_2[3].SetFillColor(ROOT.kMagenta);
    hs_2[4].SetFillColor(ROOT.kBlue);
    hs_2[5].SetFillColor(ROOT.kBlack);
    hs_2[0].SetFillStyle(3444);
    hs_2[1].SetFillStyle(3444);
    hs_2[2].SetFillStyle(3444);
    hs_2[3].SetFillStyle(3444);
    hs_2[4].SetFillStyle(3444);
    hs_2[5].SetFillStyle(3444);
   
    c7 = ROOT.TCanvas('c7')
    th = ROOT.THStack();

    th.Add(hs_2[0])
    th.Add(hs_2[4])
    th.Add(hs_2[1])
    th.Add(hs_2[2])
    th.Add(hs_2[3])
    th.Add(hs_2[5])
    
    th.Add(hs_0[0])
    th.Add(hs_0[4])
    th.Add(hs_0[1])
    th.Add(hs_0[2])
    th.Add(hs_0[3])
    th.Add(hs_0[5])
   
    h_data.SetMarkerStyle(20)
    #hs_0[0][6].SetMarkerStyle(20)
    th.Draw('histo')
    th.GetXaxis().SetTitle('Muon pT[MeV]')
    h_data.Draw('epsame')
    #hs_0[0][6].Draw('epsame')
    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.SetNColumns(2);
    leg.AddEntry( hs_0[0], 'QE' ,'f') ;
    leg.AddEntry( hs_2[0], 'QE' ,'f') ;
    
    leg.AddEntry( hs_0[4], '2p2h' ,'f') ;
    leg.AddEntry( hs_2[4], '2p2h' ,'f') ;
    
    leg.AddEntry( hs_0[1], 'RES' ,'f') ;
    leg.AddEntry( hs_2[1], 'RES' ,'f') ;
    
    leg.AddEntry( hs_0[2], 'DIS' ,'f') ;
    leg.AddEntry( hs_2[2], 'DIS' ,'f') ;
    
    leg.AddEntry( hs_0[3], 'COH' ,'f') ;
    leg.AddEntry( hs_2[3], 'COH' ,'f') ;
    leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    c7.Print('plots/muon_pt_'+target+'.pdf')
    c7.Print('plots/muon_pt_'+target+'.png')
    c7.SetLogy()
    c7.Print('plots/muon_pt_'+target+'_log.pdf')
    c7.Print('plots/muon_pt_'+target+'_log.png')

def draw_plots2(hs_4,hs_5,h_data,target):
    c8 = ROOT.TCanvas('c8')
    th_qe = ROOT.THStack();
    hs_4[0].Add(hs_4[1])
    hs_4[0].Add(hs_4[2])
    hs_4[0].Add(hs_4[3])
    hs_4[0].Add(hs_4[4])
    hs_4[0].Add(hs_4[5])
    hs_4[0].SetFillColor(ROOT.kBlue)
    hs_5[0].Add(hs_5[1])
    hs_5[0].Add(hs_5[2])
    hs_5[0].Add(hs_5[3])
    hs_5[0].Add(hs_5[4])
    hs_5[0].Add(hs_5[5])
    hs_5[0].SetFillColor(ROOT.kRed)
    th_qe.Add(hs_5[0])
    th_qe.Add(hs_4[0])
    th_qe.Draw('histo')
    th_qe.GetXaxis().SetTitle('Recoil E[MeV]')
    #hs_4[0][6].Draw('epsame')
    h_data.Draw('epsame')

    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.SetNColumns(2);
    leg.AddEntry( hs_4[0], 'QE-like' ,'f') ;
    leg.AddEntry( hs_5[0], 'Not QE-like' ,'f') ;
    
    leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    
    c8.Print('plots/recoilE_'+target+'.pdf')
    c8.Print('plots/recoilE_'+target+'.png')
    c8.SetLogy()
    c8.Print('plots/recoilE_'+target+'_log.pdf')
    c8.Print('plots/recoilE_'+target+'_log.png')

### NEWLY DEFINED FOR PION PLOTS
### HELPS TO HAVE TITLE VARIABILITY SO ONLY ONE FUNCTION FOR MANY PLOTS
def draw_plots_MCONLY(title,xtitle,hs_0,hs_2,target):
    hs_0[0].SetFillColor(ROOT.kRed);
    hs_0[1].SetFillColor(ROOT.kOrange);
    hs_0[2].SetFillColor(ROOT.kGreen-3);
    hs_0[3].SetFillColor(ROOT.kMagenta);
    hs_0[4].SetFillColor(ROOT.kBlue);
    hs_0[5].SetFillColor(ROOT.kBlack);
    
    hs_2[0].SetFillColor(ROOT.kRed);
    hs_2[1].SetFillColor(ROOT.kOrange);
    hs_2[2].SetFillColor(ROOT.kGreen-3);
    hs_2[3].SetFillColor(ROOT.kMagenta);
    hs_2[4].SetFillColor(ROOT.kBlue);
    hs_2[5].SetFillColor(ROOT.kBlack);
    hs_2[0].SetFillStyle(3444);
    hs_2[1].SetFillStyle(3444);
    hs_2[2].SetFillStyle(3444);
    hs_2[3].SetFillStyle(3444);
    hs_2[4].SetFillStyle(3444);
    hs_2[5].SetFillStyle(3444);
   
    c9 = ROOT.TCanvas('c9')
    th = ROOT.THStack();

    th.Add(hs_2[0])
    th.Add(hs_2[4])
    th.Add(hs_2[1])
    th.Add(hs_2[2])
    th.Add(hs_2[3])
    th.Add(hs_2[5])
    
    th.Add(hs_0[0])
    th.Add(hs_0[4])
    th.Add(hs_0[1])
    th.Add(hs_0[2])
    th.Add(hs_0[3])
    th.Add(hs_0[5])

    th.Draw('histo')
    th.GetXaxis().SetTitle(xtitle)
   
    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.SetNColumns(2);
    leg.AddEntry( hs_0[0], 'QE' ,'f') ;
    leg.AddEntry( hs_2[0], 'QE' ,'f') ;
    
    leg.AddEntry( hs_0[4], '2p2h' ,'f') ;
    leg.AddEntry( hs_2[4], '2p2h' ,'f') ;
    
    leg.AddEntry( hs_0[1], 'RES' ,'f') ;
    leg.AddEntry( hs_2[1], 'RES' ,'f') ;
    
    leg.AddEntry( hs_0[2], 'DIS' ,'f') ;
    leg.AddEntry( hs_2[2], 'DIS' ,'f') ;
    
    leg.AddEntry( hs_0[3], 'COH' ,'f') ;
    leg.AddEntry( hs_2[3], 'COH' ,'f') ;
    leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    c9.Print('plots/'+title+target+'.pdf')
    c9.Print('plots/'+title+target+'.png')
    c9.SetLogy()
    c9.Print('plots/'+title+target+'_log.pdf')
    c9.Print('plots/'+title+target+'_log.png')

def draw_plots2D(hs_4,hs_5,h_data,target):
    c8 = ROOT.TCanvas('c8', "First canvas", 1600, 600)
    c8.Divide(2,1)
    c8.cd(1)
    hs_4[0].Add(hs_4[1])
    hs_4[0].Add(hs_4[2])
    hs_4[0].Add(hs_4[3])
    hs_4[0].Add(hs_4[4])
    hs_4[0].Add(hs_4[5])
    hs_4[0].SetMarkerColor(ROOT.kBlue)
    hs_4[0].SetFillColor(ROOT.kBlue)
    #hs_4[0].SetMarkerStyle(3)
    hs_5[0].Add(hs_5[1])
    hs_5[0].Add(hs_5[2])
    hs_5[0].Add(hs_5[3])
    hs_5[0].Add(hs_5[4])
    hs_5[0].Add(hs_5[5])
    hs_5[0].SetMarkerColor(ROOT.kRed)
    hs_5[0].SetFillColor(ROOT.kRed)
    #hs_5[0].SetMarkerStyle(3)
    hs_4[0].Draw()
    hs_4[0].GetXaxis().SetTitle('Q^{2}')
    hs_4[0].GetYaxis().SetTitle('Recoil E[MeV]')
    hs_4[0].GetYaxis().SetTitleOffset(1.5);

    c8.cd(2);
    hs_5[0].Draw()
    hs_5[0].GetXaxis().SetTitle('Q^{2}')
    hs_5[0].GetYaxis().SetTitle('Recoil E[MeV]')
    hs_5[0].GetYaxis().SetTitleOffset(1.5);
    
    #hs_4[0][6].Draw('epsame')
    #h_data.Draw('epsame')

    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.SetNColumns(2);
    leg.AddEntry( hs_4[0], 'QE-like' ,'f') ;
    leg.AddEntry( hs_5[0], 'Not QE-like' ,'f') ;
    
    #leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    
    c8.Print('plots/recoilE_q2_'+target+'.pdf')
    c8.Print('plots/recoilE_q2_'+target+'.png')
    c8.Print('plots/recoilE_q2_'+target+'.C')

    c9 = ROOT.TCanvas('c9')
    xbins = hs_4[0].GetXaxis().GetNbins()
    ybins = hs_4[0].GetYaxis().GetNbins()
    xmax  = hs_4[0].GetXaxis().GetXmax()
    ymax  = hs_4[0].GetYaxis().GetXmax()
    
    
    h_ratio = ROOT.TH2F('h_ratio','',xbins,0,xmax,ybins,0,ymax)
    for x in range(1,xbins):
        for y in range(1,xbins):
            sig = hs_4[0].GetBinContent(x,y)
            bkg = hs_5[0].GetBinContent(x,y)
            
            if sig+bkg > 0:
                h_ratio.SetBinContent(x,y,float(bkg)/float(sig+bkg))
            else:
                h_ratio.SetBinContent(x,y,0.0)

    h_ratio.Draw('colz')
    h_ratio.GetXaxis().SetTitle('Q^{2}')
    h_ratio.GetYaxis().SetTitle('Recoil E[MeV]')
    c9.Print('plots/recoilE_q2_'+target+'_ratio.pdf')
    c9.Print('plots/recoilE_q2_'+target+'_ratio.png')
    c9.Print('plots/recoilE_q2_'+target+'_ratio.C')
    
            
if __name__ == "__main__":
    main()
