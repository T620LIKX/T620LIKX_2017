#!/usr/bin/env python3
import gettinglambdas
import worker_details
import simulator
import helperfunctions as hf
import company_a
import company_b
import numpy


days = ['mon','tue','wed','thu','fri','sat','sun']
sim_settings, lambdas, workers = company_a.initialize_company(days)

iterations = 5

results = {}

for d in days:
    results[d] = []

    for i in range(iterations):
        stats = simulator.run_simulation(settings_details = sim_settings[d].copy(), lambdas = lambdas[d].copy(), workers_details = workers[d].copy(), SHOWGRAPH=False, SHOWOUTPUT='.')
        results[d].append(stats)

print('')

# do something clever with the results...

