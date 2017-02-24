import numpy


class SettingsManager():
    def __init__(self):
        self.starttime = 0
        self.endtime = 10000
        self.number_of_workers = 1

        self.lam = 0.1
        self.mu = 0.2
        self.rho = self.lam / self.mu
        self.muj_process = 0.1                             ### bætti þessu við // rebekka
        self.std_process = 0.005                           ### bætti þessu við // rebekka

    def rand_phonecall_length(self):
        return numpy.random.exponential(1/self.mu)

    def rand_arrival_time(self):
        return numpy.random.exponential(1/self.lam)
    def rand_reneg_time(self):  # á eftir að breyta
        return 5
        #return self.endtime+1
    def rand_processing_time(self):                                                 #baetti thessu vid
        return numpy.random.normal(self.muj_process, self.std_process, 1000)



