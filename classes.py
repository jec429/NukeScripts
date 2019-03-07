import ROOT
from functions import *
from systematicsFunctions import *

class MasterPlot:

  def __init__( self ):
    self.curves = [] 
    self.playlists = []
    self.dummyHists = []
    self.drawDummyLegend = False
    self.xTitle = None
    self.yTitle = None
    self.yMin = None
    self.yMax = None
    self.legYOffset = 0
    self.leg2Y0 = 0
    self.legendX1=0.60
    self.legendY1=0.15
    self.legendX2=0.85
    self.legendY2=0.15
    self.setLog = False
    self.dontDrawLowNuLines = False
  
    self.TCanvas = ROOT.TCanvas( "canvas" , "canvas" , 10 , 10 , 1000, 750 )

  def AddCurve( self , curve , data_set ):
    self.curves.append([curve,data_set])
    if len(self.curves) == 1:
      curve.Draw()
    else:
      curve.Draw("same")

  def DrawTitles( self ):
    self.curves[0][0].SetXTitle( self.xTitle )
    self.curves[0][0].SetYTitle( self.yTitle )

  def SetBounds( self ):
    self.curves[0][0].SetMinimum( self.yMin )
    self.curves[0][0].SetMaximum( self.yMax )

  def CountUniqueDataSets( self , curves):
    uniqueDataSets = []
    for curve,data_set in curves:
      if data_set not in uniqueDataSets: uniqueDataSets.append(data_set)
    
    return uniqueDataSets

  def SetStandardLegendStyle( self , legend ):
    legend.SetNColumns(1)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.SetTextFont(42)

  def DrawLegend( self ):
    playlists = self.CountUniqueDataSets(self.curves)
    n_playlists = len(playlists)
    if n_playlists == 1: self.legYOffset = 0.035 # in the case of only one playlist, artificially raise center of legend in y-direction
    else: self.legYOffset = 0.0
    self.legYCenter = self.legendY1 + 0.07*n_playlists/2 # Determine vertical center of first legend, which will scale with number of playlists
    self.leg2Y0 = self.legYCenter - 0.07 # Fix vertical position of second legend to center on first
    legend = ROOT.TLegend(self.legendX1,self.legendY1+self.legYOffset,self.legendX2,self.legendY2+(0.07*n_playlists)+self.legYOffset) # legend for playlists

    self.SetStandardLegendStyle(legend)

    for playlist in playlists:
      legend.AddEntry(playlist.dummyHist,playlist.label,"l")

    return legend

  def Draw( self , file_path ):
    if self.setLog==True: 
      self.TCanvas.SetLogy()
    if not self.dontDrawLowNuLines:
      drawLowNuLines(self.yMin,self.yMax)
    self.DrawTitles()
    if not self.dontDrawLowNuLines:
      self.SetBounds()
    legend = self.DrawLegend()
    legend.Draw()
    if self.drawDummyLegend: 
      dummyLegend = self.DummyLegend()
      dummyLegend.Draw()
    self.TCanvas.Print(file_path)

class EfficiencyPlot( MasterPlot ):

  def __init__( self ):
    MasterPlot.__init__(self)
    #---------- Set dummyHist Specs
    self.drawDummyLegend=True
    self.dummyHists.append(ROOT.TH1D('h_dummy_Inclusive','h_dummy_Inclusive',10,0.0,10.0))
    self.dummyHists.append(ROOT.TH1D('h_dummy_LowNu','h_dummy_LowNu',10,0.0,10.0))
    #self.dummyHists[1].SetMarkerStyle(ROOT.kCircle)
    self.dummyHists[1].SetMarkerStyle(25)
    #----------
    self.xTitle = "Reconstructed Neutrino Energy (GeV)"
    self.yTitle = "Efficiency"
    self.yMin = 0.0
    self.yMax = 1.0 
    #self.GetXaxis().SetNdivisions(410)
    #self.GetYaxis().SetNdivisions(407)

  def DummyLegend( self ):
    dummyLegend = ROOT.TLegend(0.43,self.leg2Y0+self.legYOffset,0.60,self.leg2Y0+0.14+self.legYOffset)
    self.SetStandardLegendStyle(dummyLegend)

    dummyLegend.AddEntry(self.dummyHists[0],"Inclusive","p")
    #dummyLegend.AddEntry(self.dummyHists[1],"Low Nu","p")
    dummyLegend.AddEntry(self.dummyHists[1],"High Nu","p")

    return dummyLegend

class EventRatePlot( MasterPlot ):

  def __init__( self ):
    MasterPlot.__init__(self)
    #---------- Set dummyHist Specs
    self.drawDummyLegend=True
    self.dummyHists.append(ROOT.TH1D('h_dummy_eventRate_1','h_dummy_eventRate_1',10,0.0,10.0))
    self.dummyHists.append(ROOT.TH1D('h_dummy_eventRate_2','h_dummy_eventRate_2',10,0.0,10.0))
    self.dummyHists[0].SetMarkerStyle(23)
    self.dummyHists[1].SetMarkerStyle(26)
    #---------- Set custom Legend Coordinates
    self.legendX1=0.60
    self.legendY1=0.15
    self.legendX2=0.85
    self.legendY2=0.15
    #----------
    self.xTitle = "Reconstructed Neutrino Energy (GeV)"
    self.yTitle = "Event Rate"
    self.yMin = 1
    self.yMax = 2*10**6
    self.setLog=True
    #self.GetXaxis().SetNdivisions(410)
    #self.GetYaxis().SetNdivisions(407)

  def DummyLegend( self ):
    dummyLegend = ROOT.TLegend(0.43,self.leg2Y0+self.legYOffset,0.60,self.leg2Y0+0.14+self.legYOffset)
    self.SetStandardLegendStyle(dummyLegend)

    dummyLegend.AddEntry(self.dummyHists[0],"MC Reco","p")
    dummyLegend.AddEntry(self.dummyHists[1],"MC Truth","p")

    return dummyLegend

class EventRatePlotData( EventRatePlot ):

  def __init__( self ):
    EventRatePlot.__init__(self)
    self.xTitle = "Reconstructed Neutrino Energy (GeV)" 

  def DummyLegend( self ):
    dummyLegend = ROOT.TLegend(0.43,self.leg2Y0+self.legYOffset,0.60,self.leg2Y0+0.14+self.legYOffset)
    self.SetStandardLegendStyle(dummyLegend)

    dummyLegend.AddEntry(self.dummyHists[0],"MC Reco","p")

    return dummyLegend

class FluxPlot( MasterPlot ):

  def __init__( self ):
    MasterPlot.__init__(self)
    self.xTitle = "Reconstructed Neutrino Energy (GeV)"
    self.yTitle = "Flux (kinda-POT-normalized)"    
    self.yMin = 0.0
    self.yMax = 10**4
    self.dontDrawLowNuLines = True

class Playlist: 

  def __init__( self ):
    self.label = None
    self.color = None
    self.dummyHist = None

  def setLabel( self , label ):
    self.label = label

  def setColor( self , color_string ):
    self.color = ROOT.TColor.GetColor(color_string)

  def setDummyHist( self ):
    if not self.label: print "You must setLabel() before you attempt to setDummyHist()"
    self.dummyHist = ROOT.TH1D('h_dummy_%s'%self.label,'h_dummy_%s'%self.label,10,0.0,10.0)
    self.dummyHist.SetLineColor(self.color)
    self.dummyHist.SetMarkerColor(self.color)

