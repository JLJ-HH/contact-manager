# Contact Manager - GUI Verwaltungssystem (mit Suche)

Diese Anwendung wurde um eine leistungsfähige Such- und Filterfunktion erweitert.

## Funktionen

- **Gefilterte Anzeige**: Die Kontaktliste ist beim Start standardmäßig leer. Kontakte erscheinen erst, wenn du im Suchfeld tippst.
- **Suche**: Filtere Kontakte in Echtzeit nach Vorname, Nachname oder Telefonnummer.
- **Spezialbefehle**: Gib `zeige alle` oder `zeige liste` in das Suchfeld ein, um alle Kontakte auf einmal zu sehen.
- **Punktuelles Ändern**: Wähle einen Kontakt in der Tabelle aus. Die Daten werden in die Felder geladen. Du kannst nun einzelne Felder (z.B. nur den Nachnamen) ändern und auf "Ändern" klicken.
- **Clean Code**: Datenlogik (`data_manager.py`) und GUI (`contact_manager.py`) sind strikt getrennt.

## Installation & Start

1. **Voraussetzung**: Python 3.
2. **Start**:
   ```bash
   python contact_manager.py
   ```

## Datenstruktur

Die Daten liegen in der `contacts.txt` im Format:
`Vorname|Nachname|Straße|PLZ|E-Mail|Telefonnummer`
