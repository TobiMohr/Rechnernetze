import datetime
import threading
import time

import Kunde
from Ergebnis import Ergebnis
from Station import Station

DEBUG = 10
SIMULATION_TIME = 3200
ENDE = 1800


def create_kunde(name, time_next, event_time):
    kundennummer = 1
    while event_time <= ENDE:
        liste = list()
        if name == "A":
            liste.append((baecker, 10 / DEBUG, 10, 10))
            liste.append((wurst, 30 / DEBUG, 10, 5))
            liste.append((kaese, 45 / DEBUG, 5, 3))
            liste.append((kasse, 60 / DEBUG, 20, 30))
        else:
            liste.append((wurst, 30 / DEBUG, 5, 2))
            liste.append((kasse, 30 / DEBUG, 20, 3))
            liste.append((baecker, 20 / DEBUG, 20, 3))
        kunde = Kunde.KundInnen(f"{name}{kundennummer}", liste)
        kunde.start()
        kundennummer += 1
        time.sleep(time_next)
        event_time += time_next * DEBUG


baecker = Station("Bäcker", 10 / DEBUG)
wurst = Station("Metzger", 30 / DEBUG)
kaese = Station("Käse", 60 / DEBUG)
kasse = Station("Kasse", 5 / DEBUG)

baecker.start()
wurst.start()
kaese.start()
kasse.start()

kunde1 = threading.Thread(target=create_kunde, args=("A", 200 / DEBUG, 0))
kunde2 = threading.Thread(target=create_kunde, args=("B", 60 / DEBUG, 1))

Ergebnis.time_start = datetime.datetime.now()
kunde1.start()
time.sleep(1 / DEBUG)
kunde2.start()

time.sleep((SIMULATION_TIME - 1) / DEBUG)
Ergebnis.time_ende = datetime.datetime.now()
dropped_bäcker = baecker.skipped / baecker.anzahlkunden * 100
dropped_wurst = wurst.skipped / wurst.anzahlkunden * 100
dropped_käse = kaese.skipped / kaese.anzahlkunden * 100
dropped_kasse = kasse.skipped / kasse.anzahlkunden * 100
baecker.stop_ev.set()
wurst.stop_ev.set()
kaese.stop_ev.set()
kasse.stop_ev.set()

simulationszeit = Ergebnis.time_ende - Ergebnis.time_start
print("ende")
print(f"Simulationsende: {simulationszeit}s")
print(f"Anzahl Kunden: {Ergebnis.kundenanzahl}")
print(f"Anzahl vollständiger Einkäufe: {Ergebnis.vollständig_eingekauft}")
mittlere_einkaufsdauer = Ergebnis.absolvierte_einkaufszeit / Ergebnis.kundenanzahl
print(f"Mittlere Einkaufsdauer: {mittlere_einkaufsdauer}")
mittlere_einkaufsdauer_vollständig = Ergebnis.absolvierte_einkaufszeit_vollständig / Ergebnis.vollständig_eingekauft
print(f"Mittlere Einkaufsdauer (vollständig): {mittlere_einkaufsdauer_vollständig}")
print("Drop percentage at Bäcker: %.2f" % dropped_bäcker)
print("Drop percentage at Metzger: %.2f" % dropped_wurst)
print("Drop percentage at Käsetheke: %.2f" % dropped_käse)
print("Drop percentage at Kasse: %.2f" % dropped_kasse)


