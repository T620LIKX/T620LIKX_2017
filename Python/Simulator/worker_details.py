import numpy

def check_lunch(workers_details):
    #[check lunch] true if the worker get lunch, false if worker don´t get lunch
    for w in workers_details:
        if w['shift_end'] - w['shift_start'] >= 60*60*5: # if worker works longet than 5 hour he/she got lunch
            w['check_lunch'] = True
        else:
            w['check_lunch'] = False

def lunch_time(workers_details):
   # stilla matarhlé
    for w in workers_details:
        if w['check_lunch'] == True:
            mu = (w['shift_end'] + w['shift_start'])/2 # tekur mat að metaltali þegar vaktin er hálfnuð
            sigma = 60*30 # staðalfrávik 30 mín
            timi = numpy.random.normal(mu, sigma) # hvenær hann fer í mat
            w['breaks'].append({'time': timi, 'length': 30*60, 'type':'lunch'})

def how_long_break(workers_details):
   # finna hve löng kaffi hlé starfsmaður á inni
    for w in workers_details:
        w['break_length'] = int(5*((w['shift_end'] - w['shift_start'])/60)) # fær 5 mín á hvern klukkutíma

def break_time(workers_details): # hvenær hann fer í kaffi hvort hann fari eniu sinni eða tvisvar
    for w in workers_details:
        if w['break_length'] >= 60*20: #tvær pásur ef hann á meira en 20 mín í kaffi
            mu = w['shift_start'] + 60*60*1.5 # tekur kaffi meðaltali eftir 1.5 tíma vinnu
            sigma = 60*20 # staðalfrávik 20 mín
            timi = numpy.random.normal(mu, sigma) # hvenær hann fer í fyrra kaffi
            w['breaks'].append({'time': timi, 'length': w['break_length']/2, 'type':'break'})

            mu2 = w['shift_end'] - 60*60*1.5 # tekur kaffi meðaltali eftir 1.5 tíma fyrir lok vinnu
            sigma2 = 60*20 # staðalfrávik 20 mín
            timi2 = numpy.random.normal(mu2, sigma2) # hvenær hann fer í seinna kaffi
            w['breaks'].append({'time': timi2, 'length': w['break_length']/2, 'type':'break'})

        else:# w['break_length']<=60*20 & w['break_length']>60*1:  kemst annars ekki inn
            mu = w['shift_start'] + 200 # 60*60*1.5 # tekur kaffi meðaltali eftir 1.5 tíma vinnu
            sigma = 60 # staðalfrávik 20 mín
            timi = numpy.random.normal(mu, sigma) # hvenær hann fer í kaffi
            w['breaks'].append({'time': timi, 'length': w['break_length'], 'type':'break'})


def get_workers(shift_times, rules=None):
    workers_details =[]

    for shift in shift_times:
        workers_details.append( {"shift_start": shift['starttime'],"shift_end": shift['endtime'], 'breaks':[]} )

    check_lunch(workers_details)
    lunch_time(workers_details)
    how_long_break(workers_details)
    break_time(workers_details)

    return workers_details

    # þetta virkar fryir einn starfsmann og svo þarf bara að importa þetta í simrunner og láta svo færast í settingsmanager og svo´yfir í workers managaer


