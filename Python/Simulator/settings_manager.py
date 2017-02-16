import numpy


class SettingsManager():
    def __init__(self):
        self.starttime = 0
        self.endtime = 300
        self.number_of_workers = 1

        self.lam = 0.1
        self.mu = 0.2
        self.rho = self.lam / self.mu

    def rand_phonecall_length(self):
        return numpy.random.exponential(1/self.mu)

    def rand_arrival_time(self):
        return numpy.random.exponential(1/self.lam)



