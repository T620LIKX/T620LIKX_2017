import numpy


class SettingsManager():
    def __init__(self):
        self.starttime = 0
        self.endtime = 10000
        self.number_of_workers = 1

        self.lam = 0.1
        self.mu = 0.2
        self.rho = self.lam / self.mu

    def rand_phonecall_length(self):
        return numpy.random.exponential(1/self.mu)

    def rand_arrival_time(self):
        return numpy.random.exponential(1/self.lam)
    def rand_reneg_time(self):  # á eftir að breyta
        return 5
        #return self.endtime+1



