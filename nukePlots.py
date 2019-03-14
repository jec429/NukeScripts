import ROOT
from math import sqrt
import time
import mcweight
import os
from nukeFunctions import *

def findMat(mc_vtx,mc_targetZ):
   mat = -1
   if is_scintillator(mc_vtx,mc_targetZ):
      mat = 0
   elif mc_targetZ == 8 or mc_targetZ == 1:
      mat = 1
   elif mc_targetZ == 26:
      mat = 2
   elif mc_targetZ == 82:
      mat = 3
   elif mc_targetZ == 6:
      mat = 4
   else:
      mat = 5
   return mat
   
def findProc(mc_intType):
   proc = -1
   if mc_intType == 1:
      proc = 0
   elif mc_intType == 2:
      proc = 1
   elif mc_intType == 3:
      proc = 2
   elif mc_intType == 4:
      proc = 3
   elif mc_intType == 8:
      proc = 4
   else:
      proc = 5
   return proc

def drawPlotMat(hs_0,h_data,xtitle,fname):
    # 0 -> scintillator
    # 1 -> water
    # 2 -> iron
    # 3 -> lead
    # 4 -> pure carbon
    # 5 -> other

    c1 = ROOT.TCanvas('c1')
    th = ROOT.THStack();

    hs_0[0].SetFillColor(ROOT.kOrange);
    hs_0[1].SetFillColor(ROOT.kBlue-3);
    hs_0[2].SetFillColor(ROOT.kRed+1);
    hs_0[3].SetFillColor(38);
    hs_0[4].SetFillColor(ROOT.kGreen-3);
    hs_0[5].SetFillColor(ROOT.kBlack);

    for x in xrange(6):
        th.Add(hs_0[x])
    h_data.SetMarkerStyle(20)
    th.Draw('histo')
    th.GetXaxis().SetTitle(xtitle)
    h_data.Draw('epsame')
    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.AddEntry( hs_0[1], 'Water' ,'f') ;
    leg.AddEntry( hs_0[2], 'Iron' ,'f') ;
    leg.AddEntry( hs_0[3], 'Lead' ,'f') ;
    leg.AddEntry( hs_0[4], 'Pure Carbon' ,'f') ;
    leg.AddEntry( hs_0[0], 'Scintillator' ,'f') ;
    leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    if oneNeutron:
       fname = 'plots/mat/'+playlist+'/oneNeutron/'+fname
    elif moreOneNeutron:
       fname = 'plots/mat/'+playlist+'/moreOneNeutron/'+fname
    else:
       fname = 'plots/mat/'+playlist+'/'+fname
       
    dir_path = os.path.dirname(os.path.realpath(fname))
    os.system('mkdir -p '+dir_path)
    c1.Print(fname)
    c1.Print(fname.replace('.pdf','.png'))
    c1.SetLogy()
    c1.Print(fname.replace('.pdf','_log.pdf'))
    c1.Print(fname.replace('.pdf','_log.png'))

def drawPlotProc(hs_0,h_data,xtitle,fname):
    # 0 -> QE
    # 1 -> RES
    # 2 -> DIS
    # 3 -> COH
    # 4 -> 2p2h
    # 5 -> other

    hs_0[0].SetFillColor(ROOT.kRed);
    hs_0[1].SetFillColor(ROOT.kOrange);
    hs_0[2].SetFillColor(ROOT.kGreen-3);
    hs_0[3].SetFillColor(ROOT.kMagenta);
    hs_0[4].SetFillColor(ROOT.kBlue);
    hs_0[5].SetFillColor(ROOT.kBlack);
    
    c1 = ROOT.TCanvas('c1')
    th = ROOT.THStack();

    th.Add(hs_0[0])
    th.Add(hs_0[4])
    th.Add(hs_0[1])
    th.Add(hs_0[2])
    th.Add(hs_0[3])
    th.Add(hs_0[5])

    h_data.SetMarkerStyle(20)
    th.Draw('histo')
    th.GetXaxis().SetTitle(xtitle)
    h_data.Draw('epsame')
    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.AddEntry( hs_0[0], 'QE' ,'f') ;
    leg.AddEntry( hs_0[4], '2p2h' ,'f') ;
    leg.AddEntry( hs_0[1], 'RES' ,'f') ;
    leg.AddEntry( hs_0[2], 'DIS' ,'f') ;
    leg.AddEntry( hs_0[3], 'COH' ,'f') ;
    leg.SetFillColor( ROOT.kWhite ) ;
    leg.Draw();
    if oneNeutron:
       fname = 'plots/proc/'+playlist+'/oneNeutron/'+fname
    elif moreOneNeutron:
       fname = 'plots/proc/'+playlist+'/moreOneNeutron/'+fname
    else:
       fname = 'plots/proc/'+playlist+'/'+fname

    dir_path = os.path.dirname(os.path.realpath(fname))
    os.system('mkdir -p '+dir_path)
    c1.Print(fname)
    c1.Print(fname.replace('.pdf','.png'))
    c1.SetLogy()
    c1.Print(fname.replace('.pdf','_log.pdf'))
    c1.Print(fname.replace('.pdf','_log.png'))

def drawPlot2D(hs_0,h_data,xtitle,ytitle,fname):

    c1 = ROOT.TCanvas('c1')

    hs_0[0].Add(hs_0[1])
    hs_0[0].Add(hs_0[2])
    hs_0[0].Add(hs_0[3])
    hs_0[0].Add(hs_0[4])
    hs_0[0].Add(hs_0[5])
    
    h_data.SetMarkerColor(ROOT.kRed)
    #hs_0[0].SetMarkerStyle(3)
    hs_0[0].Draw("colz")
    #h_data.Draw('boxsame')
    leg = ROOT.TLegend( 0.68, 0.50, 0.88, 0.65 ) ;
    leg.AddEntry( hs_0[0], 'MC') ;
    leg.AddEntry( h_data, 'Data') ;
    leg.SetFillColor( ROOT.kWhite ) ;
    #leg.Draw();
    if oneNeutron:
       fname = 'plots/'+playlist+'/oneNeutron/'+fname
    elif moreOneNeutron:
       fname = 'plots/'+playlist+'/moreOneNeutron/'+fname
    else:
       fname = 'plots/'+playlist+'/'+fname
       
    dir_path = os.path.dirname(os.path.realpath(fname))
    os.system('mkdir -p '+dir_path)
    c1.Print(fname)
    c1.Print(fname.replace('.pdf','.png'))
    c1.SetLogy()
    c1.Print(fname.replace('.pdf','_log.pdf'))
    c1.Print(fname.replace('.pdf','_log.png'))

def makeHistos(nhists, bins, ranges):
   histos = []
   histos.append(makeHistosTarget(nhists,bins, ranges,'1'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'2'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'3'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'4'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'5'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'6'))
   histos.append(makeHistosTarget(nhists,bins, ranges,'7'))
   return histos

def makeHistos2D(nhists, bins1, ranges1, bins2, ranges2):
   histos = []
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '1'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '2'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '3'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '4'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '5'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '6'))
   histos.append(makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, '7'))
   return histos

def makeHistosTarget(nhists, bins, ranges, target):
   hs = []
   hs_P = []
   hs_S = []
   hs_S_P = []
   hs_A = []
   hs_A_P = []
   for x in xrange(6):
      hs_S.append(ROOT.TH1F('h_mc_single_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1]))
      hs_S_P.append(ROOT.TH1F('h_mc_single_P_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1]))
      hs.append(ROOT.TH1F('h_mc_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1])) # Z vertex
      hs_P.append(ROOT.TH1F('h_mc_P_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1]))
      hs_A.append(ROOT.TH1F('h_mc_all_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1])) # Z vertex
      hs_A_P.append(ROOT.TH1F('h_mc_all_P_'+nhists+'_'+str(x)+target,'',bins,ranges[0],ranges[1]))

   h_data = ROOT.TH1F('h_data_'+nhists+target,'',bins,ranges[0],ranges[1])
   h_data_S = ROOT.TH1F('h_data_S_'+nhists+target,'',bins,ranges[0],ranges[1])
   h_data_all = ROOT.TH1F('h_data_all_'+nhists+target,'',bins,ranges[0],ranges[1])

   histos = []
   histos.append(hs_S)
   histos.append(hs_S_P)
   histos.append(hs)
   histos.append(hs_P)
   histos.append(hs_A)
   histos.append(hs_A_P)

   histos.append(h_data_S)
   histos.append(h_data)
   histos.append(h_data_all)

   return histos

def makeHistosTarget2D(nhists, bins1, ranges1, bins2, ranges2, target):
   hs = []
   hs_P = []
   hs_S = []
   hs_S_P = []
   hs_A = []
   hs_A_P = []
   for x in xrange(6):
      hs_S.append(ROOT.TH2F('h_mc_single_'+nhists+'_'+str(x)+target,'',
                            bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1]))
      hs_S_P.append(ROOT.TH2F('h_mc_single_P_'+nhists+'_'+str(x)+target,'',
                              bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1]))
      hs.append(ROOT.TH2F('h_mc_'+nhists+'_'+str(x)+target,'',
                          bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1])) # Z vertex
      hs_P.append(ROOT.TH2F('h_mc_P_'+nhists+'_'+str(x)+target,'',
                            bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1]))
      hs_A.append(ROOT.TH2F('h_mc_all_'+nhists+'_'+str(x)+target,'',
                            bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1])) # Z vertex
      hs_A_P.append(ROOT.TH2F('h_mc_all_P_'+nhists+'_'+str(x)+target,'',
                              bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1]))

   h_data = ROOT.TH2F('h_data_'+nhists+target,'',
                      bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1])
   h_data_S = ROOT.TH2F('h_data_S_'+nhists+target,'',
                        bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1])
   h_data_all = ROOT.TH2F('h_data_all_'+nhists+target,'',
                          bins1,ranges1[0],ranges1[1],bins2,ranges2[0],ranges2[1])

   histos = []
   histos.append(hs_S)
   histos.append(hs_S_P)
   histos.append(hs)
   histos.append(hs_P)
   histos.append(hs_A)
   histos.append(hs_A_P)

   histos.append(h_data_S)
   histos.append(h_data)
   histos.append(h_data_all)

   return histos

def fillHistosMC(hs_0,proc,mat,SingleTrackSample,weight,value,target):
   fillHistosTargetMC(hs_0[target],proc,mat,SingleTrackSample,weight,value)
   
def fillHistosTargetMC(hs_0,proc,mat,SingleTrackSample,weight,value):
   if SingleTrackSample == 1:
      hs_0[0][mat].Fill(value,weight)
      hs_0[1][proc].Fill(value,weight)
      
   else:
      hs_0[2][mat].Fill(value,weight)
      hs_0[3][proc].Fill(value,weight)

   
   hs_0[4][mat].Fill(value,weight)
   hs_0[5][proc].Fill(value,weight)
      
def fillHistosMC2D(hs_0,proc,mat,SingleTrackSample,weight,value,value2,target):
   fillHistosTargetMC2D(hs_0[target],proc,mat,SingleTrackSample,weight,value,value2)
   
def fillHistosTargetMC2D(hs_0,proc,mat,SingleTrackSample,weight,value,value2):
   if SingleTrackSample == 1:
      hs_0[0][mat].Fill(value,value2,weight)
      hs_0[1][proc].Fill(value,value2,weight)
      
   else:
      hs_0[2][mat].Fill(value,value2,weight)
      hs_0[3][proc].Fill(value,value2,weight)

   
   hs_0[4][mat].Fill(value,value2,weight)
   hs_0[5][proc].Fill(value,value2,weight)
      
def fillHistosData(hs_0,SingleTrackSample,value,target):
   fillHistosTargetData(hs_0[target],SingleTrackSample,value)
   
def fillHistosTargetData(hs_0,SingleTrackSample,value):
   if SingleTrackSample == 1:
      hs_0[6].Fill(value)
   else:
      hs_0[7].Fill(value)
   hs_0[8].Fill(value)

def fillHistosData2D(hs_0,SingleTrackSample,value,value2,target):
   fillHistosTargetData2D(hs_0[target],SingleTrackSample,value,value2)
   
def fillHistosTargetData2D(hs_0,SingleTrackSample,value,value2):
   if SingleTrackSample == 1:
      hs_0[6].Fill(value,value2)
   else:
      hs_0[7].Fill(value,value2)
   hs_0[8].Fill(value,value2)

def drawPlots(hs_0,xname,fname):
   drawPlotMat(hs_0[0],hs_0[6],xname,'single/'+fname+'_mat_S.pdf')
   drawPlotProc(hs_0[1],hs_0[6],xname,'single/'+fname+'_proc_S.pdf')

   drawPlotMat(hs_0[2],hs_0[7],xname,'multi/'+fname+'_mat.pdf')
   drawPlotProc(hs_0[3],hs_0[7],xname,'multi/'+fname+'_proc.pdf')
   
   drawPlotMat(hs_0[4],hs_0[8],xname,'all/'+fname+'_mat_all.pdf')
   drawPlotProc(hs_0[5],hs_0[8],xname,'all/'+fname+'_proc_all.pdf')

def drawPlots2D(hs_0,xname,yname,fname):
   drawPlot2D(hs_0[0],hs_0[6],xname,yname,'single/'+fname+'_S.pdf')

   drawPlot2D(hs_0[2],hs_0[7],xname,yname,'multi/'+fname+'.pdf')
   
   drawPlot2D(hs_0[4],hs_0[8],xname,yname,'all/'+fname+'_all.pdf')

   
def pass_neutron_cuts(e):
   if oneNeutron and e.neutron3d_N != 1: return False
   if moreOneNeutron and e.neutron3d_N == 0: return False
   if moreOneNeutron and e.neutron3d_N > 3: return False
   return True


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
      hs_0 = makeHistos('0',85,[4400,6100]) # Z vertex
      hs_1 = makeHistos('1',100,[0,13000]) # muon momentum
      hs_2 = makeHistos('2',bins,[-1000,1000]) # X vertex
      hs_3 = makeHistos('3',bins,[-1000,1000]) # Y vertex
      hs_4 = makeHistos('4',20,[0,20]) # Neutrons 3d
      hs_5 = makeHistos('5',20,[0,20]) # Neutrons prox
      hs_6 = makeHistos('6',40,[0,40]) # Neutrons 3d clusters
      hs_7 = makeHistos('7',100,[0,400]) # Neutrons prox clusters
      hs_8 = makeHistos('8',100,[0,2000]) # Hadronic energy
      
      hs_9 = makeHistos('9',100,[0,500]) # Neutrons 3d energy
      hs_10 = makeHistos('10',100,[0,2000]) # Neutrons prox energy
      hs_11 = makeHistos('11',bins,[-1000,1000]) # Neutrons 3d x
      hs_12 = makeHistos('12',bins,[-1000,1000]) # Neutrons 3d y
      hs_13 = makeHistos('13',bins,[4400,7100]) # Neutrons 3d z
      hs_14 = makeHistos('14',bins,[-1000,1000]) # Neutrons prox x
      hs_15 = makeHistos('15',bins,[-1000,1000]) # Neutrons prox y
      hs_16 = makeHistos('16',bins,[4400,7100]) # Neutrons prox z
      
      hs_17 = makeHistos('17',bins,[-1000,1000]) # Protons x
      hs_18 = makeHistos('18',bins,[-1000,1000]) # Protons y
      hs_19 = makeHistos('19',bins,[4400,7100]) # Protons z
      
      hs_20 = makeHistos('20',bins,[0,20000]) # Recoil E
      hs_21 = makeHistos('21',bins,[0,50]) # Primary Vertex Energy
      hs_22 = makeHistos('22',bins,[0,5000]) # Recoil E
      hs_23 = makeHistos('23',bins,[0,2000]) # Recoil E

      hs_24 = makeHistos('24',10,[0,10]) # Improved N Michel
      
      hs_2D_0 = makeHistos2D('0',bins,[0,2000],bins,[0,2000])
      
   i = 0
   nentries = t_mc_0.GetEntries()
   timeNow = time.time()

   mcwgt = mcweight.MCweight()
   
   for e in t_mc_0:
      if i%10000 == 0:
         print "%d/%d"%(i,nentries)
         #print time.time() - timeNow 
         timeNow = time.time()
      i += 1
      if i > 10000 and short_run: break

      if not pass_cuts(e): continue
      if not pass_neutron_cuts(e): continue

      '''
      if target == 't1':
         if not (target1_cut(e.vtx[2]) or target1_scint_cut(e.vtx[2])): continue
      elif target == 't2':
         if not (target2_cut(e.vtx[2]) or target2_scint_cut(e.vtx[2])): continue
      elif target == 't3':
         if not (target3_cut(e.vtx[2]) or target3_scint_cut(e.vtx[2])): continue
      elif target == 't4':
         if not (target4_cut(e.vtx[2]) or target4_scint_cut(e.vtx[2])): continue
      elif target == 't5':
         if not (target5_cut(e.vtx[2]) or target5_scint_cut(e.vtx[2])): continue
            
      if target == 't1':
         if not target1_cut(e.vtx[2]): continue
      elif target == 't2':
         if not target2_cut(e.vtx[2]): continue
      elif target == 't3':
         if not target3_cut(e.vtx[2]): continue
      elif target == 't4':
         if not target4_cut(e.vtx[2]): continue
      elif target == 't5':
         if not target5_cut(e.vtx[2]): continue
      '''   
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

      # Fill histos
      if True:
         fillHistosMC(hs_0,proc,mat,single_sample,e.wgt*weight,e.vtx[2],5)
         fillHistosMC(hs_1,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_muon_p,5)
         fillHistosMC(hs_2,proc,mat,single_sample,e.wgt*weight,e.vtx[0],5)
         fillHistosMC(hs_3,proc,mat,single_sample,e.wgt*weight,e.vtx[1],5)
         fillHistosMC(hs_4,proc,mat,single_sample,e.wgt*weight,e.neutron3d_N,5)
         fillHistosMC(hs_5,proc,mat,single_sample,e.wgt*weight,e.neutronprox_N,5)
         for nc in xrange(min(5,len(e.neutron3d_nclusters))):
            if e.neutron3d_x[nc] == 0.0 and e.neutron3d_y[nc] == 0.0: continue
            fillHistosMC(hs_6,proc,mat,single_sample,e.wgt*weight,e.neutron3d_nclusters[nc],5)
            fillHistosMC(hs_9,proc,mat,single_sample,e.wgt*weight,e.neutron3d_energy[nc],5)
            fillHistosMC(hs_11,proc,mat,single_sample,e.wgt*weight,e.neutron3d_x[nc],5)
            fillHistosMC(hs_12,proc,mat,single_sample,e.wgt*weight,e.neutron3d_y[nc],5)
            fillHistosMC(hs_13,proc,mat,single_sample,e.wgt*weight,e.neutron3d_z[nc],5)
         for nc in xrange(min(5,len(e.neutronprox_nclusters))):
            if e.neutronprox_x[nc] == 0.0 and e.neutronprox_y[nc] == 0.0: continue
            fillHistosMC(hs_7,proc,mat,single_sample,e.wgt*weight,e.neutronprox_nclusters[nc],5)
            fillHistosMC(hs_10,proc,mat,single_sample,e.wgt*weight,e.neutronprox_energy[nc],5)
            fillHistosMC(hs_14,proc,mat,single_sample,e.wgt*weight,e.neutronprox_x[nc],5)
            fillHistosMC(hs_15,proc,mat,single_sample,e.wgt*weight,e.neutronprox_y[nc],5)
            fillHistosMC(hs_16,proc,mat,single_sample,e.wgt*weight,e.neutronprox_z[nc],5)
            
         fillHistosMC(hs_8,proc,mat,single_sample,e.wgt*weight,e.hadronic_energy,5)

         for p in xrange(min(5,len(e.NukeCCQETwoTrack_proton_startPointX))):
            fillHistosMC(hs_17,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointX[p],5)
            fillHistosMC(hs_18,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointY[p],5)
            fillHistosMC(hs_19,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointZ[p],5)
            
         fillHistosMC(hs_20,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,5)
         fillHistosMC(hs_21,proc,mat,single_sample,e.wgt*weight,e.primaryVertexEnergy,5)
         fillHistosMC(hs_22,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,5)
         fillHistosMC(hs_23,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,5)

         fillHistosMC(hs_24,proc,mat,single_sample,e.wgt*weight,e.improved_nmichel,5)
         fillHistosMC2D(hs_2D_0,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,5)


      
      target = -1
      if target1_cut(e.vtx[2]): target = 0
      elif target2_cut(e.vtx[2]): target = 1
      elif target3_cut(e.vtx[2]): target = 2
      elif target4_cut(e.vtx[2]): target = 3
      elif target5_cut(e.vtx[2]): target = 4
      elif targetW_cut(e.vtx[2]): target = 6
      else: continue
      
      # Fill target histos
      if True:
         fillHistosMC(hs_0,proc,mat,single_sample,e.wgt*weight,e.vtx[2],target)
         fillHistosMC(hs_1,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_muon_p,target)
         fillHistosMC(hs_2,proc,mat,single_sample,e.wgt*weight,e.vtx[0],target)
         fillHistosMC(hs_3,proc,mat,single_sample,e.wgt*weight,e.vtx[1],target)
         fillHistosMC(hs_4,proc,mat,single_sample,e.wgt*weight,e.neutron3d_N,target)
         fillHistosMC(hs_5,proc,mat,single_sample,e.wgt*weight,e.neutronprox_N,target)
         for nc in xrange(min(5,len(e.neutron3d_nclusters))):
            if e.neutron3d_x[nc] == 0.0 and e.neutron3d_y[nc] == 0.0: continue
            fillHistosMC(hs_6,proc,mat,single_sample,e.wgt*weight,e.neutron3d_nclusters[nc],target)
            fillHistosMC(hs_9,proc,mat,single_sample,e.wgt*weight,e.neutron3d_energy[nc],target)
            fillHistosMC(hs_11,proc,mat,single_sample,e.wgt*weight,e.neutron3d_x[nc],target)
            fillHistosMC(hs_12,proc,mat,single_sample,e.wgt*weight,e.neutron3d_y[nc],target)
            fillHistosMC(hs_13,proc,mat,single_sample,e.wgt*weight,e.neutron3d_z[nc],target)
         for nc in xrange(min(5,len(e.neutronprox_nclusters))):
            if e.neutronprox_x[nc] == 0.0 and e.neutronprox_y[nc] == 0.0: continue
            fillHistosMC(hs_7,proc,mat,single_sample,e.wgt*weight,e.neutronprox_nclusters[nc],target)
            fillHistosMC(hs_10,proc,mat,single_sample,e.wgt*weight,e.neutronprox_energy[nc],target)
            fillHistosMC(hs_14,proc,mat,single_sample,e.wgt*weight,e.neutronprox_x[nc],target)
            fillHistosMC(hs_15,proc,mat,single_sample,e.wgt*weight,e.neutronprox_y[nc],target)
            fillHistosMC(hs_16,proc,mat,single_sample,e.wgt*weight,e.neutronprox_z[nc],target)
            
         fillHistosMC(hs_8,proc,mat,single_sample,e.wgt*weight,e.hadronic_energy,target)

         for p in xrange(min(5,len(e.NukeCCQETwoTrack_proton_startPointX))):
            fillHistosMC(hs_17,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointX[p],target)
            fillHistosMC(hs_18,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointY[p],target)
            fillHistosMC(hs_19,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_proton_startPointZ[p],target)
            
         fillHistosMC(hs_20,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,target)
         fillHistosMC(hs_21,proc,mat,single_sample,e.wgt*weight,e.primaryVertexEnergy,target)
         fillHistosMC(hs_22,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,target)
         fillHistosMC(hs_23,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,target)

         fillHistosMC(hs_24,proc,mat,single_sample,e.wgt*weight,e.improved_nmichel,target)

         fillHistosMC2D(hs_2D_0,proc,mat,single_sample,e.wgt*weight,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,target)
         

   print 'Pass n=',pass_entries
   print 'Entries=',t_data.GetEntries()
   pass_entries = 0

   i = 0
   nentries = t_data.GetEntries()
   for e in t_data:
      if i%10000 == 0:
         print "%d/%d"%(i,nentries)

      i += 1
      if i > 100000 and short_run: break

      if not pass_cuts(e): continue
      if not pass_neutron_cuts(e): continue
        
      '''           
      if target == 't1':
         if not (target1_cut(e.vtx[2]) or target1_scint_cut(e.vtx[2])): continue
      elif target == 't2':
         if not (target2_cut(e.vtx[2]) or target2_scint_cut(e.vtx[2])): continue
      elif target == 't3':
         if not (target3_cut(e.vtx[2]) or target3_scint_cut(e.vtx[2])): continue
      elif target == 't4':
         if not (target4_cut(e.vtx[2]) or target4_scint_cut(e.vtx[2])): continue
      elif target == 't5':
         if not (target5_cut(e.vtx[2]) or target5_scint_cut(e.vtx[2])): continue
                       
      if target == 't1':
         if not target1_cut(e.vtx[2]): continue
      elif target == 't2':
         if not target2_cut(e.vtx[2]): continue
      elif target == 't3':
         if not target3_cut(e.vtx[2]): continue
      elif target == 't4':
         if not target4_cut(e.vtx[2]): continue
      elif target == 't5':
         if not target5_cut(e.vtx[2]): continue
      '''
      pass_entries += 1
      single_sample = e.SingleTrackSample

      # Fill histos
      if True:
         fillHistosData(hs_0,single_sample,e.vtx[2],5)
         fillHistosData(hs_1,single_sample,e.NukeCCQETwoTrack_muon_p,5)
         fillHistosData(hs_2,single_sample,e.vtx[0],5)
         fillHistosData(hs_3,single_sample,e.vtx[1],5)
         fillHistosData(hs_4,single_sample,e.neutron3d_N,5)
         fillHistosData(hs_5,single_sample,e.neutronprox_N,5)

         for nc in xrange(min(5,len(e.neutron3d_nclusters))):
            if e.neutron3d_x[nc] == 0.0 and e.neutron3d_y[nc] == 0.0: continue
            fillHistosData(hs_6,single_sample,e.neutron3d_nclusters[nc],5)
            fillHistosData(hs_9,single_sample,e.neutron3d_energy[nc],5)
            fillHistosData(hs_11,single_sample,e.neutron3d_x[nc],5)
            fillHistosData(hs_12,single_sample,e.neutron3d_y[nc],5)
            fillHistosData(hs_13,single_sample,e.neutron3d_z[nc],5)
         for nc in xrange(min(5,len(e.neutronprox_nclusters))):
            if e.neutronprox_x[nc] == 0.0 and e.neutronprox_y[nc] == 0.0: continue
            fillHistosData(hs_7,single_sample,e.neutronprox_nclusters[nc],5)
            fillHistosData(hs_10,single_sample,e.neutronprox_energy[nc],5)
            fillHistosData(hs_14,single_sample,e.neutronprox_x[nc],5)
            fillHistosData(hs_15,single_sample,e.neutronprox_y[nc],5)
            fillHistosData(hs_16,single_sample,e.neutronprox_z[nc],5)

         fillHistosData(hs_8,single_sample,e.hadronic_energy,5)
         fillHistosData(hs_20,single_sample,e.NukeCCQETwoTrack_recoilE,5)
         fillHistosData(hs_21,single_sample,e.primaryVertexEnergy,5)
         fillHistosData(hs_22,single_sample,e.NukeCCQETwoTrack_recoilE,5)
         fillHistosData(hs_23,single_sample,e.NukeCCQETwoTrack_recoilE,5)

         fillHistosData(hs_24,single_sample,e.improved_nmichel,5)

         fillHistosData2D(hs_2D_0,single_sample,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,5)

      
      target = -1
      if target1_cut(e.vtx[2]): target = 0
      elif target2_cut(e.vtx[2]): target = 1
      elif target3_cut(e.vtx[2]): target = 2
      elif target4_cut(e.vtx[2]): target = 3
      elif target5_cut(e.vtx[2]): target = 4
      elif targetW_cut(e.vtx[2]): target = 6
      else: continue
      
      # Fill target histos
      if True:
         fillHistosData(hs_0,single_sample,e.vtx[2],target)
         fillHistosData(hs_1,single_sample,e.NukeCCQETwoTrack_muon_p,target)
         fillHistosData(hs_2,single_sample,e.vtx[0],target)
         fillHistosData(hs_3,single_sample,e.vtx[1],target)
         fillHistosData(hs_4,single_sample,e.neutron3d_N,target)
         fillHistosData(hs_5,single_sample,e.neutronprox_N,target)

         for nc in xrange(min(5,len(e.neutron3d_nclusters))):
            if e.neutron3d_x[nc] == 0.0 and e.neutron3d_y[nc] == 0.0: continue
            fillHistosData(hs_6,single_sample,e.neutron3d_nclusters[nc],target)
            fillHistosData(hs_9,single_sample,e.neutron3d_energy[nc],target)
            fillHistosData(hs_11,single_sample,e.neutron3d_x[nc],target)
            fillHistosData(hs_12,single_sample,e.neutron3d_y[nc],target)
            fillHistosData(hs_13,single_sample,e.neutron3d_z[nc],target)
         for nc in xrange(min(5,len(e.neutronprox_nclusters))):
            if e.neutronprox_x[nc] == 0.0 and e.neutronprox_y[nc] == 0.0: continue
            fillHistosData(hs_7,single_sample,e.neutronprox_nclusters[nc],target)
            fillHistosData(hs_10,single_sample,e.neutronprox_energy[nc],target)
            fillHistosData(hs_14,single_sample,e.neutronprox_x[nc],target)
            fillHistosData(hs_15,single_sample,e.neutronprox_y[nc],target)
            fillHistosData(hs_16,single_sample,e.neutronprox_z[nc],target)

         fillHistosData(hs_8,single_sample,e.hadronic_energy,target)
         fillHistosData(hs_20,single_sample,e.NukeCCQETwoTrack_recoilE,target)
         fillHistosData(hs_21,single_sample,e.primaryVertexEnergy,target)
         fillHistosData(hs_22,single_sample,e.NukeCCQETwoTrack_recoilE,target)
         fillHistosData(hs_23,single_sample,e.NukeCCQETwoTrack_recoilE,target)

         fillHistosData(hs_24,single_sample,e.improved_nmichel,target)

         fillHistosData2D(hs_2D_0,single_sample,e.NukeCCQETwoTrack_recoilE,e.NukeCCQETwoTrack_muon_q2,target)


   scale = pot_data/pot_mc
   print 'Pass n=',pass_entries

   # Draw plots
   for i,targetN in enumerate(['t1','t2','t3','t4','t5','all','tW']):
      
      drawPlots(hs_0[i],'Vertex Z [mm]',targetN+'/zpos')      
      drawPlots(hs_1[i],'Muon momentum [GeV/c]',targetN+'/mom_mu')
      drawPlots(hs_2[i],'Vertex X [mm]',targetN+'/xpos')
      drawPlots(hs_3[i],'Vertex Y [mm]',targetN+'/ypos')
      drawPlots(hs_4[i],'Neutrons 3D',targetN+'/neutron3d')
      drawPlots(hs_5[i],'Neutrons Prox',targetN+'/neutronProx')
      drawPlots(hs_6[i],'Neutrons 3D NClusters',targetN+'/neutron3d_nclusters')
      drawPlots(hs_7[i],'Neutrons Prox NClusters',targetN+'/neutronProx_nclusters')
      drawPlots(hs_8[i],'Hadronic Energy [MeV]',targetN+'/hadronic_E')
      drawPlots(hs_9[i],'Neutrons 3D Energy [MeV]',targetN+'/neutron3d_E')
      drawPlots(hs_11[i],'Neutrons 3D X [mm]',targetN+'/neutron3d_x')
      drawPlots(hs_12[i],'Neutrons 3D Y [mm]',targetN+'/neutron3d_y')
      drawPlots(hs_13[i],'Neutrons 3D Z [mm]',targetN+'/neutron3d_z')
      drawPlots(hs_10[i],'Neutrons Prox Energy [MeV]',targetN+'/neutronprox_E')
      drawPlots(hs_14[i],'Neutrons Prox X [mm]',targetN+'/neutronprox_x')
      drawPlots(hs_15[i],'Neutrons Prox Y [mm]',targetN+'/neutronprox_y')
      drawPlots(hs_16[i],'Neutrons Prox Z [mm]',targetN+'/neutronprox_z')
      drawPlots(hs_20[i],'Recoil E [MeV]',targetN+'/recoilE')
      drawPlots(hs_21[i],'Primary Vertex Energy [MeV]',targetN+'/vertexE')
      drawPlots(hs_22[i],'Recoil E [MeV]',targetN+'/recoilE_reduced')
      drawPlots(hs_23[i],'Recoil E [MeV]',targetN+'/recoilE_reduced2')
      drawPlots(hs_24[i],'N Michel',targetN+'/improvedNmichel')
      
      drawPlots2D(hs_2D_0[i],'Recoil E [MeV]','Q2 [MeV]',targetN+'/recoilE_vs_q2')
      
if __name__ == "__main__":
   main()
