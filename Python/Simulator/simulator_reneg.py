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
event_time = [0]
event_counter = [0]
counter = 0

while currenttime < s.endtime:
    e = events.get_next_event()
    currenttime = e['time']
    
    if e['type'] == 'phonecall arrive':
        counter += 1
        # create a new phonecall, add it to the queue
        # add an event for the next phonecall arrival
        phonecalls.add_phonecall(e['id'], currenttime, s)
        events.add_event('phonecall arrive', currenttime + s.rand_arrival_time())
        events.add_event('check', currenttime)
        events.add_event('phonecall renegs', currenttime + s.rand_reneg_time(), phonecalls.phonecall_id)

        event_time.append(e['time'])
        event_counter.append(counter-1)
        event_time.append(e['time'])
        event_counter.append(counter) # appenda tölunni sem var á undan + 1
 

    elif e['type'] == 'check':
        # find an idle worker and answer a phonecall
        if phonecalls.phonecalls_in_queue() > 0 and workers.workers_available():
            p = phonecalls.next_phonecall()
            p['answer time'] = currenttime
            worker_index = workers.answer_phonecall( p, currenttime )
            events.add_event('phonecall ends', currenttime + p['length'], worker_index)
    
    elif e['type'] == 'phonecall ends':
        counter -= 1
        # end a phonecall, update the statistics
        # add a check idle event
        p = workers.finish_phonecall( e['object id'] )
        p['end time'] = currenttime
        phonecalls.finish_phonecall(p)
        events.add_event('check', currenttime)

        event_time.append(e['time'])
        event_counter.append(counter+1)
        event_time.append(e['time'])
        event_counter.append(counter) # appenda tölunni sem var á undan + 1
    elif e['type'] == 'phonecall renegs':
        phonecalls.reneg(e['object id'])

    # collect statistics
    stats.update_statistics(currenttime, lasttime, events, phonecalls, workers, s)
    lasttime = currenttime


# final stats collection
stats.calculate_statistics(phonecalls, workers, s)

# output
om.show_output(stats, events, workers, s)
print(phonecalls.length_R())
event_plot = pd.DataFrame([event_time,event_counter]).transpose()
event_plot.columns = ['time','counter']
#print(event_plot)
#print(event_time)

plt.plot(event_plot['time'],event_plot['counter'])
plt.show()





