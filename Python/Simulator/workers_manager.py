import data_structures as ds

class WorkersManager:

    def __init__(self):
        self.workers = []
        self.workers_schedule = []
        self.worker_id = 0

        # ----------- ADD WORKER -------
        # Function loops through the number of workers and creates as many 
        # workers as needed, by calling create_worker.
    def add_workers(self, settings):
        for i in range(settings.number_of_workers):
            self.create_worker(settings, i)

        # ----------- CREATE  -------
        # Creates one worker and initializes its attributes. 
    def create_worker(self, settings, index):
        w = {}
        w['id'] = self.worker_id
        self.worker_id += 1
        w['idle'] = False
        w['phonecall'] = 0
        w['idletime'] = 0
        w['status'] = 'notworking'  # idle, incall, notworking, processing, break
        w['check overdue'] = False   # true if the worker should have taken a break, lunch or ended shift, but is still stuck in a phonecall

        # Comment needed for clarity!
        # w['breaks'] is  a column that uses the class SortedQueue() to create a queued list for breaks. 
        w['breaks'] = ds.SortedQueue() #
        # here we can add breaks, lunch and so on.
        #w['breaks'].enqueue( {'time': 3*60*60, 'length': 30*60, 'type':'lunch'} )
        #w['breaks'].enqueue( {'time': 1*60*60, 'length': 15*60, 'type':'coffee'} )
        #w['breaks'].enqueue( {'time': 5*60*60, 'length': 15*60, 'type':'coffee'} )

        w['shift start'] = settings.starttime 
        w['shift end'] = settings.endtime
        self.workers.append(w) 


        # ----------- GET IDLE WORKER  -------
        # Function returns the worker that has been idle for the longest time. Loops through all of the workers to find the max idle time.
        # This is not the time idle since last phonecall! We want to return the worker who has been idle for the longest time in total.
    def get_idle_worker_id(self):
        idleworkerindex = -1
        idleworkeridletime = -1
        for i in range(len(self.workers)):
            if self.workers[i]['idle'] and self.workers[i]['idletime'] > idleworkeridletime:
                idleworkerindex = i
                idleworkeridletime = self.workers[i]['idletime']
        return idleworkerindex

        # ----------- WORKERS AVAILABLE?  -------
        # Checks if there are _any_ available workers. Returns boolean.
        # Used to check if a phonecall can be answered or if it should be queued / stay in queue.
    def workers_available(self):
        for w in self.workers:
            if w['idle']:
                return True
        return False


        # ----------- ANSWER PHONECALL  -------
        # Worker stops being idle and its status is updated.
        # Updates the answertime of the phonecall and returns the id of the worker who answers (through get_idle_worker_id())
    def answer_phonecall(self, phonecall, currenttime):
        i = self.get_idle_worker_id()
        w = self.workers[i]
        phonecall['answer time'] = currenttime
        w['phonecall'] = phonecall
        w['idle'] = False
        w['status'] = 'incall'
        return i


        # ----------- FINISH PHONECALL  -------
        # When a worker finishes a phonecall, he/she automatically starts the post processing.
        # The phonecall is returned (not just the ID!) and from simulator.py it is sent to a list of finished phonecalls.
    def finish_phonecall(self, worker_id):
        w = self.workers[worker_id]
        p = w['phonecall']
        w['phonecall'] = 0
        w['idle'] = False
        w['status'] = 'processing'
        return p


        # ----------- FINISH PROCESSING  -------
        # When a worker finishes processing, its attributes are updated. 
    def finish_processing(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'


        # ----------- UPDATE WORKERS TOTAL IDLETIME  -------
        # Used to collect statistics (used by statistics manager)
        # This function is called at every event. Time passed is the time between events.
        # workers['idle'] is a binary function so if a worker has not been idle, its value is 0 (ergo the stats don't change)
    def update_idletime(self, time_passed):
        for i in range(len(self.workers)):
            self.workers[i]['idletime'] += time_passed * self.workers[i]['idle']


        # ----------- WORKER STARTS SHIFT -------      
        # If the event is "shift starts". Worker is now ready to work.      
    def start_shift(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'

        # ----------- WORKER ENDS SHIFT -------   
        # End the workers shift. If still in phonecall, make check overdue: True
    def end_shift(self, worker_id):
        w = self.workers[worker_id]
        if w['idle']:
            w['idle'] = False
            w['status'] = 'notworking'
            return True
        else:
            w['check overdue'] = True
            return False

        # ----------- WORKER STARTS BREAK -------  
        # Returns the length of the break and updates the workers attributes. 
        # If the worker is not idle, its going to check overdue (and returns an error)
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

        # ----------- WORKER STARTS BREAK -------  
        # Workers break ends. Worker returns to idle.
    def end_break(self, worker_id):
        w = self.workers[worker_id]
        w['idle'] = True
        w['status'] = 'idle'

        # ----------- WORKER STARTS BREAK ------- 
        # >>>>>>>>>>>>>> Comments needed <<<<<<<<<<<<<<<<<
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



