#!/usr/bin/env python3
import settings_manager as settingsmanager
import event_manager as em
import phonecall_manager as pm
import workers_manager as wm
import statistics_manager as sm
import output_manager as om
import pandas as pd
import matplotlib.pyplot as plt

#main
events = em.EventsManager()
phonecalls = pm.PhonecallsManager()
workers = wm.WorkersManager()
stats = sm.StatisticsManager()

# settings
s = settingsmanager.SettingsManager()

# initialization
workers.add_workers(s)
events.initialize_events(workers, s)

# simulation loop
currenttime = s.starttime
lasttime = currenttime

# Lists for plotting
event_time = [0]
event_counter = [0]
people_counter = 0
reneg_time =[0]
reneg_counter = [0]

while currenttime < s.endtime:
    e = events.get_next_event()
    currenttime = e['time']

    if e['type'] == 'phonecall arrive':
        people_counter += 1
        # create a new phonecall, add it to the queue
        # add an event for the next phonecall arrival
        phonecalls.add_phonecall(e['id'], currenttime, s)
        events.add_event('phonecall arrive', currenttime + s.rand_arrival_time())
        events.add_event('check', currenttime)
        events.add_event('phonecall renegs', currenttime + s.rand_reneg_time(), phonecalls.phonecall_id -1 ) # off by 1 villa sem þarf að laga 
        
        event_time.append(e['time'])
        event_counter.append(people_counter-1)
        event_time.append(e['time'])
        event_counter.append(people_counter) # appenda tölunni sem var á undan + 1
 

    elif e['type'] == 'check':
        # find an idle worker and answer a phonecall
        if phonecalls.phonecalls_in_queue() > 0 and workers.workers_available():
            p = phonecalls.next_phonecall()
            p['answer time'] = currenttime
            worker_index = workers.answer_phonecall( p, currenttime )
            events.add_event('phonecall ends', currenttime + p['length'], worker_index)

    elif e['type'] == 'phonecall ends':
        people_counter -= 1
        # end a phonecall, update the statistics
        # add a check idle event
        p = workers.finish_phonecall( e['object id'] )
        p['end time'] = currenttime
        phonecalls.finish_phonecall(p)
        events.add_event('check', currenttime)

        event_time.append(e['time'])
        event_counter.append(people_counter+1)
        event_time.append(e['time'])
        event_counter.append(people_counter)
    elif e['type'] == 'phonecall renegs':
        phonecalls.reneg(e['object id'])
        for key in phonecalls.reneging_phonecalls:
           if (key['arrival'] + key['Reneging time']) == e['time']:
            people_counter -= 1
            event_time.append(e['time'])
            event_counter.append(people_counter+1)
            event_time.append(e['time'])
            event_counter.append(people_counter)

            reneg_time.append(e['time'])
            reneg_counter.append(people_counter+1)

        

    #elif e['type'] == 'worker':
            # hérna uppfæra mat/kaffi/úrvinnsla og annað ... ? 
    #    p = 1

        
    # collect statistics
    stats.update_statistics(currenttime, lasttime, events, phonecalls, workers, s)
    lasttime = currenttime


# final stats collection
stats.calculate_statistics(phonecalls, workers, s)

#output
om.show_output(stats, events, workers, s)

# Plotting commands

plt.plot(event_time,event_counter)
plt.plot(reneg_time,reneg_counter,'o')
plt.show()