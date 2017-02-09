import simpy
import random


def source(env, number,counter,Wait,Servicetime):
    for i in range(number):
        c = call(env, 'Call%02d' %i, counter,Wait,Servicetime)
        env.process(c)
        t = random.expovariate(1/4)
        yield env.timeout(t)



def call(env, name, counter, Qtime,Servicetime):

    arrive=env.now
    print('%7.4f %s: Call arrives' % (arrive, name))
    
    with counter.request() as req:


        resaults = yield req    
        
        wait=env.now - arrive
        Qtime.append(wait)

        

        print('%7.4f %s: Waits %6.3f' % (env.now, name, wait))
            
        Time = random.expovariate(0.5)
        Servicetime.append(Time)
        yield env.timeout(Time)
        print('%7.4f %s: Finished' % (env.now, name))

num_calls=100;

Wait=[]
Servicetime=[]
print('basic call center')
env = simpy.Environment()
random.seed(30)
counter = simpy.Resource(env, capacity=1)
env.process(source(env,num_calls,counter,Wait,Servicetime))
env.run()

print(sum(Wait)/100)
print(sum(Servicetime)/100)