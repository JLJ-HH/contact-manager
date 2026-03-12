document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');
    const contactsBody = document.getElementById('contacts-body');
    const searchInput = document.getElementById('search-input');
    const submitBtn = document.getElementById('submit-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const contactIndexInput = document.getElementById('contact-index');

    let allContacts = [];
    let isEditing = false;

    // Fetch and display contacts
    async function loadContacts() {
        try {
            const response = await fetch('/api/contacts');
            allContacts = await response.json();
            renderTable(allContacts);
        } catch (error) {
            console.error('Fehler beim Laden:', error);
        }
    }

    function renderTable(contacts) {
        contactsBody.innerHTML = '';
        contacts.forEach((contact, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${contact.vorname || ''}</td>
                <td>${contact.nachname || ''}</td>
                <td>${contact.strasse || ''}</td>
                <td>${contact.plz || ''}</td>
                <td>${contact.email || ''}</td>
                <td>${contact.rufnummer || ''}</td>
                <td>${contact.mobil || ''}</td>
                <td class="actions-col">
                    <button class="btn action-btn edit-btn" onclick="editContact(${index})">Ändern</button>
                    <button class="btn action-btn delete-btn" onclick="deleteContact(${index})">Löschen</button>
                </td>
            `;
            contactsBody.appendChild(row);
        });
    }

    // Handle form submit (Add/Update)
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            vorname: document.getElementById('vorname').value.trim(),
            nachname: document.getElementById('nachname').value.trim(),
            strasse: document.getElementById('strasse').value.trim(),
            plz: document.getElementById('plz').value.trim(),
            email: document.getElementById('email').value.trim(),
            rufnummer: document.getElementById('rufnummer').value.trim(),
            mobil: document.getElementById('mobil').value.trim()
        };

        try {
            let url = '/api/contacts';
            let method = 'POST';

            if (isEditing) {
                const index = contactIndexInput.value;
                url = `/api/contacts/${index}`;
                method = 'PUT';
            }

            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                resetForm();
                loadContacts();
            }
        } catch (error) {
            console.error('Fehler beim Speichern:', error);
        }
    });

    // Search functionality
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allContacts.filter(c => 
            (c.vorname && c.vorname.toLowerCase().includes(term)) ||
            (c.nachname && c.nachname.toLowerCase().includes(term)) ||
            (c.rufnummer && c.rufnummer.includes(term)) ||
            (c.mobil && c.mobil.includes(term))
        );
        renderTable(filtered);
    });

    // Exposed to window for onclick handlers
    window.editContact = (index) => {
        const contact = allContacts[index];
        document.getElementById('vorname').value = contact.vorname || '';
        document.getElementById('nachname').value = contact.nachname || '';
        document.getElementById('strasse').value = contact.strasse || '';
        document.getElementById('plz').value = contact.plz || '';
        document.getElementById('email').value = contact.email || '';
        document.getElementById('rufnummer').value = contact.rufnummer || '';
        document.getElementById('mobil').value = contact.mobil || '';
        
        contactIndexInput.value = index;
        isEditing = true;
        submitBtn.textContent = 'Aktualisieren';
        cancelBtn.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.deleteContact = async (index) => {
        if (confirm('Soll dieser Kontakt wirklich gelöscht werden?')) {
            try {
                const response = await fetch(`/api/contacts/${index}`, { method: 'DELETE' });
                if (response.ok) loadContacts();
            } catch (error) {
                console.error('Fehler beim Löschen:', error);
            }
        }
    };

    function resetForm() {
        contactForm.reset();
        contactIndexInput.value = '';
        isEditing = false;
        submitBtn.textContent = 'Hinzufügen';
        cancelBtn.classList.add('hidden');
    }

    cancelBtn.addEventListener('click', resetForm);

    // Initial load
    loadContacts();
});
