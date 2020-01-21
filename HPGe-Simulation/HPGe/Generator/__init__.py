#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ROOT
from math import sin, cos, pi, acos
import Geant4 as G4
from Geant4 import keV, MeV

# ==================================================================
# user actions in python
# ==================================================================
class MyPrimaryGeneratorAction(G4.G4VUserPrimaryGeneratorAction):
  "My Primary Generator Action"

  def __init__(self):
    theta_min = 00.0; self.ulim = cos(theta_min * pi /180.)
    theta_max = 10.0; self.llim = cos(theta_max * pi /180.)
    G4.G4VUserPrimaryGeneratorAction.__init__(self)
    self.particleGun = G4.G4ParticleGun(1) # параметр = число генерируемых (за раз) частиц
    self.particleGun.SetParticleByName("gamma")
    self.particleGun.SetParticleEnergy(2.614*MeV)
    self.particleGun.SetParticlePosition(G4.G4ThreeVector(0.0, 0.0, 180.0))

  def GeneratePrimaries(self, event):
    phi   =      ROOT.gRandom.Uniform( 0.0, 2*pi)
    theta = acos(ROOT.gRandom.Uniform(self.llim, self.ulim))
    vx, vy, vz = sin(theta)*cos(phi), sin(theta)*sin(phi), -cos(theta)
    self.particleGun.SetParticleMomentumDirection(G4.G4ThreeVector(vx, vy, vz))
    self.particleGun.GeneratePrimaryVertex(event)

# ------------------------------------------------------------------
class MyEventAction(G4.G4UserEventAction):
  def __init__(self, sd, hist):
    G4.G4UserEventAction.__init__(self)
    self.sd = sd
    self.hist = hist
    self.count = 0
  def BeginOfEventAction(self, event):
    self.count += 1
#    print "==== start of event ", self.count
    self.sd.eventEnergy = 0
  def EndOfEventAction(self, event):
    if self.sd.eventEnergy > 10.0*keV:
      self.hist.Fill(self.sd.eventEnergy)
#    print "==== end of event ", self.count, ", energy=", self.sd.eventEnergy
    

"""
# ------------------------------------------------------------------
class MyRunAction(G4.G4UserRunAction):
  "My Run Action"

  def BeginOfRunAction(self, run):
    print "*** #event to be processed (BRA)=",
    run.GetNumberOfEventToBeProcessed()

  def EndOfRunAction(self, run):
    print "*** run end run(ERA)=", run.GetRunID()

# ------------------------------------------------------------------
class MySteppingAction(G4.G4UserSteppingAction):
  "My Stepping Action"

  def UserSteppingAction(self, step):
    print "*** dE/dx in current step=", step.GetTotalEnergyDeposit()
    track= step.GetTrack()
    touchable= track.GetTouchable()
    pv= touchable.GetVolume()
    #print pv.GetCopyNo()
    #print touchable.GetReplicaNumber(0)
"""


