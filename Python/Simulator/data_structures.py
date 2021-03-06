
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

    def __getitem__(self,index):
        return self.items[index]

    def __str__(self):
        output = ''
        for i in self.items:
            output = output + '\n' + str(i)
        return output


# \/\/\/ ~~~~~!! ------Comment needed ------ !!~~~~~ \/\/\/
class SortedQueue:
    def __init__(self):
        self.items = []

    def isempty(self):
        return self.items == []

    def enqueue(self, item):
        index = 0
        while index < len(self.items) and self.items[index]['time'] < item['time']:
            index += 1

        self.items.insert(index, item)

#        self.items.append(item)
#        self.items.sort(key = lambda x: x['time'])

    def dequeue(self):
        if (len(self.items) > 0):
            return self.items.pop(0)

    def length(self):
        return len(self.items)

    def empty(self):
        while isempty() != True:
            dequeue()

    def __getitem__(self,index):
        return self.items[index]

    def __str__(self):
        output = ''
        for i in self.items:
            output = output + '\n' + str(i)
        return output

