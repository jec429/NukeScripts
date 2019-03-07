import ROOT,os

class makeEnv_TCanvas(object):

  def __init__(self,plotName,logy=False):
    self.plotName = plotName
    self.logy = logy

  def __enter__(self):
    self.canvas = ROOT.TCanvas( "canvas" , "canvas" , 10 , 10 , 1000, 750 )
    if self.logy: self.canvas.SetLogy(0)
    return self

  def __exit__(self,*exc):
    # If directory for plotName doesn't exist yet, make it
    plotNameComponents = self.plotName.split('/')
    plotDir = '/'.join(plotNameComponents[:-1]) 
    if not os.path.isdir(plotDir):
      print "Making plot directory {0}".format(plotDir)
      os.system( "mkdir %s" % plotDir )
    self.canvas.Print(self.plotName)
    del self.canvas

class makeEnv_TCanvas_nuMigrationMatrix(makeEnv_TCanvas):

  def __init__(self,plotName,nu,bigBins):
    makeEnv_TCanvas.__init__(self,plotName)
    self.nu = nu
    self.bigBins = bigBins

  def __exit__(self,*exc):
   
    scale = 10 if not self.bigBins else 1
    horizontalLine = ROOT.TLine(0.0,self.nu*scale,5.0*scale,self.nu*scale)
    horizontalLine.SetLineColor(ROOT.kRed)
    horizontalLine.Draw()
    verticalLine = ROOT.TLine(self.nu*scale,0.0,self.nu*scale,5.0*scale)
    verticalLine.SetLineColor(ROOT.kRed)
    verticalLine.Draw()

    makeEnv_TCanvas.__exit__(self,*exc)

def setPlotSpecs_nuMigrationMatrix(MM):
  MM.GetXaxis().SetTitle("Reco #nu")
  MM.GetYaxis().SetTitle("True #nu")

def setPlotSpecs_ENu(hist):
  hist.GetXaxis().SetTitle('E_{#nu}(GeV)')
  #hist.GetXaxis().SetRangeUser(0,22)

def setPlotSpecs_Mupt(hist):
  hist.GetXaxis().SetTitle('Muon p_{T} (MeV)')
  #hist.GetXaxis().SetRangeUser(0,22)

def setPlotSpecs_Mupz(hist):
  hist.GetXaxis().SetTitle('Muon p_{Z} (MeV)')
  #hist.GetXaxis().SetRangeUser(0,22)

def setPlotSpecs_eff(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('Efficiency, #eta')

def setPlotSpecs_effNumerator(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#Reco MC Events (#eta Numerator)')

def setPlotSpecs_effDenominator(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#True MC Events (#eta Denominator)')

def setPlotSpecs_dataRate(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#Reco Data Events')

def setPlotSpecs_flux(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#nu\'s/m^{2}/GeV')

def setPlotSpecs_xSection(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#sigma (10^{-38}cm^{2})')

def setPlotSpecs_2D(hist,hor='ENu'):
  if hor == 'ENu': setPlotSpecs_ENu(hist)
  if hor == 'Mupt': setPlotSpecs_Mupt(hist)
  if hor == 'Mupz': setPlotSpecs_Mupz(hist)
  hist.GetYaxis().SetTitle('#nu (GeV)')
  global line
  line = ROOT.TLine(3,0,3,5)
  line.SetLineStyle(2)
  line.SetLineWidth(2)
  line.Draw()
  
  return


