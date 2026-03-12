# ==============================================================================
# CONTACT MANAGER - GUI VERSION (MIT SUCHE)
# ==============================================================================
# Dieses Programm bietet eine grafische Oberfläche zur Kontaktverwaltung.
# Die Datenlogik ist in data_manager.py ausgelagert.
# ==============================================================================

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import data_manager
import configparser
import os

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Grid-Gewichtung für das Hauptfenster (Wichtig für Responsivität)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1) # Wir packen alles in ein Main-Frame
        
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)

        # Daten laden
        self.kontakte = data_manager.laden()
        self.load_config()

        self.setup_ui()
        # Initial keine Kontakte anzeigen (leere Liste)
        self.update_tabelle(filter_text=None)

    def load_config(self):
        """Lädt die Sicherheitskonfiguration aus der settings.ini."""
        self.config = configparser.ConfigParser()
        ini_path = "settings.ini"
        if os.path.exists(ini_path):
            self.config.read(ini_path)
            self.sicherheits_code = self.config.get("Security", "delete_code", fallback="1234")
        else:
            self.sicherheits_code = "1234" # Fallback

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # --- Titel ---
        title_label = tk.Label(self.main_frame, text="CONTACT MANAGER", font=("Arial", 22, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=(15, 5), fill="x")

        # --- Suchbereich ---
        search_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Suchen (z.B. 'A' oder 'zeige alle'):", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # --- Eingabeformular ---
        self.form_frame = tk.LabelFrame(self.main_frame, text="Kontakt-Details", padx=10, pady=10, bg="#f0f0f0", font=("Arial", 9, "bold"))
        self.form_frame.pack(padx=20, pady=10, fill="x")

<<<<<<< HEAD
        labels = ["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:", "Mobil:"]
=======
        self.labels_config = ["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:", "Mobil:"]
>>>>>>> 6e752066ceb5eb8ef4c70052184269978ae721dc
        self.entries = {}
        self.entry_widgets = [] # Hilfsliste für schnellen Zugriff beim Redraw

        for text in self.labels_config:
            label = tk.Label(self.form_frame, text=text, bg="#f0f0f0")
            entry = tk.Entry(self.form_frame, width=28)
            self.entries[text] = entry
            self.entry_widgets.append((label, entry))

        # Initiales Layout setzen
        self.root.update_idletasks() # Sicherstellen, dass Geometrie bekannt ist
        self.reorganize_form()
        
        # Bind Resize-Event
        self.root.bind("<Configure>", self.on_root_configure)

        # --- Buttons (Aktionen) ---
        btn_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=5, fill="x")
        
        # Container für die Buttons, um sie zu zentrieren und flexibel zu halten
        btn_inner_frame = tk.Frame(btn_frame, bg="#f0f0f0")
        btn_inner_frame.pack(anchor="center")

        tk.Button(btn_inner_frame, text="Hinzufügen", command=self.hinzufuegen, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5, pady=5)
        tk.Button(btn_inner_frame, text="Ändern", command=self.aendern, bg="#2196F3", fg="white", width=15).pack(side="left", padx=5, pady=5)
        tk.Button(btn_inner_frame, text="Zurücksetzen", command=self.clear_inputs, bg="#FF9800", fg="white", width=15).pack(side="left", padx=5, pady=5)
        tk.Button(btn_inner_frame, text="Löschen", command=self.loeschen, bg="#f44336", fg="white", width=15).pack(side="left", padx=5, pady=5)
        tk.Button(btn_inner_frame, text="Alle Löschen", command=self.alle_loeschen, bg="#333", fg="white", width=15).pack(side="left", padx=5, pady=5)

        # --- Tabelle ---
        tab_frame = tk.Frame(self.main_frame)
        tab_frame.pack(padx=20, pady=10, fill="both", expand=True)

        spalten = ("Vorname", "Nachname", "Straße", "PLZ", "E-Mail", "Telefon", "Mobil")
        self.tree = ttk.Treeview(tab_frame, columns=spalten, show="headings")
        
        for col in spalten:
            self.tree.heading(col, text=col)
<<<<<<< HEAD
            self.tree.column(col, width=120)
=======
            self.tree.column(col, width=100, minwidth=80, stretch=True)
>>>>>>> 6e752066ceb5eb8ef4c70052184269978ae721dc

        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_root_configure(self, event):
        """Wird aufgerufen, wenn das Fenster in der Größe verändert wird."""
        # Wir reagieren nur auf Änderungen am Hauptfenster selbst
        if event.widget == self.root:
            self.reorganize_form()

    def reorganize_form(self):
        """Berechnet die Spaltenanzahl basierend auf der Breite und ordnet die Felder neu an."""
        width = self.root.winfo_width()
        
        # Annahme: Ein Feld inkl. Padding braucht ca. 250 Pixel
        num_cols = max(1, width // 300)
        
        # Alle Widgets erst mal aus dem Grid nehmen
        for label, entry in self.entry_widgets:
            label.grid_forget()
            entry.grid_forget()
            
        # Grid-Gewichtung zurücksetzen
        for i in range(10): # Genug Spalten abdecken
            self.form_frame.columnconfigure(i, weight=0)

        # Neu anordnen
        for i, (label, entry) in enumerate(self.entry_widgets):
            row, col = divmod(i, num_cols)
            label.grid(row=row*2, column=col, sticky="w", padx=5)
            entry.grid(row=row*2+1, column=col, sticky="ew", padx=5, pady=(0, 10))
            self.form_frame.columnconfigure(col, weight=1)

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
                  filter_text in k["rufnummer"].lower() or
                  filter_text in k.get("mobil", "").lower()):
                matches = True
            
            if matches:
                # Wir speichern den Original-Index als iid (item id)
                self.tree.insert("", "end", iid=str(i), values=(k["vorname"], k["nachname"], k["strasse"], k["plz"], k["email"], k["rufnummer"], k.get("mobil", "")))

    def get_input_data(self):
        """Hilfsfunktion zum Auslesen der Entry-Felder."""
        return {
            "vorname": self.entries["Vorname:"].get().strip(),
            "nachname": self.entries["Nachname:"].get().strip(),
            "strasse": self.entries["Straße:"].get().strip(),
            "plz": self.entries["PLZ:"].get().strip(),
            "email": self.entries["E-Mail:"].get().strip(),
            "rufnummer": self.entries["Telefon:"].get().strip(),
            "mobil": self.entries["Mobil:"].get().strip()
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
        for i, key in enumerate(["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:", "Mobil:"]):
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
        
        # Sicherheitsabfrage
        eingabe = simpledialog.askstring("Sicherheit", "Bitte gib den Code zum Löschen ein:", show='*')
        if eingabe != self.sicherheits_code:
            messagebox.showerror("Fehler", "Falscher Code! Löschen abgebrochen.")
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
        # Sicherheitsabfrage
        eingabe = simpledialog.askstring("Sicherheit", "Bitte gib den Code zum Löschen aller Kontakte ein:", show='*')
        if eingabe != self.sicherheits_code:
            messagebox.showerror("Fehler", "Falscher Code! Löschen abgebrochen.")
            return

        if messagebox.askyesno("Gefahrenzone", "Willst du wirklich ALLE Kontakte löschen?"):
             self.kontakte.clear()
             data_manager.speichern(self.kontakte)
             self.update_tabelle(filter_text=None)
             self.clear_inputs()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()