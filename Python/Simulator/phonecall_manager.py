import data_structures as ds

class PhonecallsManager:

    def __init__(self):
        self.phonecalls = ds.Queue()
        self.finished_phonecalls = []
        self.phonecall_id = 0

    def add_phonecall(self, event_id, currenttime, settings):
        phonecall = {}
        phonecall['id'] = self.phonecall_id
        self.phonecall_id += 1
        phonecall['event_id'] = event_id

        phonecall['length'] = settings.rand_phonecall_length()
        phonecall['Reneging time'] = settings.rand_reneg_time()   # á eftir að útfæra nánar en dugar í bili.
        phonecall['arrival'] = currenttime
        phonecall['time'] = currenttime
        phonecall['answer time'] = 0
        phonecall['end time'] = 0

        self.phonecalls.enqueue(phonecall)

    def next_phonecall(self):
        p = self.phonecalls.dequeue()
        return p

    def finish_phonecall(self, phonecall):
        self.finished_phonecalls.append(phonecall)

    def phonecalls_in_queue(self):
        return self.length() > 0

    def length(self):
        return self.phonecalls.length()
            
    #Viðbót vegna Reneging
    def search(self, value):
        for p in self.phonecalls.items:    
            if p['id']== value:
                print(p)
        
        for i, dic in enumerate(self.phonecalls.items):
            if dic.get('id') == value:
                return i
        return -1
    
    #Viðbót vegna Reneging
    def leave_queue(self,num):
        return self.phonecalls.items.pop(num)

