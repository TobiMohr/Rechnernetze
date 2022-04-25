import heapq


class Ereignisliste:
    stationen_ausgabe = list()
    heap_queue = []
    simulationszeit = 0
    ereignisnummer = 0
    max_ereignisse = 200000000
    max_sim_time = 1800  # 30 min in s
    Kundenanzahl = 0
    vollständig_eingekauft = 0
    absolvierte_einkaufszeit = 0
    absolvierte_einkaufszeit_vollständig = 0

    @staticmethod
    def pop():
        return heapq.heappop(Ereignisliste.heap_queue)

    @staticmethod
    def push(event):
        Ereignisliste.ereignisnummer += 1  # global erhöhen
        heapq.heappush(Ereignisliste.heap_queue, event)

    @staticmethod
    def start():
        """
        takes event from eventlist and call their eventfunction
        until eventlist is empty
        :return:
        """
        while len(Ereignisliste.heap_queue) > 0:
            if Ereignisliste.ereignisnummer >= Ereignisliste.max_ereignisse:
                break
            event = Ereignisliste.pop()
            Ereignisliste.simulationszeit = event[0]
            if len(event) == 5:
                event[3](event[4])
            else:
                event[3]()



