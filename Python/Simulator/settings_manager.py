import numpy

class SettingsManager():
    def __init__(self):
        # Start/end time, number of workers
        self.starttime = 0
        self.endtime = 10*60*60
        self.number_of_workers = 3
        self.workers_details = []

        # Arrival rate
        self.lam = 0.1
        self.mu = 0.2
        self.rho = self.lam / self.mu
        self.lambdas = []

        # Post processing time
        self.muj_process = 0.1
        self.std_process = 0.005

    def rand_phonecall_length(self):
        return numpy.random.exponential(1/self.mu)

    def rand_arrival_time(self, currenttime):
        current_lam = self.get_lambda(currenttime)
        return numpy.random.exponential(1/current_lam)

    def rand_reneg_time(self):  # á eftir að breyta
        #return 5
        return self.endtime+1

    def rand_processing_time(self):
        return numpy.random.normal(self.muj_process, self.std_process)

    def setup_settings(self, settings_details):
        self.starttime = settings_details['start time']
        self.endtime = settings_details['end time']

    def setup_workers(self, workers_details):
        # Assume workers_details is a list of dicts, each dict contains all info for the worker (i.e. start,end, lunch, breaks)
        self.number_of_workers = len(workers_details)
        self.workers_details = workers_details

    def setup_lambda(self, lambdas):
        # assume lambdas is a sorted list of dicts, each dict contains time and lambda value
        self.lambdas = lambdas

    def setup_processing(self, processing):
        # Do we need anything else for the processing times?
        self.muj_process = processing['mu']
        self.std_process = processing['std']

    def get_lambda(self, currenttime):
        #update self.lam if needed...
        if len(self.lambdas) > 0:
            if self.lambdas[0]['time'] <= currenttime:
                l = self.lambdas.pop(0)
                self.lam = l['lam']
        return self.lam


