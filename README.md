# Contact Manager - GUI Verwaltungssystem

Diese Anwendung ist ein leistungsfähiges Tool zur Verwaltung von Kontakten mit einer benutzerfreundlichen grafischen Oberfläche (GUI).

## Funktionen

- **Grafische Oberfläche**: Einfache Bedienung über Fenster und Schaltflächen statt Terminal-Eingaben.
- **Getrennte Namensfelder**: Kontakte werden nun nach **Vorname** und **Nachname** getrennt verwaltet.
- **Tabellenansicht**: Alle Kontakte werden in einer sortierbaren Tabelle (Treeview) angezeigt.
- **Interaktives Editieren**: Wähle einen Kontakt in der Tabelle aus, um seine Daten direkt in die Eingabefelder zu laden und zu bearbeiten.
- **Sicherheitsfunktionen**: Bestätigungsdialoge verhindern versehentliches Löschen von Daten.
- **Clean Code Struktur**: Trennung von Datenlogik (`data_manager.py`) und Benutzeroberfläche (`contact_manager.py`).

## Installation & Start

1. **Voraussetzung**: Installiertes Python 3 (inkl. `tkinter`, was meist standardmäßig dabei ist).
2. **Start**: Führe die Hauptdatei aus:
   ```bash
   python contact_manager.py
   ```

## Datenstruktur & Migration

Die Daten werden in der `contacts.txt` im neuen Format gespeichert:
`Vorname|Nachname|Straße|PLZ|E-Mail|Telefonnummer`

**Hinweis**: Bestehende Daten im alten Format (`Name|Straße|...`) werden beim ersten Start automatisch erkannt und migriert, wobei der Name am ersten Leerzeichen in Vor- und Nachname gesplittet wird.

## Sicherheit

Kritische Aktionen wie das Löschen aller Daten erfordern eine Bestätigung über einen Sicherheitsdialog.
