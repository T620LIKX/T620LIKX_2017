
class Queue:
    def __init__(self):
        self.items = []

    def isempty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if (len(self.items) > 0):
            return self.items.pop(0)

    def length(self):
        return len(self.items)

    def empty(self):
        while isempty() != True:
            dequeue()
    

    #Viðbót vegna Reneging
    def search(self, value):
        print(self.items)
        for i, dic in enumerate(self.items):
            if dic['id'] == value:
                return i
        return -1

class SortedQueue:
    def __init__(self):
        self.items = []

    def isempty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)
        self.items.sort(key = lambda x: x['time'])

    def dequeue(self):
        if (len(self.items) > 0):
            return self.items.pop(0)

    def length(self):
        return len(self.items)

    def empty(self):
        while isempty() != True:
            dequeue()
    #Viðbót vegna Reneging   
    def search(self, value):
        print(self.items)
        for i, dic in enumerate(self.items):
            if dic['id'] == value:
                return i
        return -1

