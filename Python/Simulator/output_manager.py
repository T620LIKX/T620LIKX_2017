def show_output(stats, events, workers, settings):
    print('Number of phonecalls: {}'.format(stats.phonecall_counter))
    print('Answered phonecalls:  {}'.format(stats.phonecalls_answered))
    print('Number of events: {}'.format(events.event_id))
    if (stats.number_of_finished_phonecalls > 0):
        print('Average sojourn: {}'.format(stats.total_sojourn/stats.number_of_finished_phonecalls))
        print('Average wait: {}'.format(stats.total_wait/stats.number_of_finished_phonecalls))
    print('Max wait: {}'.format(stats.max_wait))
    print('Average queue length: {}'.format(stats.average_queue_length / settings.endtime))
    print('Max queue length: {}'.format(stats.max_queue_length))
    print('Average priority queue lenght: {}'.format(stats.average_pqueue_length))
    print('Max priority queue length: {}'.format(stats.max_pqueue_length))

    for w in workers.workers:
        print('Worker {}, busy ratio: {}'.format(w['id'], (settings.endtime - w['idletime']) / settings.endtime ))

    print('\nVerification: ')
    if stats.number_of_finished_phonecalls > 0:
        print('Sojourn time:  {}'.format(stats.total_sojourn)/stats.number_of_finished_phonecalls)
        print("Little's law:  {}".format( 1 / (settings.mu-settings.lam)))
        print('Waiting time:  {}'.format(stats.total_wait/stats.number_of_finished_phonecalls))
        print('Expected wait: {}'.format( settings.rho / (settings.mu-settings.lam) ))
        print('Number of renegs: {}'.format (stats.reneging_phonecalls))