# ==============================================================================
# CONTACT MANAGER - GUI VERSION
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
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Daten laden
        self.kontakte = data_manager.laden()
        self.sicherheits_code = "1234"

        self.setup_ui()
        self.update_tabelle()

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # --- Titel ---
        title_label = tk.Label(self.root, text="CONTACT MANAGER", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)

        # --- Eingabeformular (Oben) ---
        form_frame = tk.LabelFrame(self.root, text="Kontakt-Details", padx=10, pady=10, bg="#f0f0f0")
        form_frame.pack(padx=20, pady=10, fill="x")

        # Grid-Layout für Felder
        labels = ["Vorname:", "Nachname:", "Straße:", "PLZ:", "E-Mail:", "Telefon:"]
        self.entries = {}

        for i, text in enumerate(labels):
            row, col = divmod(i, 3)
            tk.Label(form_frame, text=text, bg="#f0f0f0").grid(row=row*2, column=col, sticky="w", padx=5)
            entry = tk.Entry(form_frame, width=25)
            entry.grid(row=row*2+1, column=col, padx=5, pady=(0, 10))
            self.entries[text] = entry

        # --- Buttons (Aktionen) ---
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.add_btn = tk.Button(btn_frame, text="Hinzufügen", command=self.hinzufuegen, bg="#4CAF50", fg="white", width=15)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = tk.Button(btn_frame, text="Ändern", command=self.aendern, bg="#2196F3", fg="white", width=15)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Löschen", command=self.loeschen, bg="#f44336", fg="white", width=15)
        self.delete_btn.pack(side="left", padx=5)

        self.clear_all_btn = tk.Button(btn_frame, text="Alle Löschen", command=self.alle_loeschen, bg="#333", fg="white", width=15)
        self.clear_all_btn.pack(side="left", padx=5)

        # --- Tabelle (Mitte/Unten) ---
        tab_frame = tk.Frame(self.root)
        tab_frame.pack(padx=20, pady=10, fill="both", expand=True)

        spalten = ("Vorname", "Nachname", "Straße", "PLZ", "E-Mail", "Telefon")
        self.tree = ttk.Treeview(tab_frame, columns=spalten, show="headings")
        
        for col in spalten:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def update_tabelle(self):
        """Aktualisiert die Treeview-Anzeige."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for k in self.kontakte:
            self.tree.insert("", "end", values=(k["vorname"], k["nachname"], k["strasse"], k["plz"], k["email"], k["rufnummer"]))

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
        self.entries["Vorname:"].insert(0, values[0])
        self.entries["Nachname:"].insert(0, values[1])
        self.entries["Straße:"].insert(0, values[2])
        self.entries["PLZ:"].insert(0, values[3])
        self.entries["E-Mail:"].insert(0, values[4])
        self.entries["Telefon:"].insert(0, values[5])

    def hinzufuegen(self):
        data = self.get_input_data()
        if not data_manager.ist_gueltiger_text(data["vorname"]) or not data_manager.ist_gueltiger_text(data["nachname"]):
            messagebox.showerror("Fehler", "Vor- und Nachname müssen ausgefüllt sein.")
            return
        
        if not data_manager.ist_gueltige_email(data["email"]):
            messagebox.showerror("Fehler", "Ungültige E-Mail Adresse.")
            return

        self.kontakte.append(data)
        data_manager.speichern(self.kontakte)
        self.update_tabelle()
        self.clear_inputs()
        messagebox.showinfo("Erfolg", "Kontakt wurde hinzugefügt.")

    def aendern(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus der Tabelle aus.")
            return
        
        # Den alten Index finden (anhand der Telefonnummer als Beinahe-Unique-ID für dieses Beispiel)
        old_values = self.tree.item(selected[0])["values"]
        new_data = self.get_input_data()
        
        for i, k in enumerate(self.kontakte):
            if k["rufnummer"] == str(old_values[5]): # Match per Nummer
                self.kontakte[i] = new_data
                break
        
        data_manager.speichern(self.kontakte)
        self.update_tabelle()
        messagebox.showinfo("Erfolg", "Kontakt wurde aktualisiert.")

    def loeschen(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wähle einen Kontakt aus.")
            return
        
        if messagebox.askyesno("Bestätigung", "Soll dieser Kontakt wirklich gelöscht werden?"):
            values = self.tree.item(selected[0])["values"]
            self.kontakte = [k for k in self.kontakte if k["rufnummer"] != str(values[5])]
            data_manager.speichern(self.kontakte)
            self.update_tabelle()
            self.clear_inputs()

    def alle_loeschen(self):
        # Einfache Abfrage des Codes via Dialog wäre schöner, hier tun wir es via askyesno + Abfrage
        # Da tkinter keinen Standard-Passwort-Dialog hat, fragen wir nur Bestätigung.
        if messagebox.askyesno("Gefahrenzone", "Willst du wirklich ALLE Kontakte löschen?"):
             self.kontakte.clear()
             data_manager.speichern(self.kontakte)
             self.update_tabelle()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()