import helperfunctions as hf
import worker_details
import gettinglambdas

def company_a_opening_hours():
    openinghours = {'mon':{}, 'tue':{}, 'wed':{}, 'thu':{}, 'fri':{}, 'sat':{}, 'sun':{} }

    openinghours['mon']['start time'] = '9:00'
    openinghours['mon']['end time'] =  '17:00'

    openinghours['tue']['start time'] = '9:00'
    openinghours['tue']['end time'] =  '17:00'

    openinghours['wed']['start time'] = '9:00'
    openinghours['wed']['end time'] =  '17:00'

    openinghours['thu']['start time'] = '9:00'
    openinghours['thu']['end time'] =  '17:00'

    openinghours['fri']['start time'] = '9:00'
    openinghours['fri']['end time'] =  '17:00'

    openinghours['sat']['start time'] = '12:00'
    openinghours['sat']['end time'] =  '17:00'

    openinghours['sun']['start time'] = '12:00'
    openinghours['sun']['end time'] =  '17:00'

    return openinghours

def company_a_shifts():
    shiftplan = {}

    shiftplan['mon'] = [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]

    shiftplan['tue'] = [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]

    shiftplan['wed'] = [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]
[['9:00','17:00'],
                        [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]


    shiftplan['thu'] = [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]


    shiftplan['fri'] = [['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00'],
                        ['9:00','17:00']]


    shiftplan['sat'] = [['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00']]


    shiftplan['sun'] = [['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00'],
                        ['12:00','17:00']]


    return shiftplan


def initialize_company(days):
    sim_settings = {}
    shift_times = {}
    lambdas = {}
    workers = {}

    openinghours = company_a_opening_hours()

    shiftplan = company_a_shifts()

    for d in days:
        sim_settings[d] = {}
        sim_settings[d]['start time'] = hf.strtime2sec(openinghours[d]['start time'])
        sim_settings[d]['end time'] =  hf.strtime2sec(openinghours[d]['end time'])

        lambdas[d] = gettinglambdas.CollectList('MedaltalPerHour.csv', d)

        shift_times[d] = []
        for p in shiftplan[d]:
            shift_times[d].append( {'starttime': hf.strtime2sec(p[0]), 'endtime': hf.strtime2sec(p[1]) } )

        workers[d] = worker_details.get_workers(shift_times[d])

    return sim_settings, lambdas, workers
