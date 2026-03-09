# ==============================================================================
# CONTACT MANAGER - GUI VERSION (MIT SUCHE)
# ==============================================================================
# Dieses Programm bietet eine grafische Oberfläche zur Kontaktverwaltung.
# Die Datenlogik ist in data_manager.py ausgelagert.
# ==============================================================================

import tkinter as tk
from tkinter import messagebox, ttk
import data_manager

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        # Daten laden
        self.kontakte = data_manager.laden()
        self.sicherheits_code = "1234"

        self.setup_ui()
        # Initial keine Kontakte anzeigen (leere Liste)
        self.update_tabelle(filter_text=None)

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # --- Titel ---
        title_label = tk.Label(self.root, text="CONTACT MANAGER", font=("Arial", 22, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=(15, 5))

        # --- Suchbereich ---
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Suchen (z.B. 'A' oder 'zeige alle'):", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # --- Eingabeformular ---
        form_frame = tk.LabelFrame(self.root, text="Kontakt-Details", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 9, "bold"))
        form_frame.pack(padx=20, pady=10, fill="x")

        labels = ["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:"]
        self.entries = {}

        for i, text in enumerate(labels):
            row, col = divmod(i, 3)
            tk.Label(form_frame, text=text, bg="#f0f0f0").grid(row=row*2, column=col, sticky="w", padx=5)
            entry = tk.Entry(form_frame, width=28)
            entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10))
            self.entries[text] = entry

        # --- Buttons (Aktionen) ---
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Hinzufügen", command=self.hinzufuegen, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Ändern", command=self.aendern, bg="#2196F3", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Löschen", command=self.loeschen, bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Alle Löschen", command=self.alle_loeschen, bg="#333", fg="white", width=15).pack(side="left", padx=5)

        # --- Tabelle ---
        tab_frame = tk.Frame(self.root)
        tab_frame.pack(padx=20, pady=10, fill="both", expand=True)

        spalten = ("Vorname", "Nachname", "Straße", "PLZ", "E-Mail", "Telefon")
        self.tree = ttk.Treeview(tab_frame, columns=spalten, show="headings")
        
        for col in spalten:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_search_change(self, event):
        """Wird bei jeder Tastatureingabe im Suchfeld aufgerufen."""
        text = self.search_entry.get().strip().lower()
        if text == "":
            self.update_tabelle(filter_text=None) # Liste leeren
        else:
            self.update_tabelle(filter_text=text)

    def update_tabelle(self, filter_text=None):
        """Aktualisiert die Treeview-Anzeige basierend auf dem Suchbegriff."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Wenn kein Filter gesetzt ist (oder Suchfeld leer), zeigen wir nichts an
        if filter_text is None:
            return

        for i, k in enumerate(self.kontakte):
            # Prüfen, ob der Kontakt zum Filter passt
            matches = False
            if filter_text == "zeige alle" or filter_text == "zeige liste":
                matches = True
            elif (filter_text in k["vorname"].lower() or 
                  filter_text in k["nachname"].lower() or 
                  filter_text in k["rufnummer"].lower()):
                matches = True
            
            if matches:
                # Wir speichern den Original-Index als iid (item id)
                self.tree.insert("", "end", iid=str(i), values=(k["vorname"], k["nachname"], k["strasse"], k["plz"], k["email"], k["rufnummer"]))

    def get_input_data(self):
        """Hilfsfunktion zum Auslesen der Entry-Felder."""
        return {
            "vorname": self.entries["Vorname:"].get().strip(),
            "nachname": self.entries["Nachname:"].get().strip(),
            "strasse": self.entries["Straße:"].get().strip(),
            "plz": self.entries["PLZ:"].get().strip(),
            "email": self.entries["E-Mail:"].get().strip(),
            "rufnummer": self.entries["Telefon:"].get().strip()
        }

    def clear_inputs(self):
        """Leert alle Eingabefelder."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def on_select(self, event):
        """Befüllt die Felder, wenn ein Kontakt in der Tabelle ausgewählt wird."""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0])["values"]
        self.clear_inputs()
        # Einträge befüllen (nur wenn Werte vorhanden sind)
        for i, key in enumerate(["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:"]):
            val = values[i]
            self.entries[key].insert(0, str(val) if val != "None" and val != "" else "")

    def hinzufuegen(self):
        data = self.get_input_data()
        if not data_manager.ist_gueltiger_text(data["vorname"]) or not data_manager.ist_gueltiger_text(data["nachname"]):
            messagebox.showerror("Fehler", "Vor- und Nachname müssen ausgefüllt sein.")
            return
        
        self.kontakte.append(data)
        data_manager.speichern(self.kontakte)
        
        # Suche zurücksetzen und Liste aktualisieren
        self.search_entry.delete(0, tk.END)
        self.update_tabelle(filter_text="zeige alle")
        self.clear_inputs()
        messagebox.showinfo("Erfolg", "Kontakt wurde hinzugefügt.")

    def aendern(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus der Tabelle aus.")
            return
        
        # Wir holen den Original-Index aus der iid des Treeview-Items
        original_index = int(selected[0])
        new_data = self.get_input_data()
        
        # Validierung
        if not new_data["vorname"] or not new_data["nachname"]:
            messagebox.showerror("Fehler", "Vor- und Nachname dürfen nicht leer sein.")
            return

        # Den Kontakt direkt über den Index aktualisieren
        self.kontakte[original_index] = new_data
        data_manager.speichern(self.kontakte)
        
        # Ansicht aktualisieren (Suchbegriff beibehalten falls vorhanden)
        current_search = self.search_entry.get().strip().lower()
        self.update_tabelle(filter_text=current_search if current_search else "zeige alle")
        messagebox.showinfo("Erfolg", "Kontakt wurde aktualisiert.")

    def loeschen(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus.")
            return
        
        if messagebox.askyesno("Bestätigung", "Soll dieser Kontakt wirklich gelöscht werden?"):
            # Original-Index holen
            original_index = int(selected[0])
            # Kontakt entfernen
            self.kontakte.pop(original_index)
            data_manager.speichern(self.kontakte)
            
            # Tabelle aktualisieren
            current_search = self.search_entry.get().strip().lower()
            self.update_tabelle(filter_text=current_search if current_search else None)
            self.clear_inputs()

    def alle_loeschen(self):
        if messagebox.askyesno("Gefahrenzone", "Willst du wirklich ALLE Kontakte löschen?"):
             self.kontakte.clear()
             data_manager.speichern(self.kontakte)
             self.update_tabelle(filter_text=None)
             self.clear_inputs()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()