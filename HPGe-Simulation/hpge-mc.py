#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import HPGe

if __name__ == "__main__" :
    visengine = "OGLIX"
    #visengine = "HepRepFile"
    #visengine = None
    simulation = HPGe.Simulation(visualize = visengine)
    simulation.run(10)
    simulation.hist.Draw()
    sys.stderr.write("Press ENTER...\n"); sys.stderr.flush()
    sys.stdin.readline()
    exit()
            
            
            
