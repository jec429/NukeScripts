import ROOT
import PlotUtils

from array import *
from lists import *
import math,os

def copyHist( inHist ):

  tempHist = inHist.Clone( "doesThisEvenMatter?" )
  tempHist.Sumw2()

  return tempHist

class WrapChain(ROOT.TChain):

  def __init__(self, name):
    ROOT.TChain.__init__(self, name)

  def LoadTree(self, entry):
    self.local_entry=ROOT.TChain.LoadTree(self, entry)

  def __getattr__(self, name):
    ROOT.TChain.GetBranch(self, name).GetEntry(self.local_entry)
    return ROOT.TChain.__getattr__(self, name)

class HistWrapper():
 
  def __init__(self,*args,**kwargs):
   
    if len(args) == 5: self.init1D(*args)
    if len(args) == 6: self.init2DFromVecs(*args)
    if len(args) == 8: self.init2D(*args)
    if len(args) == 11: self.init3D(*args)
 
    nAssigned = 0
  
    # CV is a special case, because we'll store the MnvHXD itself here, as opposed to the various error bands of the MnvHXD  
    self.eventToUnivMap['CV'] = {}
    self.eventToUnivMap['CV'][0] = self.hist
    
    for systematicUniverseClass in self.systematicUniverses:
        
      # We've already handled this case
      if systematicUniverseClass == 'CV': continue 

      # Create error band if it doesn't exist (it shouldn't), and add corresponding entry to univMap dict
      if not self.hist.HasVertErrorBand(systematicUniverseClass):
        self.eventToUnivMap[systematicUniverseClass]={}
        self.hist.AddVertErrorBand(systematicUniverseClass,len(self.systematicUniverses[systematicUniverseClass]))
      else:
        print 'Error: You\'re trying to create an error band that already exists'

      for i,systematicUniverse in enumerate(self.systematicUniverses[systematicUniverseClass]):

          self.eventToUnivMap[systematicUniverseClass][i] = self.hist.GetVertErrorBand(systematicUniverseClass).GetHist(i)

  def init1D(self,title,nBins,xMin,xMax,systEvents):

    self.title = title
    self.nBins = nBins
    self.xMin = xMin
    self.xMax = xMax
    self.systematicUniverses = systEvents
    self.eventToUnivMap = {}

    self.hist = PlotUtils.MnvH1D('h_%s'%self.title,self.title,self.nBins,self.xMin,self.xMax)
    self.hist.SetDirectory(0)
   
  def init2D(self,title,nXBins,xMin,xMax,nYBins,yMin,yMax,systEvents):
  
    self.title = title
    self.nXBins = nXBins
    self.xMin = xMin
    self.xMax = xMax
    self.nYBins = nYBins
    self.yMin = yMin
    self.yMax = yMax
    self.systematicUniverses = systEvents
    self.eventToUnivMap = {}

    self.hist = PlotUtils.MnvH2D('h_%s'%self.title,self.title,self.nXBins,self.xMin,self.xMax,self.nYBins,self.yMin,self.yMax)
    self.hist.SetDirectory(0)
   
  def init2DFromVecs(self,title,nXBins,xBins,nYBins,yBins,systEvents):
  
    self.title = title
    self.nXBins = nXBins
    self.xBins = xBins
    self.nYBins = nYBins
    self.yBins = yBins
    self.systematicUniverses = systEvents
    self.eventToUnivMap = {}

    self.hist = PlotUtils.MnvH2D('h_%s'%self.title,self.title,self.nXBins,self.xBins,self.nYBins,self.yBins)
    self.hist.SetDirectory(0)

  def init3D(self,title,nXBins,xMin,xMax,nYBins,yMin,yMax,nZBins,zMin,zMax,systEvents):
  
    self.title = title
    self.nXBins = nXBins
    self.xMin = xMin
    self.xMax = xMax
    self.nYBins = nYBins
    self.yMin = yMin
    self.yMax = yMax
    self.nZBins = nZBins
    self.zMin = zMin
    self.zMax = zMax
    self.systematicUniverses = systEvents
    self.eventToUnivMap = {}

    self.hist = PlotUtils.MnvH3D('h_%s'%self.title,self.title,self.nXBins,self.xMin,self.xMax,self.nYBins,self.yMin,self.yMax,self.nZBins,self.zMin,self.zMax)
    self.hist.SetDirectory(0)
   
  def univHist(self,systematicUniverseClass,i):
    return self.eventToUnivMap[systematicUniverseClass][i]   

def declareChain( tree , playlist , test = False):

  print "I'm inside declareChain()"

  chain = WrapChain( tree )  

  infile = open( '/minerva/app/users/finer/cmtuser/highNu/analysis/playlists/%s' % playlist, 'r' ).readlines()
  for it,line in enumerate(infile):
    if it%1000==0:
      print "I'm adding file #" , it , ': %s' % line 
    if test == True and it > 2: break
    chain.Add( line.rstrip('\n') )

  print "I'm returning a declared chain"

  return chain

def declareChainExplicit( tree , playlistPath ):

  print "I'm inside declareChainExplicit()"
  chain = WrapChain( tree )

  infile = open( playlistPath ).readlines()
  for it,line in enumerate(infile):
    if it%500==0:
      print "I'm adding file#" , it , ':%s' % line
    chain.Add( line.rstrip('\n') )

  print "I'm returning a declared chain"

  return chain

def copyHist( inHist ):

  tempHist = inHist.Clone( "doesThisEvenMatter?" )
  tempHist.Sumw2()

  return tempHist

def drawLowNuLines(y1,y2):

  #if not 'lines' in globals():
  #  global lines
  #  lines  = [ROOT.TLine(i,y1,i,y2) for i in [3,7,12]]

  global lines
  lines  = [ROOT.TLine(i,y1,i,y2) for i in [3,7,12]]

  for line in lines:
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()

  return

def setCurveColor( listOfCurves , playlist_object ):

  for curve in listOfCurves:

    curve.SetLineColor(playlist_object.color)
    curve.SetMarkerColor(playlist_object.color)
  
  return

