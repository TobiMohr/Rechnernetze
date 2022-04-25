from copy import copy, deepcopy

from Ereignisliste import Ereignisliste


class KundIn:
    kundennummer = 1
    station = None
    anzahl_waren = 0
    vollständig = 1
    beginnt = 0

    def __init__(self, name, liste, time_next):
        self.name = name
        self.liste = liste  # liste in form (station, laufzeit, skipped_bei ,anzahl_käufe)
        self.time_next = time_next

    def begin(self):
        if self.liste:
            neuer_kunde = deepcopy(self)
            neuer_kunde.liste = list()
            if self.name == "A":
                neuer_kunde.liste.append((self.liste[0][0], 10, 10, 10))
                neuer_kunde.liste.append((self.liste[1][0], 30, 10, 5))
                neuer_kunde.liste.append((self.liste[2][0], 45, 5, 3))
                neuer_kunde.liste.append((self.liste[3][0], 60, 20, 30))
            else:
                neuer_kunde.liste.append((self.liste[0][0], 30, 5, 2))
                neuer_kunde.liste.append((self.liste[1][0], 30, 20, 3))
                neuer_kunde.liste.append((self.liste[2][0], 20, 20, 3))

            neuer_kunde.kundennummer += 1
            self.beginnt = Ereignisliste.simulationszeit
            queue_ankunft = (
                Ereignisliste.simulationszeit + self.liste[0][1], 3, Ereignisliste.ereignisnummer, self.ankunft)
            Ereignisliste.push(queue_ankunft)
            if Ereignisliste.simulationszeit + self.time_next <= Ereignisliste.max_sim_time:
                Ereignisliste.Kundenanzahl += 1
                queue_beginn = (
                    Ereignisliste.simulationszeit + self.time_next, 3, Ereignisliste.ereignisnummer, neuer_kunde.begin)
                Ereignisliste.push(queue_beginn)

    def ankunft(self):
        entry = self.liste[0]
        print(str(Ereignisliste.simulationszeit) + ":" + str(self.name) + str(self.kundennummer)
              + " Queueing at " + str(entry[0].art))
        entry[0].anzahl_kunden += 1
        if len(entry[0].queue) <= entry[2]:
            self.anzahl_waren = entry[3]
            Ereignisliste.ereignisnummer += 1
            queue_einreihen = (Ereignisliste.simulationszeit, 2, Ereignisliste.ereignisnummer, entry[0].einreihen, self)
            Ereignisliste.push(queue_einreihen)
        else:
            entry[0].skipped += 1
            self.vollständig = 0
            self.liste.pop(0)
            Ereignisliste.ereignisnummer += 1
            queue_ankunft = (Ereignisliste.simulationszeit + entry[1], 3, Ereignisliste.ereignisnummer, self.ankunft)
            Ereignisliste.push(queue_ankunft)

    def verlassen(self):

        entry = self.liste.pop(0)
        station = entry[0]
        print(str(Ereignisliste.simulationszeit) + ":" + str(self.name) + str(self.kundennummer)
              + " Finished at " + str(station.art))
        if len(self.liste) == 0:
            if self.vollständig == 1:
                Ereignisliste.vollständig_eingekauft += 1
                Ereignisliste.absolvierte_einkaufszeit_vollständig += Ereignisliste.simulationszeit - self.beginnt
            Ereignisliste.absolvierte_einkaufszeit += Ereignisliste.simulationszeit - self.beginnt
            return
        laufzeit = self.liste[0][1]
        queue_ankunft = (Ereignisliste.simulationszeit + laufzeit, 3, Ereignisliste.ereignisnummer, self.ankunft)
        Ereignisliste.push(queue_ankunft)
