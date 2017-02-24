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
        events.add_event('phonecall renegs', currenttime + s.rand_reneg_time(), phonecalls.latest_id() ) # off by 1 villa sem þarf að laga 
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
            events.add_event('processing begins', currenttime + p['length'], worker_index)                             ### bætti  við // rebekka - veit ekki alveg hvað worker_index gerir
            events.add_event('processing ends', currenttime + p['length'] + s.rand_processing_time(), worker_index)     

    elif e['type'] == 'phonecall ends':
        people_counter -= 1                              ### er þetta að láta einn starfsmann verða lausan? ef já þá má þetta ekki útaf han ner ekki laus fyrr en eftir processing phonecall
        # end a phonecall, update the statistics
        # add a check idle event
        p = workers.finish_phonecall( e['object id'] )
        p['end time'] = currenttime
        phonecalls.processing_phonecalls(p)              ### mín hugsun að þegar símtalið er búið þá byrjar starfsmaður að process-a
                                                         ### spurning hvað kemur hér á eftir
        phonecalls.finish_phonecall(p)                   ### komin hingað
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

        

    elif e['type'] == 'worker':  # event type er worker þá þarf að athuga hvað er að gerast
        workers.update_status(e['object id'],currenttime) # uppfærum status á starfsmanni
        if e['object id'] == 'break' or e['object id'] == 'lunch' : # ef hann er að fara í pásu þarf hann að byrja vinna aftur
            events.add_event('worker', currenttime+500,'break_done') # stillum hér að hann sé 500 sek í pásu
        events.add_event('check', currenttime) # þarf þetta ekki alltaf að vera ?

        
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