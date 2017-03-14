
class StatisticsManager:
    # stats

    def __init__(self):
        self.info = ''
        self.phonecall_counter = 0
        self.finished_phonecalls = 0
        self.average_queue_length = 0
        self.max_queue_length = 0
        self.worker_idle = 0
        self.average_sojourn = 0
        self.average_wait = 0
        self.max_wait = 0
        self.phonecalls_answered = 0
        self.average_pqueue_length = 0
        self.max_pqueue_length = 0
        # Lists for plotting
        self.phonecall_queue_time = [0,]
        self.phonecall_queue_counter = [0,]
        self.people_counter = 0
        self.reneg_time =[]
        self.reneg_counter = []



    def update_statistics(self, currenttime, lasttime, event, phonecalls, workers, settings):

        workers.update_idletime(currenttime - lasttime)

        self.average_queue_length += phonecalls.length() * (currenttime - lasttime)
        self.max_queue_length = max( self.max_queue_length, phonecalls.length())
        self.average_pqueue_length += phonecalls.length_prio() * (currenttime - lasttime)
        self.max_pqueue_length = max(self.max_pqueue_length, phonecalls.length_prio())
    def update_statistics_graph(self, currenttime, lasttime, event, phonecalls, workers, settings):
        if not (self.phonecall_queue_time[-1] == event['time'] and self.phonecall_queue_counter[-1] == phonecalls.length()):
            self.phonecall_queue_time.append(event['time'])
            self.phonecall_queue_counter.append(phonecalls.length())

        if event['phonecall action'] == 'renege':
            self.reneg_time.append(event['time'])
            self.reneg_counter.append(phonecalls.length() + 1 )


    def calculate_statistics(self, phonecalls, workers, settings):
        self.phonecall_counter = len(phonecalls.finished_phonecalls) + len(phonecalls.reneging_phonecalls)
        self.phonecalls_answered = len(phonecalls.finished_phonecalls)
        self.finished_phonecalls = phonecalls.phonecall_id
        self.reneging_phonecalls = len(phonecalls.reneging_phonecalls)

        for p in phonecalls.finished_phonecalls:
            self.average_sojourn += p['end time'] - p['arrival']
            self.average_wait += p['answer time'] - p['arrival']
            self.max_wait = max(self.max_wait, p['answer time'] - p['arrival'])

        if len(phonecalls.finished_phonecalls) > 0:
            self.average_sojourn = self.average_sojourn / len(phonecalls.finished_phonecalls)
            self.average_wait = self.average_wait / len(phonecalls.finished_phonecalls)


