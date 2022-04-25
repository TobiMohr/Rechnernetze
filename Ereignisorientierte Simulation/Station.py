from Ereignisliste import Ereignisliste


class Station:
    anzahl_kunden = 0
    skipped = 0
    occupied = 0

    def __init__(self, art, abarbeitungsdauer):
        self.queue = []
        self.art = art
        self.abarbeitungsdauer = abarbeitungsdauer

    def einreihen(self, kundin):
        self.queue.append(kundin)
        Ereignisliste.stationen_ausgabe.append(
            f"{Ereignisliste.simulationszeit}:{self.art} adding customer {kundin.name}{kundin.kundennummer}")

        if self.occupied == 0:  # nicht belegt
            Ereignisliste.ereignisnummer += 1
            queue_serve = (Ereignisliste.simulationszeit, 2, Ereignisliste.ereignisnummer, self.serve, kundin)
            Ereignisliste.push(queue_serve)

    def serve(self, kundin):
        Ereignisliste.stationen_ausgabe.append(
            f"{Ereignisliste.simulationszeit}:{self.art} serving customer {kundin.name}{kundin.kundennummer}")
        self.occupied = 1  # auf belegt stellen

        event = (Ereignisliste.simulationszeit + (self.abarbeitungsdauer * kundin.anzahl_waren), 2,
                 Ereignisliste.ereignisnummer, self.fertig_bedient, kundin)
        Ereignisliste.push(event)

    def fertig_bedient(self, kundin):
        if len(self.queue) > 0:
            kundin = self.queue.pop(0)
            Ereignisliste.stationen_ausgabe.append(
                f"{Ereignisliste.simulationszeit}:{self.art} finished customer {kundin.name}{kundin.kundennummer}")
            self.occupied = 0
            kundin.verlassen()

            if len(self.queue) > 0:
                customer = self.queue[0]
                self.occupied = 1
                Ereignisliste.ereignisnummer += 1
                event = (Ereignisliste.simulationszeit, 2,
                         Ereignisliste.ereignisnummer, self.serve, customer)
                Ereignisliste.push(event)
