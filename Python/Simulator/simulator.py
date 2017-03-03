#!/usr/bin/env python3
import settings_manager as settingsmanager
import event_manager as em
import phonecall_manager as pm
import workers_manager as wm
import statistics_manager as sm
import output_manager as om


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
currenttime = s.starttime()
lasttime = currenttime

while currenttime < s.endtime:
    e = events.get_next_event()
    currenttime = e['time']

    if e['type'] == 'phonecall arrive':
        # create a new phonecall, add it to the queue
        # add an event for the next phonecall arrival
        phonecalls.add_phonecall(e['id'], currenttime, s)
        events.add_event('phonecall arrive', currenttime + s.rand_arrival_time(currenttime))
        events.add_event('check', currenttime)

    elif e['type'] == 'check':
        # find an idle worker and answer a phonecall
        if phonecalls.phonecalls_in_queue() > 0 and workers.workers_available():
            p = phonecalls.next_phonecall()
            p['answer time'] = currenttime
            worker_index = workers.answer_phonecall( p, currenttime )
            events.add_event('phonecall ends', currenttime + p['length'], worker_index)

    elif e['type'] == 'phonecall ends':
        # end a phonecall, update the statistics
        # add a check idle event
        p = workers.finish_phonecall( e['object id'] )
        p['end time'] = currenttime
        phonecalls.finish_phonecall(p)
        events.add_event('check', currenttime)


    # collect statistics
    stats.update_statistics(currenttime, lasttime, events, phonecalls, workers, s)
    lasttime = currenttime



# final stats collection
stats.calculate_statistics(phonecalls, workers, s)


# output
om.show_output(stats, events, workers, s)


