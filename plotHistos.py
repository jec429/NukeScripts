import ROOT
from lists import *
from functions import *
from plottingClasses import *

ROOT.gROOT.SetBatch()

ROOT.TH1.AddDirectory(False)

plotter = PlotUtils.MnvPlotter()
targetUtils = PlotUtils.TargetUtils()

mcHistsFile = ROOT.TFile('systematics_6A_minerva.root')

SIGNAL_DEFINITIONS = [
  'inclusive'
]

PLAYLISTS_LE = [
  #'minerva1',
  #'minerva7',
  #'minerva9',
  #'minerva13',
  #'2p2h'
]

PLAYLISTS_ME = [
  'minervame6A',
]

FLUX_COMPONENTS = [
  'dataRate',
  'effNumerator',
  'effDenominator'
]

HISTDIR_LE = '/minerva/data/users/jchaves/highNu/mergedHists/LE-MECAnaTool-Tuples_2019-02-26'
HISTDIR_ME = '/minerva/data/users/jchaves/highNu/mergedHists/ME-NukeCC-Tuples_2019-02-26'
plotDir    = 'plots'


for PLAYLISTS,HISTDIR,isME in zip([PLAYLISTS_LE,PLAYLISTS_ME],[HISTDIR_LE,HISTDIR_ME],[False,True]):
  for playlist in PLAYLISTS: 
    print 'playlist: ' , playlist
    print 'HISTDIR: ' , HISTDIR
    print 'isME: ' , isME
    
    potsh = mcHistsFile.Get("potsh")
        
    mcPOT_used,mcPOT_total = potsh.GetBinContent(1),potsh.GetBinContent(3)
    mcPOT_ratio = mcPOT_used/mcPOT_total
    dataPOT = potsh.GetBinContent(2)
    scaleFactor = dataPOT/mcPOT_used
    #scaleFactor = 1.0
    #mcPOT_ratio = 1.0

    for target in ['','t1_','t2_','t3_','t4_','t5_','tW_']: 
        for sigDef in SIGNAL_DEFINITIONS:
            key = '{0}_{1}'.format(sigDef,playlist)
            exec("dataRateHist2D_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco')".format(key,target,sigDef))
            exec("dataRateHist_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco').ProjectionX()".format(key,target,sigDef))
            exec("dataRateHist_Y_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco').ProjectionY()".format(key,target,sigDef))
            exec("effNumeratorHist2D_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco')".format(key,target,sigDef))
            exec("effNumeratorHist_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco').ProjectionX()".format(key,target,sigDef))
            exec("effNumeratorHist_Y_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_reco').ProjectionY()".format(key,target,sigDef))
            exec("effDenominatorHist2D_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_truth')".format(key,target,sigDef))
            exec("effDenominatorHist_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_truth').ProjectionX()".format(key,target,sigDef))
            exec("effDenominatorHist_Y_{0} = mcHistsFile.Get('h_Mupt_VS_Mupz_{1}{2}_truth').ProjectionY()".format(key,target,sigDef))

            # Scale MC to the POT of data
            exec("effNumeratorHist_{0}.Scale(scaleFactor)".format(key))
            exec("effNumeratorHist_Y_{0}.Scale(scaleFactor)".format(key))
            exec("effNumeratorHist2D_{0}.Scale(scaleFactor)".format(key))
            exec("effDenominatorHist_{0}.Scale(scaleFactor*mcPOT_ratio)".format(key)) # Truth distribution doesn't have data-quality pre-selection that reco MC does. This is the Eroica 'POT-Counting' bug, which is corrected for by scaling the truth distribution by the ratio of POT_Used to POT_Total
            exec("effDenominatorHist_Y_{0}.Scale(scaleFactor*mcPOT_ratio)".format(key)) # Truth distribution doesn't have data-quality pre-selection that reco MC does. This is the Eroica 'POT-Counting' bug, which is corrected for by scaling the truth distribution by the ratio of POT_Used to POT_Total
            exec("effDenominatorHist2D_{0}.Scale(scaleFactor*mcPOT_ratio)".format(key))

            # Plot raw flux components
            for component in FLUX_COMPONENTS:
                print 'comp=',component,' key=',key
                with makeEnv_TCanvas('{0}/fluxComponents_byPlaylist/{1}_{2}_{3}pt.png'.format(plotDir,component,key,target)):
                    exec("setPlotSpecs_{0}({0}Hist_{1},'Mupt')".format(component,key))
                    exec("{0}Hist_{1}.Draw('PE')".format(component,key))
                with makeEnv_TCanvas('{0}/fluxComponents_byPlaylist/errorSummary_{1}_{2}_{3}pt.png'.format(plotDir,component,key,target)):
                    exec("plotter.DrawErrorSummary({0}Hist_{1})".format(component,key))

                with makeEnv_TCanvas('{0}/fluxComponents_byPlaylist/{1}_{2}_{3}pz.png'.format(plotDir,component,key,target)):
                    exec("setPlotSpecs_{0}({0}Hist_Y_{1},'Mupz')".format(component,key))
                    exec("{0}Hist_Y_{1}.Draw('PE')".format(component,key))
                with makeEnv_TCanvas('{0}/fluxComponents_byPlaylist/errorSummary_{1}_{2}_{3}pz.png'.format(plotDir,component,key,target)):
                    exec("plotter.DrawErrorSummary({0}Hist_Y_{1})".format(component,key))

