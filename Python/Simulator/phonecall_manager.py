import data_structures as ds

class PhonecallsManager:

    def __init__(self):
        self.phonecalls = ds.Queue()
        self.priority_calls = ds.Queue()
        self.finished_phonecalls = []
        self.phonecall_id = 0
        self.reneging_phonecalls = []
        self.processing_phonecalls = []


        # ----------- PHONECALLS CREATED ------- 
        # Phonecalls and its attributes are created 
    def add_phonecall(self, event_id, currenttime, settings):
        phonecall = {}
        phonecall['id'] = self.phonecall_id
        self.phonecall_id += 1
        phonecall['event_id'] = event_id
        phonecall['length'] = settings.rand_phonecall_length()
        phonecall['reneging time'] = settings.rand_reneg_time()
        phonecall['arrival'] = currenttime
        phonecall['time'] = currenttime
        phonecall['answer time'] = 0
        phonecall['end time'] = 0
        phonecall['processing time'] = settings.rand_processing_time()
        phonecall['priority'] = 0  # Gerum ráð fyrir að forgangurinn hefur gildið 0 fyrir venjulegt símtal eða 1. Það á eftir að búa til dreifingu fyrir þetta.
        
        if phonecall['priority'] == 0:
            self.phonecalls.enqueue(phonecall)
        else:
            self.priority_calls.enqueue(phonecall)
        return phonecall

        # ----------- NEXT PHONECALL ------- 
        # Gets the next phonecall waiting. 
    def next_phonecall(self):
        p = self.phonecalls.dequeue()
        return p

    def next_priority(self):
        p = self.priority_calls.dequeue()
        return p

    def finish_priority(self, phonecall):
        self.finished_phonecalls.append(phonecall)

    def finish_phonecall(self, phonecall):
        self.finished_phonecalls.append(phonecall)


        # ----------- PHONECALLS IN QUEUE? ------- 
        # Boolean: Checks if there are any phonecalls waiting. Returns True if length > 0, else False.
    def phonecalls_in_queue(self):
        return self.length() > 0
    
    def phonecalls_in_priority_queue(self):
        return len(self.priority_calls.items) > 0

    def length(self):
        return self.phonecalls.length()

    def length_prio(self):
        return self.priority_calls.length()

    # Allt hérna fyrir neðan er viðbót vegna reneging
    # fall sem sækir id á því símtali sem kom síðast í röðina
    def latest_id(self):
        return self.phonecalls.items[-1]['id']

    def renege(self, renege_id):
        (renege_index, p) = self.find_phonecall(renege_id)
        if renege_index != -1:
            if p==0:
                phonecall = self.phonecalls.items.pop(renege_index)
                self.reneging_phonecalls.append(phonecall)
            elif p==1:
                phonecall = self.priority_calls.items.pop(renege_index)
                self.reneging_phonecalls.append(phonecall)
            return True

        return False

    #Fall sem finnur indexinn á símtalinu sem renegar, skilar -1 ef símtalið er ekki lengur í röðinni
    def find_phonecall(self, phonecall_id):
        A = 0
        if len(self.phonecalls.items) > 0:
            for i in range(len(self.phonecalls.items)):
                if (self.phonecalls.items[i]['id'] == phonecall_id):
                    return (i,A)
        if len(self.priority_calls.itmes) >0:
            for i in range(len(self.priority_calls.itmes)):
                if (self.priority_calls[i]['id'] == phonecall_id):
                    A = 1
                    return(i,A)
        return -1

    #lengd á reneging röðini
    def length_R(self):
        return len(self.reneging_phonecalls)

    def __str__(self):
        return 'Phonecalls:'+str(self.phonecalls)
