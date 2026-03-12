# ==============================================================================
# DATA MANAGER - LOGIK-MODUL
# ==============================================================================
# Dieses Modul verwaltet die Datenhaltung und Validierung.
# ==============================================================================

import os

DATEINAME = "contacts.txt"

def ist_gueltiger_text(text):
    """Prüft, ob der Text nicht leer ist."""
    return text.strip() != ""

def ist_gueltige_email(email):
    """Prüft auf ein @-Zeichen und einen Punkt in der E-Mail."""
    return "@" in email and "." in email

def laden():
    """Läd Kontakte aus der Datei (Format: Vorname|Nachname|Straße|PLZ|Email|Tel|Mobil)."""
    liste = []
    if not os.path.exists(DATEINAME):
        return liste
        
    try:
        with open(DATEINAME, "r", encoding="utf-8") as datei:
            for zeile in datei:
                teile = zeile.strip().split("|")
<<<<<<< HEAD
                # Wir unterstützen jetzt 7 Felder (Neu), 6 Felder (Alt) oder 5 Felder (Migration)
=======
                # Wir unterstützen jetzt 7 Felder (Neu), 6 Felder (Migration) oder 5 Felder (Migration)
>>>>>>> 6e752066ceb5eb8ef4c70052184269978ae721dc
                if len(teile) == 7:
                    vorname, nachname, strasse, plz, email, rufnummer, mobil = teile
                    liste.append({
                        "vorname": vorname,
                        "nachname": nachname,
                        "strasse": strasse,
                        "plz": plz,
                        "email": email,
                        "rufnummer": rufnummer,
                        "mobil": mobil
                    })
                elif len(teile) == 6:
                    vorname, nachname, strasse, plz, email, rufnummer = teile
                    liste.append({
                        "vorname": vorname,
                        "nachname": nachname,
                        "strasse": strasse,
                        "plz": plz,
                        "email": email,
                        "rufnummer": rufnummer,
<<<<<<< HEAD
                        "mobil": "" # Neues Feld initial leer
=======
                        "mobil": "" # Migration: Mobil leer
>>>>>>> 6e752066ceb5eb8ef4c70052184269978ae721dc
                    })
                elif len(teile) == 5:
                    # Migration: Voller Name war im ersten Feld
                    voller_name, strasse, plz, email, rufnummer = teile
                    namen_teile = voller_name.split(" ", 1)
                    vorname = namen_teile[0]
                    nachname = namen_teile[1] if len(namen_teile) > 1 else ""
                    liste.append({
                        "vorname": vorname,
                        "nachname": nachname,
                        "strasse": strasse,
                        "plz": plz,
                        "email": email,
                        "rufnummer": rufnummer,
                        "mobil": ""
                    })
    except Exception as e:
        print(f"Fehler beim Laden: {e}")
    return liste

def speichern(contact_liste):
    """Speichert die Liste alphabetisch sortiert nach Nachname."""
    contact_liste.sort(key=lambda e: (e["nachname"].lower(), e["vorname"].lower()))
    try:
        with open(DATEINAME, "w", encoding="utf-8") as datei:
            for e in contact_liste:
<<<<<<< HEAD
                # Sicherstellen, dass alle Felder vorhanden sind
                m = e.get("mobil", "")
                datei.write(f"{e['vorname']}|{e['nachname']}|{e['strasse']}|{e['plz']}|{e['email']}|{e['rufnummer']}|{m}\n")
=======
                datei.write(f"{e['vorname']}|{e['nachname']}|{e['strasse']}|{e['plz']}|{e['email']}|{e['rufnummer']}|{e.get('mobil', '')}\n")
>>>>>>> 6e752066ceb5eb8ef4c70052184269978ae721dc
    except IOError as e:
        print(f"Fehler beim Speichern: {e}")
