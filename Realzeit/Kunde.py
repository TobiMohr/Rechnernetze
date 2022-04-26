from threading import Thread, Event
from datetime import datetime
from time import sleep, time

from Ergebnis import Ergebnis

kundenanzahl = 0


class KundInnen(Thread):
    vollständig = 1

    def __init__(self, name, liste):
        Thread.__init__(self)
        self.name = name
        self.liste = liste
        self.serv_ev = Event()
        self.time_end = None

    def run(self):
        Ergebnis.kundenanzahl += 1

        start = datetime.now()
        while self.liste:  # arbeite Einkaufsstationen ab
            self.shop()
        ende = datetime.now()  # Zeit beim Beenden vom Einkauf
        timedelta = ende - start
        if self.vollständig == 1:  # Wenn man alle Stationen besucht hat, die man vorhatte
            Ergebnis.vollständig_eingekauft += 1
            Ergebnis.absolvierte_einkaufszeit_vollständig += timedelta.seconds

        Ergebnis.absolvierte_einkaufszeit += timedelta.seconds
        print(f"{self.name} finished shopping")

    def shop(self):
        entry = self.liste.pop(0)
        sleep(entry[1])  # entry[1] = laufzeit  ---> gehe zu Station

        station = entry[0]
        station.lock.acquire()  # kommt bei station an
        if station.arrEv.is_set():  # wenn station bereits bedient
            station.anzahlkunden += 1
            if len(station.queue) <= entry[2]:  # reiht sich ein
                print(f"{self.name} Queueing at {station.art}")
                station.queue.append(self)
                station.lock.release()
                self.serv_ev.wait()  # wartet bis er bedient wird
            else:
                station.lock.release()  # skipped die station und reiht sich nicht ein
                print(f"{self.name} skips {station.art}")
                station.skipped += 1
                self.vollständig = 0     # wird nicht jede Station besuchen die er vorhatte
                return      # arbeite nächste Supermarktstation ab
        else:
            station.anzahlkunden += 1
            station.lock.release()  # niemand an station
        station.waren_kunde = entry[3]
        station.name_kunde = self.name
        station.arrEv.set()  # lasse Station arbeiten indem man berichtet dass man ankommt
        print(f"{self.name} Served at {station.art}")
        station.serv_ev.wait()
        print(f"{self.name} Finished at {station.art}")  # fertig an Station
