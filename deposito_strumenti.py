import csv
from operator import attrgetter


class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.id_strumento}] {self.tipo} - {self.marca} ({self.anno_acquisto}) - €{self.valore:.2f}"



class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito}: Strumento {self.id_strumento} affidato all'allievo {self.cognome_allievo} in data {self.data}"





class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self._responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}

    #In Python, la riga @property
    # seguita dalla definizione di un metodo
    # trasforma quel metodo in un "getter".
    # Significa che, dal punto di vista di chi usa la classe
    # l'attributo responsabile sembra una variabile
    # ma in realtà Python sta eseguendo il codice
    # scritto dentro quel metodo

    @property
    def responsabile(self):
        return self._responsabile

    # il property controlla cosa succede quando leggi un attributo
    # mentre il setter controlla cosa succede quando cambi o assegni
    # un valore a quell'attributo

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        if nuovo_responsabile and nuovo_responsabile.strip():
            self._responsabile = nuovo_responsabile.strip()
        else:
            raise ValueError("Il nome del responsabile non può essere vuoto.")


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for riga in file:
                    parti = riga.strip().split(",")
                    if not riga:  # Salta eventuali righe vuote
                        continue
                    id_str, tipo, marca, anno_acquisto, valore = parti
                    strumento = Strumento(id_str, tipo, marca, anno_acquisto, valore)
                    self.strumenti[id_str] = strumento
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: Il file '{file_path}' non è stato trovato.")



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # 1. Calcolo il nuovo ID basato sugli strumenti già presenti

        # se il dizionario è vuoto allora:
        if not self.strumenti:
            nuovo_id = "S1"
        else:
            numeri = []
            for s_id in self.strumenti.keys():
                if s_id.startswith('S'):
                    try:
                        # Estraggo la parte numerica dopo la 'S' e la converto in intero
                        numeri.append(int(s_id[1:]))
                    except ValueError:
                        pass

            # Se ci sono numeri validi, prendo il massimo e aggiungo 1, altrimenti parto da 1
            num_succ = max(numeri) + 1 if numeri else 1
            nuovo_id = f"S{num_succ}"

        # 2. Creo l'oggetto Strumento
        strumento = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)

        # 3. Lo memorizzio nel dizionario del deposito
        self.strumenti[nuovo_id] = strumento

        return strumento


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # mi assicuro che lo strumento sia disponibile e che
        # non sia già in prestito
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: lo strumento con ID {id_strumento} non esiste nel deposito.")

        for p in self.prestiti.values():
            if p.id_strumento == id_strumento:
                raise Exception(f"Errore: lo strumento {id_strumento} risulta già in prestito.")

        #Generazione del codice univoco del prestito (P1, P2, P3...)
        num_prestito = len(self.prestiti) + 1
        id_prestito = f"P{num_prestito}"
        while id_prestito in self.prestiti:
            num_prestito += 1
            id_prestito = f"P{num_prestito}"

        prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = prestito
        return prestito




    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: nessun prestito trovato con ID {id_prestito}.")

        ## Rimuove il prestito dal dizionario
        del self.prestiti[id_prestito]
