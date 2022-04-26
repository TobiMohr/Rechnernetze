from threading import Thread, Lock, Event
from time import sleep, time


class Station(Thread):
    skipped = 0
    anzahlkunden = 0
    waren_kunde = 0
    name_kunde = ""

    def __init__(self, art, abarbeitungsdauer):
        Thread.__init__(self)
        self.queue = []
        self.art = art
        self.abarbeitungsdauer = abarbeitungsdauer
        self.arrEv = Event()
        self.occupied = 0
        self.lock = Lock()
        self.serv_ev = Event()
        self.stop_ev = Event()

    def run(self):
        print(f"{self.art} started")

        while True:
            self.arrEv.wait()  # warte bis ein Kunde eintrifft
            self.serve()  # bediene den Kunden

            self.lock.acquire()

            while len(self.queue) > 0:  # Queue abarabeiten
                kundIn = self.queue.pop(0)
                self.lock.release()
                kundIn.serv_ev.set()
                kundIn.serv_ev.clear()
                self.serve()
                self.lock.acquire()
            self.arrEv.clear()  # Keine Kunden mehr in Warteschlange --> bereit machen wieder zu warten
            self.lock.release()

    def serve(self):
        print(f" - {self.art} is serving {self.name_kunde}")
        sleep(self.abarbeitungsdauer * self.waren_kunde)  # schlafe solange Kunde bedient wird
        print(f"{self.art} finished to serve {self.name_kunde}")
        self.serv_ev.set()
        self.serv_ev.clear()
