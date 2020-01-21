#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from collections import namedtuple

from Geant4 import cm, mm, deg, keV #, cm2, cm3, mm, mm2, mm3, MeV, GeV, TeV, tesla
import Geant4 as G4

class World():
  "Whole considered space region (world)"
  def __init__(self):
    material      = G4.G4NistManager.Instance().FindOrBuildMaterial("G4_AIR")    # выбираем материал - воздух
    position      = G4.G4ThreeVector(0.0*cm, 0.0*cm, 0.0*cm)
    dimensions    = G4.G4Box("WorldBox", 6.0*cm, 6.0*cm, 20.0*cm)                # известное нам пространство (±x, ±y, ±z) 
    self.logical  = G4.G4LogicalVolume(dimensions, material, "piece")            # заполнение его материалом
    self.physical = G4.G4PVPlacement(None, position, self.logical, "World", None, False, 0)

class MetalPlate():
  "Metal Plate in front of the HPGe detector"
  def __init__(self, parent, shift_z):
    material      = G4.G4NistManager.Instance().FindOrBuildMaterial("G4_Fe")     # выбираем материал - железо
    position      = G4.G4ThreeVector(0.0*cm, 0.0*cm, 0.0*cm + shift_z)
    dimensions    = G4.G4Box("Plate", 4.0*cm, 4.0*cm, 5.0*mm)                    # размеры пластины  (±x, ±y, ±z) 
    self.logical  = G4.G4LogicalVolume(dimensions, material, "Plate")            # заполнение его материалом
    self.physical = G4.G4PVPlacement(None, position, self.logical, "Plate", parent, False, 0)
 
class Calorimeter():
  "HPGe detector"
  def __init__(self, parent, shift_z):
    nist = G4.G4NistManager.Instance()
    Vc = nist.FindOrBuildMaterial("G4_Galactic")
    Al = nist.FindOrBuildMaterial("G4_Al")
    Ge = nist.FindOrBuildMaterial("G4_Ge")
    Pg = nist.FindOrBuildMaterial("G4_PLEXIGLASS")
    Ml = nist.FindOrBuildMaterial("G4_MYLAR")
    Ai = nist.FindOrBuildMaterial("G4_AIR")
    A  = 0.5 * 51.1 *mm # Crystal Radius
    B  =       72.9 *mm # Crystal Length
    C  = 0.5 * 8.8  *mm # Hole Radius
    D  =       64.0 *mm # Hole Depth
    E  = 0.5 * 8.8  *mm # Nominal Hole End Radius
    F  =       94.  *mm # CUP Length
    G  =       3.0  *mm # Top Gap between CUP and the Shell
    H1 =       0.03 *mm # CUP Top Al Thickness
    H2 =       0.03 *mm # CUP Top Maylar Thickness
    I  =       1.0  *mm # Shell Top Thickness
    J  =       8.0  *mm # Nominal Crystal End Radius
    K  =       0.8  *mm # CUP Walls Thickness
    L  =       1.0  *mm # Shell Walls Thickness
    M  =    0.0003  *mm # Outer Dead Layer Thickness
    N  =       0.7  *mm # Inner Dead Layer Thikness
    O  =       3.0  *mm # CUP Bottom Thickness
    P  = 0.5 * 76.0 *mm # Shell Radius
    Q  =       120. *mm # Shell Length
    Z  =       0.0  *mm # zero
    s, t  = 0.0, 360.0*deg # start, turn

    # Detector Base
    base             = G4.G4Tubs("base", Z, P, 0.5*O, s,	t)
    logBase          = G4.G4LogicalVolume(base, Pg, "logBase")
    # Detector
    HPGe             = G4.G4Tubs("HPGe", Z, P, 0.5*Q,	s,	t)
    logHPGe	         = G4.G4LogicalVolume(HPGe, Vc, "logHPGe")
    # Making the Crystal shape
    crystal1         = G4.G4Tubs("cyl1",  Z, A - J, 0.5*B, s, t)
    crystal2         = G4.G4Tubs("cyl2",  Z, A, 0.5 * (B - J), s, t)
    torroid1         = G4.G4Torus("tor1", Z, J, A - J, s, t)
    xyz              = G4.G4ThreeVector(Z, Z, -0.5*J)
    crystal3         = G4.G4UnionSolid("cry3",	crystal1, crystal2, None, xyz)
    xyz              = G4.G4ThreeVector(Z, Z, 0.5*B - J)
    crystal4         = G4.G4UnionSolid("cry4",	crystal3, torroid1, None, xyz)
    # Making the Active Crystal shape
    activeCrystal1   = G4.G4Tubs("acyl1", Z, A - J, 0.5*(B - M), s, t)
    activeCrystal2   = G4.G4Tubs("acyl2", Z, A - M, 0.5*(B - J), s, t)
    activeTor1       = G4.G4Torus("activeTor1", Z, J - M , A - J, s, t)
    xyz              = G4.G4ThreeVector(Z, Z, -0.5*(J-M))
    activeCrystal3   = G4.G4UnionSolid("cry3", activeCrystal1, activeCrystal2, None, xyz)
    xyz              = G4.G4ThreeVector(Z, Z, 0.5*(B - M) - J)
    activeCrystal4   = G4.G4UnionSolid("cry4", activeCrystal3, activeTor1,     None, xyz)
    # Making the hole
    hole1            = G4.G4Tubs("hole1",	Z, C, 0.5*(D-C), s, t)
    hole2            = G4.G4Orb("hole2", C)
    xyz              = G4.G4ThreeVector(Z, Z, 0.5*(D-C))
    hole             = G4.G4UnionSolid("hole", hole1, hole2, None, xyz )
    # Making outer dead layer
    xyz              = G4.G4ThreeVector(Z, Z, Z)
    outerDeadLayer   = G4.G4SubtractionSolid("outerDeadLayer",	crystal4, activeCrystal4, None, xyz)
    # Making the inner dead layer
    innerDead1       = G4.G4Tubs("innerDead1", Z, C + N, 0.5*(D-C), s, t)
    innerDead2       = G4.G4Orb("innerDead2", C + N)
    xyz              = G4.G4ThreeVector(Z, Z, 0.5*(D-C) )
    innerDead3       = G4.G4UnionSolid("innerDead3", innerDead1, innerDead2, None, xyz)
    xyz              = G4.G4ThreeVector(Z, Z, Z)
    innerDeadLayer   = G4.G4SubtractionSolid("innerDeadLayer", innerDead3, hole, None, xyz)
    # Making final detector shape
    xyz              = G4.G4ThreeVector(Z, Z, 0.5*(D - C) - 0.5*(B - M) )
    activeCrystal    = G4.G4SubtractionSolid("activeCrystal", activeCrystal4, innerDead3, None, xyz )
    logOuterDead     = G4.G4LogicalVolume(outerDeadLayer, Ge, "logOuterDead")
    logInnerDead     = G4.G4LogicalVolume(innerDeadLayer, Ge, "logInnerDead")
    logActive = G4.G4LogicalVolume(activeCrystal,  Ge, "logActive")
    # Mylar layer
    mylarLayer       = G4.G4Tubs("mylarLayer", Z, K + A, 0.5*H2, s, t)
    logMylar         = G4.G4LogicalVolume(mylarLayer, Ml, "logMylar")
    # CUP
    CUP1             = G4.G4Tubs("CUP1", Z, K + A, 0.5*F, s, t)
    CUP2             = G4.G4Tubs("CUP2", Z, A, 0.5*(F- H1- O),	s,	t)
    xyz              = G4.G4ThreeVector(Z, Z, 0.5 *(O - H1))
    CUP              = G4.G4SubtractionSolid("CUP", CUP1, CUP2, None, xyz)
    logCUP           = G4.G4LogicalVolume(CUP, Al, "logCUP")
    #detector shell
    shell1           = G4.G4Tubs("shell1", Z, P,     0.5*Q,     s, t)
    shell2           = G4.G4Tubs("shell2", Z, P - L, 0.5*Q - L, s, t)
    xyz              = G4.G4ThreeVector(Z, Z, Z)
    shell            = G4.G4SubtractionSolid("shell", shell1, shell2, None, xyz )
    logShell         = G4.G4LogicalVolume(shell, Al, "logShell")


    # Placement of all Elements
    xyz              = G4.G4ThreeVector(Z, Z,  - (I + G + F) - 0.5*O + shift_z)
    G4.G4PVPlacement(None, xyz, logBase,      "physBase",	     parent,  False, 0)
    xyz              = G4.G4ThreeVector(Z, Z , -0.5*Q + shift_z)
    G4.G4PVPlacement(None, xyz, logHPGe,      "physHPGe",	     parent,  False, 0)
    xyz              = G4.G4ThreeVector(Z, Z,   0.5*(Q - B) - I - G - H1)
    G4.G4PVPlacement(None, xyz, logOuterDead, "physOuterDead", logHPGe, False, 0)
    xyz              = G4.G4ThreeVector(Z, Z,   0.5*(Q + D - C) - I - G - H1 - B)
    G4.G4PVPlacement(None, xyz, logInnerDead, "physInnerDead", logHPGe, False, 0)
    xyz              = G4.G4ThreeVector(Z, Z, Z)
    G4.G4PVPlacement(None, xyz, logShell,     "physShell",     logHPGe, False, 0)
    xyz              = G4.G4ThreeVector(Z, Z,   0.5*(Q + H2) - L - G)
    G4.G4PVPlacement(None, xyz,	logMylar,     "physMylar",     logHPGe, False, 0)
    xyz              = G4.G4ThreeVector(Z, Z,   0.5*(Q - F) - L - G)
    G4.G4PVPlacement(None, xyz, logCUP,       "physCUP",       logHPGe, False, 0)
    xyz              = G4.G4ThreeVector(Z, Z,   0.5*(Q - M - B) - L - G - H1)
    G4.G4PVPlacement(None, xyz, logActive,    "physActive",    logHPGe, False, 0)
    self.logical     = logActive
 
    # Detector Visualization Attributes
    BaseVA  = G4.G4VisAttributes(G4.G4Color(1.0, 1.0, 1.0, 1.0)); BaseVA.SetForceSolid( True); logBase.SetVisAttributes(      BaseVA)
    HPGeVA  = G4.G4VisAttributes(G4.G4Color(1.0, 1.0, 0.0, 0.0)); HPGeVA.SetForceSolid( True); logHPGe.SetVisAttributes(      HPGeVA)
    ShellVA = G4.G4VisAttributes(G4.G4Color(1.0, 0.5, 0.9, 0.1)); ShellVA.SetForceSolid(True); logShell.SetVisAttributes(    ShellVA)
    CupVA   = G4.G4VisAttributes(G4.G4Color(0.2, 1.0, 0.0, 0.1)); CupVA.SetForceSolid(  True); logCUP.SetVisAttributes(        CupVA)
    MylarVA = G4.G4VisAttributes(G4.G4Color(0.2, 1.0, 0.0, 0.6)); MylarVA.SetForceSolid(True); logMylar.SetVisAttributes(    MylarVA)
    OutdlVA = G4.G4VisAttributes(G4.G4Color(0.9, 1.0, 0.0, 0.1)); OutdlVA.SetForceSolid(True); logOuterDead.SetVisAttributes(OutdlVA)
    InndlVA = G4.G4VisAttributes(G4.G4Color(0.9, 1.0, 0.0, 0.1)); InndlVA.SetForceSolid(True); logInnerDead.SetVisAttributes(InndlVA)
    CrystVA = G4.G4VisAttributes(G4.G4Color(0.8, 0.2, 0.8, 0.5)); CrystVA.SetForceSolid(True); logActive.SetVisAttributes(   CrystVA)
    
    
class Constructor(G4.G4VUserDetectorConstruction):
  def __init__(self):
    G4.G4VUserDetectorConstruction.__init__(self)
    self.world       = World()
    shift_z = -50.*mm
    self.calorimeter = Calorimeter(self.world.logical, shift_z)
    shift_z = -40.*mm
    self.plate       = MetalPlate(self.world.logical, shift_z)

  def Construct(self):
    return self.world.physical

class MySD(G4.G4VSensitiveDetector):
  "My sensitive detector"
  def __init__(self):
    G4.G4VSensitiveDetector.__init__(self, "MySD")
    self.eventEnergy = 0.0
  def ProcessHits(self, step, rohist):
    energy = step.GetTotalEnergyDeposit()/keV
    self.eventEnergy += energy


