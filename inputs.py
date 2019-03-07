# import python libraries
import collections
import os
from argparse import ArgumentParser

def parserSetup():
  
  parser = ArgumentParser(description='Process optional inputs')
  parser.add_argument('--test', dest='test_bool', action='store_true', default=False)
  parser.add_argument('--tuple', dest='tuplePath', action='store')
  parser.add_argument('--outdir', dest='outDir', action='store')
  parser.add_argument('--data' , dest='dataSwitch', action='store_const', const='data')
  parser.add_argument('--mc' , dest='dataSwitch', action='store_const', const='mc')
  parser.add_argument('--truth', dest='dataSwitch', action='store_const', const='truth')
  parser.add_argument('--nogrid', dest='gridness', action='store_false')
  
  return parser.parse_args( )

def setPlaylistParam():
   
  if outArgs.playlist == None:
    PLAYLISTS = [
      "minervame1A",
      "minervame1F",
      "minervame1L"
    ]
    print "I'm setting the default playlists"
  else:
    PLAYLISTS = [
      outArgs.playlist
    ]
    print "I'm setting the user-specified playlist" 

def setup():

  print "I'm inside setup"

  outArgs = parserSetup()
  #setPlaylistParam()
 
  return outArgs

def setup_mergeTrees():
    
  print "I'm inside setup_mergeTrees()"

  parserSetup()
  setPlaylistParam()

  return PLAYLISTS 

