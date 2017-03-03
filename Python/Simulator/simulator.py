#!/usr/bin/env python3
import settings_manager as settingsmanager
import event_manager as em
import phonecall_manager as pm
import workers_manager as wm
import statistics_manager as sm
import output_manager as om
import pandas as pd
import matplotlib.pyplot as plt
import numpy


#numpy.random.seed(12345)

# Run simulation function
def run_simulation(settings_details = None, workers_details = None, lambdas = None, processing = None, DEBUG = False, SHOWGRAPH = False):
    events = em.EventsManager()
    phonecalls = pm.PhonecallsManager()
    workers = wm.WorkersManager()
    stats = sm.StatisticsManager()

    # settings
    s = settingsmanager.SettingsManager()

    if settings_details:
        s.setup_settings(settings_details)
    if workers_details:
        s.setup_workers(workers_details)
    if lambdas:
        s.setup_lambda(lambdas)
    if processing:
        s.setup_processing(processing)

    # initialization
    workers.add_workers(s)
    events.initialize_events(workers, s)

    # simulation loop
    currenttime = s.starttime
    lasttime = currenttime


    while currenttime < s.endtime:

        if DEBUG:
            print('\nCurrent time: {} -------------------------------------'.format(currenttime))
            print(events)
            print(phonecalls)
            print(workers)
            print('\n')

        e = events.get_next_event()
        currenttime = e['time']

        # collect statistics
        stats.update_statistics(currenttime, lasttime, e, phonecalls, workers, s)

        if SHOWGRAPH:
            stats.update_statistics_graph(currenttime, lasttime, e, phonecalls, workers, s)

        # ---------- PHONECALL ARRIVES ----------------
        # create a new phonecall, add it to the queue
        # add an event for:
        # - next phonecall arrival
        # - renegeing time of the current phonecall
        # - check
        if e['type'] == 'phonecall arrive':
            p = phonecalls.add_phonecall(e['id'], currenttime, s)
            events.add_event('phonecall arrive', currenttime + s.rand_arrival_time())
            events.add_event('phonecall renege', currenttime + p['reneging time'], object_id = p['id'])
            events.add_event('check', currenttime)


        # ------------ CHECK --------------------
        # Check if following situations are available and act if possible:
        # - a worker is overdue a break/lunch/shift end
        # - a phonecall is waiting and a worker is idle
        elif e['type'] == 'check':
            checklist = workers.check_overdue(currenttime)
            for c in checklist:
                events.add_event(c['event type'], currenttime + c['length'], object_id = c['worker id'])

            # find an idle worker and a waiting phonecall, if we get both, let the worker answer the phonecall
            while phonecalls.phonecalls_in_queue() > 0 and workers.workers_available():
                p = phonecalls.next_phonecall()
                p['answer time'] = currenttime
                worker_index = workers.answer_phonecall( p, currenttime )
                events.add_event('phonecall ends', currenttime + p['length'], object_id = worker_index)
                events.add_event('processing ends', currenttime + p['length'] + p['processing time'], object_id = worker_index)


        # ------------- PHONECALL ENDS ----------------
        # End the phonecall, the worker starts the processing
        # Don't add check since the worker is not free
        elif e['type'] == 'phonecall ends':
            p = workers.finish_phonecall( e['object id'] )
            p['end time'] = currenttime
            phonecalls.finish_phonecall(p)


        # ---------------- PROCESSINGS ENDS --------------
        # Processing ends so now the worker becomes idle
        # add a check event
        elif e['type'] == 'processing ends':
            workers.finish_processing( e['object id'])
            events.add_event('check', currenttime)


        # ---------------- PHONECALL RENEGES --------------
        # See if the phonecall is still waiting.  If so, renege the phonecall and adjust the settings for the statistics collection
        # Don't add check since nothing else happened
        elif e['type'] == 'phonecall renege':
            if phonecalls.renege(e['object id']):
                e['phonecall action'] = 'renege'


        # ----------------- START SHIFT -----------------
        # Worker is starting a shift so he/she becomes idle
        # Add a check to see if there is anything to do.
        elif e['type'] == 'shift start':
            workers.start_shift(e['object id'])
            events.add_event('check', currenttime)


        # ------------------ END SHIFT ------------------
        # if the worker is idle, stop the shift
        # otherwise add an overdue check.
        elif e['type'] == 'shift end':
            workers.end_shift(e['object id'])


        # ------------------ START BREAK ----------------
        # check if the worker is ready to start the break
        # if yes, then start break and set an event for break end
        # else, set the worker as overdue for a break.
        elif e['type'] == 'break start':
            break_length = workers.start_break(e['object id'])
            if break_length > 0:
                events.add_event('break end', currenttime + break_length, object_id = e['object id'])


        # ------------------ END BREAK ------------------
        # end the break, the worker becomes idle and we add a check
        elif e['type'] == 'break end':
            workers.end_break(e['object id'])
            events.add_event('check', currenttime)


        # ------------------ SIMULATION ENDS OR UNKNOWN -----------
        # if the simulation ends, we do nothing.  Otherwise print a warning if we don't recognize the event type
        elif not e['type'] == 'simulation ends':
            print('WARNING: Unkown event type: {}'.format(e))


        # collect statistics
        if SHOWGRAPH:
            stats.update_statistics_graph(currenttime, lasttime, e, phonecalls, workers, s)

        # update the time for next iteration
        lasttime = currenttime



    # final stats collection
    stats.calculate_statistics(phonecalls, workers, s)

    #output
    om.show_output(stats, events, workers, s)

    # Plotting commands
    if SHOWGRAPH:
        plt.plot(stats.phonecall_queue_time, stats.phonecall_queue_counter)
        plt.plot(stats.reneg_time, stats.reneg_counter,'o')
        plt.show()

if __name__ == '__main__':
    run_simulation()