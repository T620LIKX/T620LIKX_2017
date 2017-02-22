
class WorkersManager:

    def __init__(self):
        self.workers = []
        self.workers_schedule = []
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
        w['status'] = 'idle'  # idle, incall, inlunch, notworking, aftercall,break
        w['worktime'] = 0 # vinna lengur en x þá kaffi / mat 
        self.workers.append(w)
        # búa til kannski svolítið harðkóðað en þetta er hugmyndin
        # event.add_event('worker', 0, 'worker_start')
        # event.add_event('worker', 9500, 'worker_end')
        # event.add_event('worker', 4000, 'lunch')
        # event.add_event('worker', 2000, 'break')
        # event.add_event('worker', 7000, 'break')


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
        self.workers[i]['status'] = 'incall'
        return i

    def finish_phonecall(self, worker_id):
        p = self.workers[worker_id]['phonecall']
        self.workers[worker_id]['phonecall'] = 0
        self.workers[worker_id]['idle'] = True
        self.workers[worker_id]['status'] = 'idle'
        return p

    def update_idletime(self, time_passed): ## kannski bara hægt að breyta í uptade_status
        for i in range(len(self.workers)):
            self.workers[i]['idletime'] += time_passed * self.workers[i]['idle']