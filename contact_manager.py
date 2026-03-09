# ==============================================================================
# CONTACT MANAGER - VERWALTUNGSSYSTEM (ERWEITERT)
# ==============================================================================
# Dieses Programm ermöglicht das Verwalten einer Kontaktliste.
# Gespeichert werden: Name, Straße, PLZ, E-Mail und Rufnummer.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. KONFIGURATION & GLOBALE VARIABLEN
# ------------------------------------------------------------------------------

# Der Sicherheitscode wird für sensible Aktionen wie "Alle löschen" benötigt.
SICHERHEITSCODE = "1234"

# Name der Textdatei, in der die Kontakte gespeichert werden.
DATEINAME = "contacts.txt"

# Die zentrale Liste für alle Kontakt-Objekte (Dictionaries).
contact_liste = []


# ------------------------------------------------------------------------------
# 2. VALIDIERUNGS-LOGIK (HELFER)
# ------------------------------------------------------------------------------

def ist_gueltiger_name(name):
    """Prüft, ob der Name nur Buchstaben, Leerzeichen und Bindestriche enthält."""
    return all(z.isalpha() or z in " -" for z in name) and name.strip() != ""


def ist_gueltige_strasse(strasse):
    """Stellt sicher, dass die Straße nicht leer ist."""
    return strasse.strip() != ""


def ist_gueltige_plz(plz):
    """Einfache Prüfung, ob die PLZ nicht leer ist."""
    return plz.strip() != ""


def ist_gueltige_email(email):
    """Prüft auf ein @-Zeichen und einen Punkt in der E-Mail."""
    return "@" in email and "." in email


def ist_gueltige_rufnummer(rufnummer):
    """Prüft, ob die Rufnummer nicht leer ist."""
    return rufnummer.strip() != ""


def rufnummer_existiert(rufnummer):
    """Prüft, ob eine Rufnummer bereits in der Liste vorhanden ist."""
    return any(eintrag["rufnummer"] == rufnummer for eintrag in contact_liste)


# ------------------------------------------------------------------------------
# 3. PERSISTENZ (SPEICHERN & LADEN)
# ------------------------------------------------------------------------------

def speichern():
    """Schreibt alle Kontakte in die Datei contacts.txt (Format: Name|Straße|PLZ|Email|Tel)."""
    try:
        with open(DATEINAME, "w", encoding="utf-8") as datei:
            for e in contact_liste:
                datei.write(f"{e['name']}|{e['strasse']}|{e['plz']}|{e['email']}|{e['rufnummer']}\n")
    except IOError as e:
        print(f"Fehler beim Speichern der Daten: {e}")


def laden():
    """Liest die Kontakte aus der Datei ein und befüllt die contact_liste."""
    try:
        with open(DATEINAME, "r", encoding="utf-8") as datei:
            for zeile in datei:
                teile = zeile.strip().split("|")
                # Wir erwarten jetzt 5 Felder (Name, Strasse, PLZ, Email, Tef)
                if len(teile) == 5:
                    name, strasse, plz, email, rufnummer = teile
                    contact_liste.append({
                        "name": name, 
                        "strasse": strasse, 
                        "plz": plz,
                        "email": email, 
                        "rufnummer": rufnummer
                    })
    except FileNotFoundError:
        # Erster Start: Datei existiert noch nicht.
        pass
    except Exception as e:
        print(f"Unerwarteter Fehler beim Laden: {e}")


# ------------------------------------------------------------------------------
# 4. DATEN-MANAGEMENT
# ------------------------------------------------------------------------------

def aktualisieren():
    """Sortiert die Liste alphabetisch nach Namen und speichert sie."""
    contact_liste.sort(key=lambda e: e["name"])
    speichern()


# ------------------------------------------------------------------------------
# 5. BENUTZEROBERFLÄCHE (ANZEIGE & MENÜS)
# ------------------------------------------------------------------------------

def menue_anzeigen():
    """Gibt das Hauptmenü auf der Konsole aus."""
    print("\n" + "="*35)
    print("        CONTACT MANAGER ")
    print("="*35)
    print("1 - Kontakte anzeigen (Tabelle)")
    print("2 - Kontakt hinzufügen")
    print("3 - Kontakt ändern")
    print("4 - Kontakt löschen")
    print("5 - ALLE Daten löschen")
    print("6 - Beenden")
    print("-" * 35)


def contacts_anzeigen():
    """Stellt alle Kontakte in einer übersichtlichen Tabelle dar."""
    if not contact_liste:
        print("\n[!] Die Kontaktliste ist aktuell leer.")
        return

    print("\nÜbersicht aller Kontakte (Strukturierte Liste):")
    # Header-Definition für die Spaltenbreiten
    header = f"{'Nr.':<4} | {'Name':<20} | {'Straße':<20} | {'PLZ':<6} | {'E-Mail':<20} | {'Telefon':<15}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    for index, e in enumerate(contact_liste, start=1):
        print(f"{index:<4} | {e['name']:<20} | {e['strasse']:<20} | {e['plz']:<6} | {e['email']:<20} | {e['rufnummer']:<15}")
    print("-" * len(header))


# ------------------------------------------------------------------------------
# 6. KERN-FUNKTIONEN (AKTIONEN)
# ------------------------------------------------------------------------------

def contact_hinzufuegen():
    """Interaktive Eingabe für einen neuen Kontakt."""
    print("\n--- Neuen Kontakt erstellen ---")
    vorname = input("Vorname: ").strip()
    nachname = input("Nachname: ").strip()
    voller_name = f"{vorname} {nachname}"
    
    if not ist_gueltiger_name(voller_name):
        print("[Fehler] Der Name ist ungültig oder leer.")
        return

    strasse = input("Straße & Hausnummer: ").strip()
    if not ist_gueltige_strasse(strasse):
        print("[Fehler] Die Straße darf nicht leer sein.")
        return

    plz = input("Postleitzahl (PLZ): ").strip()
    if not ist_gueltige_plz(plz):
        print("[Fehler] Die PLZ darf nicht leer sein.")
        return

    email = input("E-Mail Adresse: ").strip()
    if not ist_gueltige_email(email):
        print("[Fehler] Ungültiges E-Mail Format.")
        return

    rufnummer = input("Telefonnummer: ").strip()
    if not ist_gueltige_rufnummer(rufnummer):
        print("[Fehler] Rufnummer darf nicht leer sein.")
        return
    
    if rufnummer_existiert(rufnummer):
        print("[Fehler] Diese Telefonnummer ist bereits registriert.")
        return

    # Hinzufügen zum Datenbestand
    contact_liste.append({
        "name": voller_name, 
        "strasse": strasse, 
        "plz": plz,
        "email": email, 
        "rufnummer": rufnummer
    })
    aktualisieren()
    print(f"\n[OK] Kontakt '{voller_name}' wurde erfolgreich gespeichert.")


def contact_aendern():
    """Sucht einen Kontakt und erlaubt das selektive Ändern von Feldern."""
    suche = input("\nWelchen Kontakt möchtest du ändern? (Vollständiger Name): ").strip()
    e = next((c for c in contact_liste if c["name"].lower() == suche.lower()), None)
    
    if not e:
        print("[!] Kontakt wurde nicht gefunden.")
        return

    print("\n--- Bearbeitungsmodus (ENTER zum Überspringen) ---")
    
    # Name ändern
    neuer_name = input(f"Neuer Name [aktuell: {e['name']}]: ").strip()
    if neuer_name and ist_gueltiger_name(neuer_name):
        e["name"] = neuer_name

    # Straße ändern
    neue_str = input(f"Neue Straße [aktuell: {e['strasse']}]: ").strip()
    if neue_str:
        e["strasse"] = neue_str

    # PLZ ändern
    neue_plz = input(f"Neue PLZ [aktuell: {e['plz']}]: ").strip()
    if neue_plz:
        e["plz"] = neue_plz

    # E-Mail ändern
    neue_mail = input(f"Neue E-Mail [aktuell: {e['email']}]: ").strip()
    if neue_mail and ist_gueltige_email(neue_mail):
        e["email"] = neue_mail

    # Rufnummer ändern
    neue_num = input(f"Neue Nummer [aktuell: {e['rufnummer']}]: ").strip()
    if neue_num and ist_gueltige_rufnummer(neue_num):
        if neue_num != e["rufnummer"] and rufnummer_existiert(neue_num):
            print("[Fehler] Diese Nummer wird bereits verwendet.")
        else:
            e["rufnummer"] = neue_num

    aktualisieren()
    print("[OK] Die Änderungen wurden übernommen.")


def contact_loeschen():
    """Löscht einen Kontakt nach Bestätigung."""
    name = input("\nWelchen Kontakt möchtest du entfernen? ").strip()
    e = next((c for c in contact_liste if c["name"].lower() == name.lower()), None)
    
    if e:
        bestaetigung = input(f"Wirklich '{e['name']}' löschen? (j/n): ")
        if bestaetigung.lower() == "j":
            contact_liste.remove(e)
            speichern()
            print("[OK] Kontakt erfolgreich gelöscht.")
    else:
        print("[!] Kontakt nicht vorhanden.")


def alle_loeschen():
    """Setzt die gesamte Datenbank zurück (Sicherheitscode erforderlich)."""
    print("\n!!! GEFAHRENZONE !!!")
    if input("Sicherheitscode eingeben: ") == SICHERHEITSCODE:
        if input("Wirklich ALLE Daten unwiderruflich löschen? (j/n): ").lower() == "j":
            contact_liste.clear()
            speichern()
            print("[OK] Alle Daten wurden gelöscht.")
    else:
        print("[Abbruch] Falscher Code.")


def exit_programm():
    """Beendet das Programm."""
    print("\nProgramm beendet. Bis bald!")
    exit()


# ------------------------------------------------------------------------------
# 7. PROGRAMM-STEUERUNG (HAUPTSCHLEIFE)
# ------------------------------------------------------------------------------

# Dispatcher für die Menüpunkte
aktionen = {
    "1": contacts_anzeigen,
    "2": contact_hinzufuegen,
    "3": contact_aendern,
    "4": contact_loeschen,
    "5": alle_loeschen,
    "6": exit_programm
}

if __name__ == "__main__":
    # Initiales Laden der Kontakte aus der Datei
    laden()
    
    while True:
        menue_anzeigen()
        auswahl = input("Welche Aktion möchtest du ausführen? (1-6): ").strip()
        
        aktion = aktionen.get(auswahl)
        if aktion:
            aktion()
        else:
            print("[!] Ungültige Eingabe. Bitte eine Zahl von 1 bis 6 wählen.")