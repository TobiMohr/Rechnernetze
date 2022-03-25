import heapq

class Ereignisliste:
    heap_queue = None
    simulation_time = None
    event_number = None

    def __init__(self, simt, enr):
        self.simulation_time = simt
        self.event_number = enr

    def pop(self):
        return heapq.heappop((self.heap_queue))

    def push(self, event):
        heapq.heappush(self.heap_queue, event)

    def start(self):
        """
        takes event from eventlist and call their eventfunction
        until eventlist is empty
        :return:
        """
        return ""

