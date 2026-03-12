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
    THEMES = {
        "light": {
            "bg": "#f8f9fa",
            "fg": "#2c3e50",
            "card_bg": "#ffffff",
            "card_fg": "#2c3e50",
            "entry_bg": "#ffffff",
            "entry_fg": "#333333",
            "entry_border": "#e0e0e0",
            "btn_text": "white",
            "accent": "#3498db"
        },
        "dark": {
            "bg": "#1e1e1e",
            "fg": "#e0e0e0",
            "card_bg": "#2d2d2d",
            "card_fg": "#e0e0e0",
            "entry_bg": "#3d3d3d",
            "entry_fg": "#ffffff",
            "entry_border": "#4d4d4d",
            "btn_text": "white",
            "accent": "#2980b9"
        }
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("1000x800")
        self.root.minsize(600, 500)
        
        # Daten laden
        self.kontakte = data_manager.laden()
        self.load_config()

        # Grid-Gewichtung für das Hauptfenster
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)

        self.setup_ui()
        
        # Initial Liste verstecken
        self.list_visible = False
        self.tab_frame.pack_forget()
        
        # Theme anwenden
        self.apply_theme()

    def load_config(self):
        """Lädt die Konfiguration aus der settings.ini."""
        self.config = configparser.ConfigParser()
        self.ini_path = "settings.ini"
        if os.path.exists(self.ini_path):
            self.config.read(self.ini_path)
            self.sicherheits_code = self.config.get("Security", "delete_code", fallback="1234")
            self.current_theme = self.config.get("Appearance", "theme", fallback="light")
        else:
            self.sicherheits_code = "1234"
            self.current_theme = "light"

    def save_config(self):
        """Speichert die aktuelle Konfiguration."""
        if not self.config.has_section("Security"):
            self.config.add_section("Security")
        if not self.config.has_section("Appearance"):
            self.config.add_section("Appearance")
            
        self.config.set("Security", "delete_code", self.sicherheits_code)
        self.config.set("Appearance", "theme", self.current_theme)
        
        with open(self.ini_path, "w") as configfile:
            self.config.write(configfile)

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # --- Titel ---
        self.title_label = tk.Label(self.main_frame, text="CONTACT MANAGER", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=(20, 10), fill="x")

        # --- Such- & Theme-Bereich ---
        self.search_card = tk.LabelFrame(self.main_frame, text="Suche & Kontrolle", font=("Arial", 10, "bold"), padx=15, pady=15, relief="flat", highlightthickness=1)
        self.search_card.pack(fill="x", padx=25, pady=10)
        
        search_inner = tk.Frame(self.search_card)
        search_inner.pack(fill="x")

        self.search_label = tk.Label(search_inner, text="Begriff:", font=("Arial", 10))
        self.search_label.pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(search_inner, font=("Arial", 11), relief="solid", borderwidth=1)
        self.search_entry.pack(side="left", padx=5, ipady=3, expand=True, fill="x")
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        
        self.btn_search = tk.Button(search_inner, text="Suchen", command=self.perform_search, font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
        self.btn_search.pack(side="left", padx=5)
        
        self.btn_show_all = tk.Button(search_inner, text="Alle Anzeigen", command=self.show_all_contacts, font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5, cursor="hand2")
        self.btn_show_all.pack(side="left", padx=5)

        self.btn_theme = tk.Button(search_inner, text="🌓", command=self.toggle_theme, font=("Arial", 12), relief="flat", padx=10, pady=2, cursor="hand2")
        self.btn_theme.pack(side="left", padx=(15, 0))
        
        # --- Eingabeformular ---
        self.form_card = tk.LabelFrame(self.main_frame, text="Kontakt-Details", font=("Arial", 10, "bold"), padx=15, pady=15, relief="flat", highlightthickness=1)
        self.form_card.pack(padx=25, pady=10, fill="x")

        self.field_definitions = [
            ("Vorname:", "Vorname:", 25),
            ("Nachname:", "Nachname:", 25),
            ("Straße:", "Straße:", 40),
            ("PLZ:", "PLZ:", 10),
            ("E-Mail:", "E-Mail:", 35),
            ("Telefon:", "Telefon:", 20),
            ("Mobil:", "Mobil:", 20)
        ]
        
        self.entries = {}
        self.entry_widgets = []

        for text, key, width in self.field_definitions:
            container = tk.Frame(self.form_card)
            label = tk.Label(container, text=text, font=("Arial", 9), anchor="w")
            entry = tk.Entry(container, font=("Arial", 10), relief="solid", borderwidth=1)
            self.entries[key] = entry
            self.entry_widgets.append((container, label, entry, width))

        # Initiales Layout setzen
        self.root.update_idletasks()
        self.reorganize_form()
        
        self.root.bind("<Configure>", self.on_root_configure)

        # --- Buttons (Aktionen) ---
        self.btn_action_frame = tk.Frame(self.main_frame)
        self.btn_action_frame.pack(pady=10, fill="x")
        
        self.btn_inner = tk.Frame(self.btn_action_frame)
        self.btn_inner.pack(anchor="center")

        actions = [
            ("Hinzufügen", self.hinzufuegen, "#2ecc71"),
            ("Ändern", self.aendern, "#f1c40f"),
            ("Leeren", self.clear_inputs, "#e67e22"),
            ("Löschen", self.loeschen, "#e74c3c"),
            ("Alle löschen", self.alle_loeschen, "#34495e")
        ]

        self.action_buttons = []
        for text, cmd, color in actions:
            btn = tk.Button(self.btn_inner, text=text, command=cmd, bg=color, fg="white", font=("Arial", 10, "bold"), width=12, relief="flat", pady=6, cursor="hand2")
            btn.pack(side="left", padx=5)
            self.action_buttons.append(btn)

        # --- Tabelle (Initial versteckt) ---
        self.tab_frame = tk.Frame(self.main_frame, highlightthickness=1)

        spalten = ("Vorname", "Nachname", "Straße", "PLZ", "E-Mail", "Telefon", "Mobil")
        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.tree_style.configure("Treeview", rowheight=25, font=("Arial", 10))
        
        self.tree = ttk.Treeview(self.tab_frame, columns=spalten, show="headings", selectmode="browse")
        
        column_widths = {"Vorname": 120, "Nachname": 120, "Straße": 200, "PLZ": 60, "E-Mail": 180, "Telefon": 120, "Mobil": 120}
        
        for col in spalten:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="w")

        self.tree.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        
        self.tree_scrollbar = ttk.Scrollbar(self.tab_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side="right", fill="y", padx=(0,5), pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def apply_theme(self):
        """Wendet das aktuelle Theme auf alle Widgets an."""
        colors = self.THEMES[self.current_theme]
        
        self.root.configure(bg=colors["bg"])
        self.main_frame.configure(bg=colors["bg"])
        
        # Titel
        self.title_label.configure(bg=colors["bg"], fg=colors["fg"])
        
        # Suchbereich
        self.search_card.configure(bg=colors["card_bg"], fg=colors["card_fg"], highlightbackground=colors["entry_border"])
        self.search_card.master.configure(bg=colors["bg"]) # main_frame
        for child in self.search_card.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=colors["card_bg"])
                for grand in child.winfo_children():
                    if isinstance(grand, tk.Label):
                        grand.configure(bg=colors["card_bg"], fg=colors["card_fg"])
                    elif isinstance(grand, tk.Entry):
                        grand.configure(bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["entry_fg"], highlightthickness=1, highlightbackground=colors["entry_border"])
        
        self.btn_search.configure(bg=colors["accent"], fg=colors["btn_text"])
        self.btn_show_all.configure(bg="#95a5a6", fg=colors["btn_text"])
        self.btn_theme.configure(bg=colors["card_bg"], fg=colors["card_fg"])

        # Formular
        self.form_card.configure(bg=colors["card_bg"], fg=colors["card_fg"], highlightbackground=colors["entry_border"])
        for container, label, entry, _ in self.entry_widgets:
            container.configure(bg=colors["card_bg"])
            label.configure(bg=colors["card_bg"], fg=colors["card_fg"])
            entry.configure(bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["entry_fg"], highlightthickness=1, highlightbackground=colors["entry_border"])

        # Aktionsbuttons
        self.btn_action_frame.configure(bg=colors["bg"])
        self.btn_inner.configure(bg=colors["bg"])
        
        # Tabelle
        self.tab_frame.configure(bg=colors["card_bg"], highlightbackground=colors["entry_border"])
        
        # Treeview Style
        self.tree_style.configure("Treeview", 
            background=colors["entry_bg"], 
            foreground=colors["entry_fg"], 
            fieldbackground=colors["entry_bg"])
        self.tree_style.map("Treeview", background=[("selected", colors["accent"])])
        
        self.tree_style.configure("Treeview.Heading", 
            background=colors["card_bg"], 
            foreground=colors["card_fg"])

    def toggle_theme(self):
        """Wechselt zwischen Light und Dark mode."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.save_config()

    def on_root_configure(self, event):
        """Wird aufgerufen, wenn das Fenster in der Größe verändert wird."""
        if event.widget == self.root:
            self.reorganize_form()

    def reorganize_form(self):
        """Berechnet Spalten basierend auf Breite."""
        width = self.root.winfo_width() - 80
        
        for container, _, _, _ in self.entry_widgets:
            container.grid_forget()
            
        if width > 900:
            cols = 3
        elif width > 600:
            cols = 2
        else:
            cols = 1

        for i in range(cols):
            self.form_card.columnconfigure(i, weight=1)

        for i, (container, label, entry, _) in enumerate(self.entry_widgets):
            row, col = divmod(i, cols)
            container.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            label.pack(side="top", anchor="w")
            entry.pack(side="top", fill="x", ipady=3)

    def toggle_list(self, show=True):
        """Zeigt oder versteckt die Kontaktliste."""
        if show:
            if not self.list_visible:
                self.tab_frame.pack(padx=25, pady=(0, 20), fill="both", expand=True)
                self.list_visible = True
        else:
            if self.list_visible:
                self.tab_frame.pack_forget()
                self.list_visible = False

    def perform_search(self):
        """Führt die Suche aus und zeigt die Liste an."""
        text = self.search_entry.get().strip().lower()
        if text:
            self.update_tabelle(filter_text=text)
            self.toggle_list(show=True)
        else:
            self.toggle_list(show=False)

    def show_all_contacts(self):
        """Zeigt alle Kontakte in der Liste."""
        self.search_entry.delete(0, tk.END)
        self.update_tabelle(filter_text="zeige alle")
        self.toggle_list(show=True)

    def update_tabelle(self, filter_text=None):
        """Aktualisiert die Treeview-Anzeige."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if filter_text is None:
            return

        for i, k in enumerate(self.kontakte):
            matches = False
            if filter_text == "zeige alle":
                matches = True
            else:
                search_fields = [k["vorname"], k["nachname"], k["rufnummer"], k.get("mobil", ""), k.get("email", ""), k.get("strasse", "")]
                if any(filter_text in str(f).lower() for f in search_fields):
                    matches = True
            
            if matches:
                self.tree.insert("", "end", iid=str(i), values=(k["vorname"], k["nachname"], k["strasse"], k["plz"], k["email"], k["rufnummer"], k.get("mobil", "")))

    def get_input_data(self):
        """Hilfsfunktion zum Auslesen der Entry-Felder."""
        return {k.replace(":", "").lower(): v.get().strip() for k, v in self.entries.items()}

    def clear_inputs(self):
        """Leert alle Eingabefelder."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def on_select(self, event):
        """Befüllt die Felder, wenn ein Kontakt ausgewählt wird."""
        selected = self.tree.selection()
        if not selected: return
        
        values = self.tree.item(selected[0])["values"]
        self.clear_inputs()
        
        field_keys = ["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:", "Mobil:"]
        for i, key in enumerate(field_keys):
            if i < len(values):
                val = values[i]
                self.entries[key].insert(0, str(val) if val != "None" and val != "" else "")

    def hinzufuegen(self):
        data = self.get_input_data()
        if not data.get("vorname") or not data.get("nachname"):
            messagebox.showerror("Fehler", "Vor- und Nachname müssen ausgefüllt sein.")
            return
        
        formatted_data = {
            "vorname": data["vorname"],
            "nachname": data["nachname"],
            "strasse": data["straße"],
            "plz": data["plz"],
            "email": data["e-mail"],
            "rufnummer": data["telefon"],
            "mobil": data["mobil"]
        }
        
        self.kontakte.append(formatted_data)
        data_manager.speichern(self.kontakte)
        # Liste NICHT automatisch anzeigen
        self.clear_inputs()
        messagebox.showinfo("Erfolg", "Kontakt wurde hinzugefügt.")

    def aendern(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus der Tabelle aus.")
            return
        
        original_index = int(selected[0])
        data = self.get_input_data()
        
        if not data["vorname"] or not data["nachname"]:
            messagebox.showerror("Fehler", "Vor- und Nachname dürfen nicht leer sein.")
            return

        formatted_data = {
            "vorname": data["vorname"],
            "nachname": data["nachname"],
            "strasse": data["straße"],
            "plz": data["plz"],
            "email": data["e-mail"],
            "rufnummer": data["telefon"],
            "mobil": data["mobil"]
        }

        self.kontakte[original_index] = formatted_data
        data_manager.speichern(self.kontakte)
        self.update_tabelle(filter_text=self.search_entry.get().strip().lower() or "zeige alle")
        messagebox.showinfo("Erfolg", "Kontakt wurde aktualisiert.")

    def loeschen(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus.")
            return
        
        eingabe = simpledialog.askstring("Sicherheit", "Bitte gib den Code zum Löschen ein:", show='*')
        if eingabe != self.sicherheits_code:
            messagebox.showerror("Fehler", "Falscher Code! Löschen abgebrochen.")
            return

        if messagebox.askyesno("Bestätigung", "Soll dieser Kontakt wirklich gelöscht werden?"):
            original_index = int(selected[0])
            self.kontakte.pop(original_index)
            data_manager.speichern(self.kontakte)
            self.update_tabelle(filter_text=self.search_entry.get().strip().lower() or "zeige alle")
            self.clear_inputs()

    def alle_loeschen(self):
        eingabe = simpledialog.askstring("Sicherheit", "Bitte gib den Code zum Löschen aller Kontakte ein:", show='*')
        if eingabe != self.sicherheits_code:
            messagebox.showerror("Fehler", "Falscher Code! Löschen abgebrochen.")
            return

        if messagebox.askyesno("Gefahrenzone", "Willst du wirklich ALLE Kontakte löschen?"):
             self.kontakte.clear()
             data_manager.speichern(self.kontakte)
             self.update_tabelle(filter_text=None)
             self.toggle_list(show=False)
             self.clear_inputs()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()