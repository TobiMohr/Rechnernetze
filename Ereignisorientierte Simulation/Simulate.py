from Ereignisliste import Ereignisliste
from KundIn import KundIn
from Station import Station


def main():
    # Stationen mit (art, abarbeitungszeit in s pro Ware)
    baecker = Station("Bäcker", 10)
    wurst = Station("Metzger", 30)
    kaese = Station("Käse", 60)
    kasse = Station("Kasse", 5)

    # Zwei Typen von KundInnen (Station, laufzeit, skipped_bei, anzahl_käufe)
    vollständiger_einkauf = list()
    vollständiger_einkauf.append((baecker, 10, 10, 10))
    vollständiger_einkauf.append((wurst, 30, 10, 5))
    vollständiger_einkauf.append((kaese, 45, 5, 3))
    vollständiger_einkauf.append((kasse, 60, 20, 30))

    leberkaes_semmel = list()
    leberkaes_semmel.append((wurst, 30, 5, 2))
    leberkaes_semmel.append((kasse, 30, 20, 3))
    leberkaes_semmel.append((baecker, 20, 20, 3))

    # Generiere Kundentypen mit Zeit zu nächstem eintreffen
    kunde1 = KundIn("A", vollständiger_einkauf, 200)
    kunde2 = KundIn("B", leberkaes_semmel, 60)

    # generate events
    queue_begin_k1 = (0, 1, Ereignisliste.ereignisnummer, kunde1.begin)
    Ereignisliste.Kundenanzahl += 1
    queue_begin_k2 = (1, 1, Ereignisliste.ereignisnummer, kunde2.begin)
    Ereignisliste.Kundenanzahl += 1

    # add events to heapq
    Ereignisliste.push(queue_begin_k1)
    Ereignisliste.push(queue_begin_k2)
    Ereignisliste.start()

    print()
    for output in Ereignisliste.stationen_ausgabe:
        print(output)

    print("\nSimulationsende: " + str(Ereignisliste.simulationszeit) + "s")
    print("Anzahl Kunden: " + str(Ereignisliste.Kundenanzahl))
    print("Anzahl vollständige Einkäufe: " + str(Ereignisliste.vollständig_eingekauft))

    mittlere_einkaufsdauer = Ereignisliste.absolvierte_einkaufszeit / Ereignisliste.Kundenanzahl
    print("Mittlere Einkaufsdauer: %.2fs" % mittlere_einkaufsdauer)
    mittlere_einkaufsdauer_vollständig = Ereignisliste.absolvierte_einkaufszeit_vollständig / Ereignisliste.vollständig_eingekauft
    print("Mittlere Einkaufsdauer (vollständig): %.2fs" % mittlere_einkaufsdauer_vollständig)

    dropped_backer = baecker.skipped / baecker.anzahl_kunden * 100
    dropped_wurst = wurst.skipped / wurst.anzahl_kunden * 100
    dropped_kaese = kaese.skipped / kaese.anzahl_kunden * 100
    dropped_kasse = kasse.skipped / kasse.anzahl_kunden * 100
    print("Drop percentage at Bäcker: %.2f" % dropped_backer)
    print("Drop percentage at Metzger: %.2f" % dropped_wurst)
    print("Drop percentage at Käsetheke: %.2f" % dropped_kaese)
    print("Drop percentage at Kasse: %.2f" % dropped_kasse)


if __name__ == "__main__":
    main()
