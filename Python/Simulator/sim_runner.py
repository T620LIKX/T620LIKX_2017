#!/usr/bin/env python3
import gettinglambdas
import worker_details
import simulator
import helperfunctions as hf
import company_a as thecompany
#import company_b as thecompany
import numpy


days = ['mon','tue','wed','thu','fri','sat','sun']

sim_settings, lambdas, workers = thecompany.initialize_company(days)

iterations = 5

results = {}

lambdascaling = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

phonecalls_answered_timely = {}

for scaling in lambdascaling:

    for d in days:
        results[d] = []

        # sensitivity analysis to see the effect of changing lambdas
        tmplambdas = lambdas[d].copy()
        for i in tmplambdas:
            i['lam'] = scaling * i['lam']

        phonecalls_answered_timely[d] = {'within_40': 0, 'within_60': 0, 'within_120': 0, 'within_180': 0}
        total_calls = 0

        for i in range(iterations):
            stats = simulator.run_simulation(settings_details = sim_settings[d].copy(), lambdas = tmplambdas, workers_details = workers[d].copy(), SHOWGRAPH=False, SHOWOUTPUT='.')
            results[d].append(stats)

            phonecalls_answered_timely[d]['within_40'] += stats.count_below_40_sec
            phonecalls_answered_timely[d]['within_60'] += stats.count_below_60_sec
            phonecalls_answered_timely[d]['within_120'] += stats.count_below_120_sec
            phonecalls_answered_timely[d]['within_180'] += stats.count_below_180_sec
            total_calls += stats.number_of_finished_phonecalls

        phonecalls_answered_timely[d]['within_40'] = phonecalls_answered_timely[d]['within_40'] / total_calls
        phonecalls_answered_timely[d]['within_60'] = phonecalls_answered_timely[d]['within_60'] / total_calls
        phonecalls_answered_timely[d]['within_120'] = phonecalls_answered_timely[d]['within_120'] / total_calls
        phonecalls_answered_timely[d]['within_180'] = phonecalls_answered_timely[d]['within_180'] / total_calls

    print('')

print('----------------------------------')
print('lambda, day, within40, within60, within120, within180')
for l in lambdascaling:
    for d in days:
        print('{}; {}; {}; {}; {}; {}'.format(l, d, phonecalls_answered_timely[d]['within_40'],phonecalls_answered_timely[d]['within_60'],phonecalls_answered_timely[d]['within_120'],phonecalls_answered_timely[d]['within_180']))
print('----------------------------------')

