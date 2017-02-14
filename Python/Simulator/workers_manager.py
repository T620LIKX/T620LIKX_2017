
class WorkersManager:

    def __init__(self):
        self.workers = []
        self.worker_id = 0

    def add_workers(self, settings):
        for i in range(settings.number_of_workers):
            self.create_worker(settings)

    def create_worker(self, settings):
        w = {}
        w['id'] = self.worker_id
        self.worker_id += 1

        w['idle'] = True
        w['phonecall'] = 0
        w['idletime'] = 0
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
        phonecall['answer time'] = currenttime
        self.workers[i]['phonecall'] = phonecall
        self.workers[i]['idle'] = False
        return i

    def finish_phonecall(self, worker_id):
        p = self.workers[worker_id]['phonecall']
        self.workers[worker_id]['phonecall'] = 0
        self.workers[worker_id]['idle'] = True
        return p


    def update_idletime(self, time_passed):
        for i in range(len(self.workers)):
            self.workers[i]['idletime'] += time_passed * self.workers[i]['idle']


