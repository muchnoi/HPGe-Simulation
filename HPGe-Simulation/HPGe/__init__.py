#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time
import ROOT
import Geant4 as G4
from Geant4 import mm, cm, eV, keV, MeV

global debugModule
debugModule = False

#ROOT.gROOT.GetPluginManager().AddHandler("TVirtualStreamerInfo", "*", "TStreamerInfo", "RIO", "TStreamerInfo()")

class Simulation:
  """
  class-frontend for all simulation, under the hood
  """
  def __init__(self, **options):

    if 'visualize' in options:  self.visualize = options['visualize']
    else:                       self.visualize = False

    if 'wait' in options:       self.wait = options['wait']
    else:                       self.wait = False
        
    # setup of the random number generator
    self.randEngine = G4.Ranlux64Engine()
#    te = G4.HepRandom.getTheSeeds()
    G4.HepRandom.setTheEngine(self.randEngine)

    # creation/registering of the matter interaction physics
    G4.gRunManager.SetUserInitialization(G4.G4physicslists.LBE())

    # creation/registering of the detector constructor
    import Detector
    self.setup   = Detector.Constructor()
    self.crystal = self.setup.calorimeter.logical
    self.hpge    = Detector.MySD()
    self.crystal.SetSensitiveDetector(self.hpge)
    G4.gRunManager.SetUserInitialization(self.setup)
    
    # creation/registering of the source constructor
    import Generator
    self.hist    = ROOT.TH1D("hist", "Energy deposit [keV]", 1500, 0, 3000.0)
    self.uaction = Generator.MyEventAction(self.hpge, self.hist)
    self.myPGA   = Generator.MyPrimaryGeneratorAction()
    G4.gRunManager.SetUserAction(self.myPGA)
    G4.gRunManager.SetUserAction(self.uaction)

    G4.gRunManager.Initialize()
#    G4.gVisManager.Initialize()
#    G4.gUImanager.Initialize()
    if self.visualize!=None:
      G4.gApplyUICommand("/vis/open %s 1600x1200-0+0" % self.visualize)
      G4.gApplyUICommand("/vis/scene/create")
#      G4.gApplyUICommand("/vis/viewer/set/style surface")
      G4.gApplyUICommand("/vis/viewer/set/style wireframe")
      G4.gApplyUICommand("/vis/viewer/set/viewpointThetaPhi 90. 0.")
      G4.gApplyUICommand("/vis/scene/add/volume")
      G4.gApplyUICommand("/vis/sceneHandler/attach")
      G4.gApplyUICommand("/tracking/storeTrajectory 1")
      G4.gApplyUICommand("/vis/scene/add/trajectories")
      G4.gApplyUICommand("/vis/scene/endOfEventAction accumulate")
      G4.gApplyUICommand("/vis/enable true")
    print self.visualize
          
  def run(self, number):
#    if self.visualize==None:
#    for i in range(10):
#      G4.gRunManager.BeamOn(number)
#      raw_input()
    self.hist.Draw()
    sys.stdout.write("=== Finished %d events ===\n"%number)
    sys.stdout.flush()
