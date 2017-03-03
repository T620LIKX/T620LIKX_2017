import data_structures as ds

class WorkersManager:

    def __init__(self):
        self.workers = []
        self.workers_schedule = []
        self.worker_id = 0

    def add_workers(self, settings):
        for i in range(settings.number_of_workers):
            self.create_worker(settings, i)

    def create_worker(self, settings, index):
        w = {}
        w['id'] = self.worker_id
        self.worker_id += 1
        w['idle'] = False
        w['phonecall'] = 0
        w['idletime'] = 0
        w['status'] = 'notworking'  # idle, incall, notworking, processing, break
        w['check overdue'] = False   # true if the worker should have taken a break, lunch or ended shift, but is still stuck in a phonecall

        w['breaks'] = ds.SortedQueue()
        # here we can add breaks, lunch and so on.
        #w['breaks'].enqueue( {'time': 3*60*60, 'length': 30*60, 'type':'lunch'} )
        #w['breaks'].enqueue( {'time': 1*60*60, 'length': 15*60, 'type':'coffee'} )
        #w['breaks'].enqueue( {'time': 5*60*60, 'length': 15*60, 'type':'coffee'} )

        w['shift start'] = settings.starttime
        w['shift end'] = settings.endtime
        self.workers.append(w)

    def get_idle_worker_id(self):
        idleworkerindex = -1
        idleworkeridletime = -1
        for i in range(len(self.workers)):
            if self.workers[i]['idle'] and self.workers[i]['idletime'] > idleworkeridletime:
                idleworkerindex = i
                idleworkeridletime = self.workers[i]['idletime']
        return idleworkerindex

    def workers_available(self):
        for w in self.workers:
            if w['idle']:
                return True
        return False

    def answer_phonecall(self, phonecall, currenttime):
        i = self.get_idle_worker_id()
        w = self.workers[i]
        phonecall['answer time'] = currenttime
        w['phonecall'] = phonecall
        w['idle'] = False
        w['status'] = 'incall'
        return i

    # When a worker finishes a phonecall, he/she automatically starts the post processing
    def finish_phonecall(self, worker_id):
        w = self.workers[worker_id]
        p = w['phonecall']
        w['phonecall'] = 0
        w['idle'] = False
        w['status'] = 'processing'
        return p

    def finish_processing(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'

    def update_idletime(self, time_passed):
        for i in range(len(self.workers)):
            self.workers[i]['idletime'] += time_passed * self.workers[i]['idle']

    def start_shift(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'

    def end_shift(self, worker_id):
        w = self.workers[worker_id]
        if w['idle']:
            w['idle'] = False
            w['status'] = 'notworking'
            return True
        else:
            w['check overdue'] = True
            return False

    def start_break(self, worker_id):
        w = self.workers[worker_id]
        if w['idle']:
            b = w['breaks'].dequeue()
            w['idle'] = False
            w['status'] = 'break'
            return b['length']
        else:
            w['check overdue'] = True
            return -1

    def end_break(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'

    def check_overdue(self, currenttime):
        checklist = []
        for w in self.workers:
            if w['check overdue']:
                if currenttime >= w['shift end']:
                    self.end_shift(w['id'])
                elif currenttime >= w['breaks'][0]['time']:
                    breaklength = self.start_break(w['id'])
                    checklist.append({'event type':'break end', 'length': breaklength, 'worker id': w['id']})
                w['check overdue'] = False
        return checklist

    def __str__(self):
        output = 'Workers:'
        for w in self.workers:
            output = output + '\n' + str(w)
        return output



