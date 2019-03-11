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

        #print 'N pdg=',e.mc_nFSPart
        for pdg,energy in zip(e.mc_FSPartPDG,e.mc_FSPartE):
            if abs(pdg) == 13 :
                genie_n_muons += 1;
            elif pdg == 22 and energy >10 :
                genie_n_photons += 1;
            elif abs(pdg) == 211 or abs(pdg) == 321 or abs(pdg) == 323 or pdg == 111 or pdg == 130 or pdg == 310 or pdg == 311 or pdg == 313:
                genie_n_mesons += 1;
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
                else:
                    fillHistosMC(hs_2,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
            else:
                if QElike:
                    fillHistosMC(hs_1,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                else:
                    fillHistosMC(hs_3,proc,mat,single_sample,e.wgt*weight,muon_pt_beam,target)
                

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
    c7.Print('muon_pt_'+target+'.pdf')
    c7.Print('muon_pt_'+target+'.png')
    c7.SetLogy()
    c7.Print('muon_pt_'+target+'_log.pdf')
    c7.Print('muon_pt_'+target+'_log.png')

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
    
    c8.Print('recoilE_'+target+'.pdf')
    c8.Print('recoilE_'+target+'.png')
    c8.SetLogy()
    c8.Print('recoilE_'+target+'_log.pdf')
    c8.Print('recoilE_'+target+'_log.png')

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

   
if __name__ == "__main__":
    main()
