# Contact Manager - Verwaltungssystem

Dieses Python-Programm ist ein leistungsfähiges Kommandozeilen-Tool zur strukturierten Verwaltung von Kontakten. Es ermöglicht das Speichern, Bearbeiten und Löschen von Personendaten in einer lokalen Datenbank.

## Funktionen

- **Kontakte anzeigen**: Übersichtliche Tabellendarstellung aller gespeicherten Kontakte.
- **Kontakt hinzufügen**: Interaktive Erstellung neuer Einträge mit Validierung von Name, E-Mail und Rufnummer.
- **Kontakt ändern**: Gezielte Bearbeitung einzelner Felder eines bestehenden Kontakts.
- **Kontakt löschen**: Einfaches Entfernen einzelner Einträge nach Bestätigung.
- **Alle Daten löschen**: Sicherheitsgeschützte Funktion zum Zurücksetzen der gesamten Datenbank (erfordert PIN: `1234`).
- **Persistenz**: Automatische Speicherung und Sortierung der Daten in der Datei `contacts.txt`.

## Installation & Start

1. **Voraussetzung**: Installiertes Python 3.
2. **Download**: Lade die Datei `contact_manager.py` in ein Verzeichnis deiner Wahl.
3. **Start**: Öffne ein Terminal im Verzeichnis und führe folgenden Befehl aus:
   ```bash
   python contact_manager.py
   ```

## Datenstruktur

Die Kontakte werden im folgenden Format in der `contacts.txt` gespeichert:
`Name|Straße|PLZ|E-Mail|Telefonnummer`

## Sicherheit

Für kritische Operationen (wie das Löschen aller Daten) wird ein Sicherheitscode abgefragt. Standardmäßig ist dieser auf `1234` eingestellt.
