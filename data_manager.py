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
    """Lädt Kontakte aus der Datei (Format: Vorname|Nachname|Straße|PLZ|Email|Tel|Mobil)."""
    liste = []
    if not os.path.exists(DATEINAME):
        return liste
        
    try:
        with open(DATEINAME, "r", encoding="utf-8") as datei:
            for zeile in datei:
                teile = zeile.strip().split("|")
                # Wir unterstützen 7 Felder (Neu), 6 Felder (Alt) oder 5 Felder (Migration)
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
                        "mobil": ""  # Migration: Mobil-Feld initial leer
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
                # Sicherstellen, dass das Mobil-Feld existiert, bevor geschrieben wird
                mobil = e.get("mobil", "")
                datei.write(f"{e['vorname']}|{e['nachname']}|{e['strasse']}|{e['plz']}|{e['email']}|{e['rufnummer']}|{mobil}\n")
    except IOError as e:
        print(f"Fehler beim Speichern: {e}")