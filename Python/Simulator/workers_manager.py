
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
        w['idle'] = False
        w['phonecall'] = 0
        w['idletime'] = 0
        w['status'] = 'notworking'  # idle, incall, inlunch, notworking, aftercall,break
        w['worktime'] = 0 # vinna lengur en x þá kaffi / mat 
        w['breaktime'] = 0 # pásan er bara 20 mín eða ehv 
        self.workers.append(w)
        # búa til kannski svolítið harðkóðað en þetta er hugmyndin



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

    def update_status(self,event,time_passed,id = -1):
        for i in range(len(self.workers)):
            if event == 'worker_start':
                self.workers[i]['status'] = 'idle'
                self.workers[i]['idle'] = True
                self.workers[i]['worktime'] = 0

            elif event == 'worker_end':
                self.workers[i]['status'] = 'notworking'
                self.workers[i]['idle'] = False

            elif event == 'break':
                self.workers[i]['status'] = 'break'
                self.workers[i]['idle'] = False
                self.workers[i]['worktime'] = 0

            elif event == 'break_done':
                self.workers[i]['status'] = 'idle'
                self.workers[i]['idle'] = True
                self.workers[i]['worktime'] = 0
                self.workers[i]['breaktime'] = 0
            
            elif event == 'lunch':
                self.workers[i]['status'] = 'lunch'
                self.workers[i]['idle'] = False
                self.workers[i]['worktime'] = 0
      