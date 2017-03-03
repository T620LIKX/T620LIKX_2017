#!/usr/bin/env python3
import simulator

sim_settings = {}

sim_settings['start time'] = 0
sim_settings['end time'] = 1000 #10*60*60

lambdas = []
lambdas.append( {'time': 0, 'lam': 0.1} )
lambdas.append( {'time': 400, 'lam': 0.01} )
lambdas.append( {'time': 700, 'lam': 0.1} )



simulator.run_simulation(settings_details = sim_settings, lambdas = lambdas, SHOWGRAPH=True)


