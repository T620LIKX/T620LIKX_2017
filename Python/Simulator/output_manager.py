def show_output(stats, events, workers, settings):
    print('Number of phonecalls: {}'.format(stats.phonecall_counter))
    print('Answered phonecalls:  {}'.format(stats.phonecalls_answered))
    print('Number of events: {}'.format(events.event_id))
    print('Average sojourn: {}'.format(stats.average_sojourn))
    print('Average wait: {}'.format(stats.average_wait))
    print('Max wait: {}'.format(stats.max_wait))
    print('Average queue length: {}'.format(stats.average_queue_length / settings.endtime))
    print('Max queue length: {}'.format(stats.max_queue_length))
    for w in workers.workers:
        print('Worker {}, busy ratio: {}'.format(w['id'], (settings.endtime - w['idletime']) / settings.endtime ))

    print('\nVerification: ')
    print('Sojourn time:  {}'.format(stats.average_sojourn))
    print("Little's law:  {}".format( 1 / (settings.mu-settings.lam)))
    print('Waiting time:  {}'.format(stats.average_wait))
    print('Expected wait: {}'.format( settings.rho / (settings.mu-settings.lam) ))
    print('Number of renegs: {}'.format (stats.reneging_phonecalls))