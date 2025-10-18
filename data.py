import pandas as pd
from datetime import datetime
from typing import List, Optional

class Peso:
    def __init__(self, data: str, valore: float):
        self.data = data
        self.valore = valore

class Allenamento:
    def __init__(self, data: str, sport: str, durata: int, calorie: int, battito: int, note: str = ""):
        self.data = data
        self.sport = sport
        self.durata = durata  # minuti
        self.calorie = calorie
        self.battito = battito
        self.note = note

class Nuoto(Allenamento):
    def __init__(self, data: str, durata: int, calorie: int, 
                 stile: str, vasche: int, 
                 passo_medio: float, passo_minimo: float, 
                 bracciata_media: int, bracciata_massima: int, 
                 note: str = "", battito: int = 0):
        super().__init__(data, "Nuoto", durata, calorie, battito, note)
        self.stile = stile
        self.vasche = vasche
        self.passo_medio = passo_medio
        self.passo_minimo = passo_minimo
        self.bracciata_media = bracciata_media
        self.bracciata_massima = bracciata_massima

class Corsa(Allenamento):
    def __init__(self, data: str, durata: int, calorie: int, battito: int,
                 distanza: float, passo_medio: float, dislivello: int,
                 note: str = ""):
        super().__init__(data, "Corsa", durata, calorie, battito, note)
        self.distanza = distanza
        self.passo_medio = passo_medio
        self.dislivello = dislivello

class Ciclismo(Allenamento):
    def __init__(self, data: str, durata: int, calorie: int, battito: int,
                 distanza: float, velocita_media: float, velocita_massima: float, dislivello: int,
                 note: str = ""):
        super().__init__(data, "Ciclismo", durata, calorie, battito, note)
        self.distanza = distanza
        self.velocita_media = velocita_media
        self.velocita_massima = velocita_massima
        self.dislivello = dislivello

def salva_pesi(pesi: List[Peso], filename: str = "pesi.csv"):
    df = pd.DataFrame([vars(p) for p in pesi])
    df.to_csv(filename, index=False)

def carica_pesi(filename: str = "pesi.csv") -> List[Peso]:
    try:
        df = pd.read_csv(filename)
        return [Peso(row["data"], row["valore"]) for _, row in df.iterrows()]
    except FileNotFoundError:
        return []

def salva_allenamenti(allens: List[Allenamento], filename: str = "allenamenti.csv"):
    df = pd.DataFrame([vars(a) for a in allens])
    df.to_csv(filename, index=False)

def carica_allenamenti(filename: str = "allenamenti.csv") -> List[Allenamento]:
    try:
        df = pd.read_csv(filename)
        allenamenti = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            sport = row_dict.get("sport")
            if sport == "Nuoto":
                # Gestione per retrocompatibilità
                vasche = row_dict.get("vasche", row_dict.get("vasche_sess", 0))
                
                allenamenti.append(Nuoto(
                    data=row_dict.get("data"),
                    durata=row_dict.get("durata"),
                    calorie=row_dict.get("calorie"),
                    battito=row_dict.get("battito", 0),
                    stile=row_dict.get("stile", "Stile non specificato"),
                    vasche=vasche,
                    passo_medio=row_dict.get("passo_medio", 0.0),
                    passo_minimo=row_dict.get("passo_minimo", 0.0),
                    bracciata_media=row_dict.get("bracciata_media", 0),
                    bracciata_massima=row_dict.get("bracciata_massima", row_dict.get("bracciata_minima", 0)),
                    note=row_dict.get("note", "")
                ))
            elif sport == "Corsa":
                allenamenti.append(Corsa(
                    data=row_dict.get("data"),
                    durata=row_dict.get("durata"),
                    calorie=row_dict.get("calorie"),
                    battito=row_dict.get("battito"),
                    distanza=row_dict.get("distanza", 0.0),
                    passo_medio=row_dict.get("passo_medio", 0.0),
                    dislivello=row_dict.get("dislivello", 0),
                    note=row_dict.get("note", "")
                ))
            elif sport == "Ciclismo":
                allenamenti.append(Ciclismo(
                    data=row_dict.get("data"),
                    durata=row_dict.get("durata"),
                    calorie=row_dict.get("calorie"),
                    battito=row_dict.get("battito"),
                    distanza=row_dict.get("distanza", 0.0),
                    velocita_media=row_dict.get("velocita_media", 0.0),
                    velocita_massima=row_dict.get("velocita_massima", 0.0),
                    dislivello=row_dict.get("dislivello", 0),
                    note=row_dict.get("note", "")
                ))
            elif sport: # Per gestire "Judo" e altri futuri sport generici
                allenamenti.append(Allenamento(
                    row_dict.get("data"), 
                    row_dict.get("sport"), 
                    row_dict.get("durata"), 
                    row_dict.get("calorie"), 
                    row_dict.get("battito"), 
                    row_dict.get("note", "")
                ))
        return allenamenti
    except FileNotFoundError:
        return [] 