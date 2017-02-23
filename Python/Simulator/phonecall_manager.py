import data_structures as ds

class PhonecallsManager:

    def __init__(self):
        self.phonecalls = ds.Queue()
        self.finished_phonecalls = []
        self.phonecall_id = 0
        self.reneging_phonecalls = []
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
            
    #Allt hérna fyrir neðan er viðbót vegna reneging 
    #fall sem sækir id á því símtali sem kom síðast í röðina
    def latest_id(self):
        return self.phonecalls.items[-1]['id']

    def reneg(self,value):
        i=self.search(value)
        if i != -1:
            self.leave_queue(i)

    #FAll sem finnur indexinn á símtalinu sem renegar, skilar -1 ef símtalið er ekki lengur í röðinni
    def search(self, value):    
        if len(self.phonecalls.items) >0:
            for i in range(0, len(self.phonecalls.items)):
                if (self.phonecalls.items[i]['id'] == value):
                    return i
        return -1
    #fjarlægjum stak með indexin num og setjum í reneging_phonecalls listan
    def leave_queue(self,num):
        phonecall = self.phonecalls.items.pop(num)
        self.reneging_phonecalls.append(phonecall)
    #lengd á 
    def length_R(self):
        return len(self.reneging_phonecalls)
        