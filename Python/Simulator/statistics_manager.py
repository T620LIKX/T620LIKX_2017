 
class StatisticsManager:
    # stats

    def __init__(self):
        self.phonecall_counter = 0
        self.finished_phonecalls = 0
        self.average_queue_length = 0
        self.max_queue_length = 0
        self.worker_idle = 0
        self.average_sojourn = 0
        self.average_wait = 0
        self.max_wait = 0
        self.phonecalls_answered = 0

    def update_statistics(self, currenttime, lasttime, events, phonecalls, workers, settings):

        workers.update_idletime(currenttime - lasttime)

        self.average_queue_length += phonecalls.length() * (currenttime - lasttime)
        self.max_queue_length = max( self.max_queue_length, phonecalls.length())

    def calculate_statistics(self, phonecalls, workers, settings):
        self.phonecall_counter = len(phonecalls.finished_phonecalls) + len(phonecalls.reneging_phonecalls)
        self.phonecalls_answered = len(phonecalls.finished_phonecalls)
        self.finished_phonecalls = phonecalls.phonecall_id
        self.reneging_phonecalls = len(phonecalls.reneging_phonecalls)
        print (self.phonecall_counter)
        print (self.reneging_phonecalls)
        for p in phonecalls.finished_phonecalls:
            self.average_sojourn += p['end time'] - p['arrival']
            self.average_wait += p['answer time'] - p['arrival']
            self.max_wait = max(self.max_wait, p['answer time'] - p['arrival'])

        if len(phonecalls.finished_phonecalls) > 0:
            self.average_sojourn = self.average_sojourn / len(phonecalls.finished_phonecalls)
            self.average_wait = self.average_wait / len(phonecalls.finished_phonecalls)


