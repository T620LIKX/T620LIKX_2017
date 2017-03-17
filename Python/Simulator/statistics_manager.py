
class StatisticsManager:
    # stats

    def __init__(self):
        self.info = ''
        self.phonecall_counter = 0
        self.finished_phonecalls = 0
        self.average_queue_length = 0
        self.max_queue_length = 0
        self.worker_idle = 0
        self.total_sojourn = 0
        self.total_wait = 0
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
        self.count_below_40_sec = 0
        self.count_below_60_sec = 0
        self.count_below_120_sec = 0
        self.count_below_180_sec = 0
        self.number_of_finished_phonecalls = 0


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
            self.total_sojourn += p['end time'] - p['arrival']
            self.total_wait += p['answer time'] - p['arrival']
            self.max_wait = max(self.max_wait, p['answer time'] - p['arrival'])

            if p['answer time'] - p['arrival'] < 40:
                self.count_below_40_sec += 1
            if p['answer time'] - p['arrival'] < 60:
                self.count_below_60_sec += 1
            if p['answer time'] - p['arrival'] < 120:
                self.count_below_120_sec += 1
            if p['answer time'] - p['arrival'] < 180:
                self.count_below_180_sec += 1

        self.number_of_finished_phonecalls = len(phonecalls.finished_phonecalls)




