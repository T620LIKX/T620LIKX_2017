
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
        w['status'] = 'idle'  # idle, incall, inlunch, notworking
        self.workers.append(w)
        self.create_worker(settings,worker_id) # búa til vaktaplan fyrir starfsmann, á kannski bara að vera w['id'] ??

        # eyjó var að tala um að hafa þetta í event _manager
    def create_worker_schedule(self, settings,worker_id): # núna bara harðkoðað annars hægt að lesa inn eða ehv
        ws = {}
        ws['id'] = self.workers[worker_id] # spurning um að kalla á öðruvísi
        ws['workstarts'] = 0
        ws['workend'] = 1000
        self.workers_schedule.append(ws)

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
            if w['idle']==True: # bætti við ==True þarf þess ekki ??
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
        self.workers[i]['status'] = 'idle'
        return p


    def update_idletime(self, time_passed): ## kannski bara hægt að breyta í uptade_status
        for i in range(len(self.workers)):
            self.workers[i]['idletime'] += time_passed * self.workers[i]['idle']
        self.update_worker_status(time_passed) # setti hér má kannski vera annarstaðar

'''þetta á eftir að útfæra passar kannski betur annarstaðar, væri hgæt að athuga með pásur og annað hér '''
    def update_worker_status(self, time_passed,):
        for i in range(len(self.workers)):
            if time_passed>=self.workers_schedule[i]['shift_end'] or time_passed <=self.workers_schedule[i]['shift_start'] and self.workers[i]['idle'] ==True
                self.workers[i]['status'] = 'notworking'


