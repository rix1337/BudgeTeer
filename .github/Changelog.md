### Installation und Update:

`pip install -U budgeteer`

---

### Bekannte Fehler:
- Budgettyp (monatlich, jährlich, wöchentlich) wird nicht beachtet
- Budget-Einträge vom Typ "wöchentlich" können nicht pro Woche als gebucht markiert werden
- Budget-Einträge vom Typ "jährlich" können nicht pro Jahr als gebucht markiert werden
- Budget-Einträge vom Typ "einmalig" können nicht dauerhaft als gebucht markiert werden
- Zukünftige Restbudgets sind nicht im Kopfbereich aufrufbar


### Changelog BudgeTeer:

#### v.0.1.2
- Fehlerbehebung bei Aktivierung von Basic Auth
- Die Gültigkeit von künftigen Budgets wird beim Anzeigen und Berechnen dieser beachtet
- Budgets können monatlich als gebucht markiert werden

#### v.0.1.1
- Fehlerkorrektur beim Hinzufügen neuer Konten, Transaktionen und Budgets
- Budgets können umbenannt und gelöscht werden

#### v.0.1.0
- Kontostände, Budgets und offene Transaktionen werden beim Sperren automatisch gespeichert
- Budgeteintrag auf Gültigkeitszeitraum prüfen
- Datepicker implementiert (für Gültigkeitszeitraum der Budgets)
- Kontostände in die Kopfzeile verschoben
- Schaltfläche "Speichern" beim Löschen von Budgets und offenen Transaktionen anzeigen
