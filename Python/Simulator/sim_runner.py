#!/usr/bin/env python3
import gettinglambdas
import worker_details
import simulator
import helperfunctions as hf


sim_settings = {}
sim_settings['start time'] = hf.strtime2sec('9:00') #32400
sim_settings['end time'] =  hf.strtime2sec('21:00') #75600

shift_times = [ {'starttime': hf.strtime2sec('9:00'), 'endtime': hf.strtime2sec('21:00') },
                {'starttime': hf.strtime2sec('12:00'), 'endtime': hf.strtime2sec('21:00') },
                {'starttime': hf.strtime2sec('9:00'), 'endtime': hf.strtime2sec('15:00') },
                {'starttime': hf.strtime2sec('10:00'), 'endtime': hf.strtime2sec('14:00') },
                {'starttime': hf.strtime2sec('9:00'), 'endtime': hf.strtime2sec('21:00') }]

iterations = 5

days = ['man','tri','mid','fim','fos','lau','sun']

for d in days:
    lambdas = gettinglambdas.CollectList('MedaltalPerHour.csv', d)

    workers = worker_details.get_workers(shift_times)

    for i in range(iterations):
        tmplamdas = lambdas.copy()
        stats = simulator.run_simulation(settings_details = sim_settings, lambdas = tmplamdas, workers_details = workers, SHOWGRAPH=False)



