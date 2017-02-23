import data_structures as ds


class EventsManager:

    def __init__(self):
        self.events = ds.SortedQueue()
        self.finished_events = ds.Queue()
        self.event_id = 0

    def add_event(self, event_type, event_time, object_id = -1):
        e = {}
        e['id'] = self.event_id
        self.event_id += 1
        e['type'] = event_type
        e['time'] = event_time
        e['object id'] = object_id
    
        self.events.enqueue(e)

    def initialize_events(self, workers, settings):
        self.add_event('simulation ends', settings.endtime)
        self.add_event('phonecall arrive', settings.starttime + settings.rand_arrival_time())
        self.add_event('worker', 500, 'worker_start')
        self.add_event('worker', 9500, 'worker_end')
        self.add_event('worker', 4000, 'lunch')
        self.add_event('worker', 2500, 'break')
        self.add_event('worker', 6500, 'break')

    def get_next_event(self):
        if self.length() > 0:
            next_event = self.events.dequeue()
            self.finished_events.enqueue(next_event)
            return next_event

    def length(self):
        return self.events.length()

    def isempty(self):
        return isempty(self.events)