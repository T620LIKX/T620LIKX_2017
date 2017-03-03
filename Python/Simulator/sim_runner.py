#!/usr/bin/env python3
import simulator

sim_settings = {}

sim_settings['start time'] = 0
sim_settings['end time'] = 1000 #10*60*60




simulator.run_simulation(settings_details = sim_settings, SHOWGRAPH=True)


