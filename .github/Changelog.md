### Installation und Update:

`pip install -U budgeteer`

---

### Changelog BudgeTeer:

#### v.0.1.2
- Fehlerbehebung bei Aktivierung von Basic Auth
- Die Gültigkeit von künftigen Budgets wird bei deren Berechnung beachtet
- Budgets können monatlich als gebucht markiert werden
- ToDo
  - Add Yearly budget type (select month only for validity)
  - Add Weekly budget type
    - calculate weeks of month automatically
    - instead of done check do done +/- counter button
  - Allow displaying future remaining budget in head

#### v.0.1.1
- Fehlerkorrektur beim Hinzufügen neuer Konten, Transaktionen und Budgets
- Budgets können umbenannt und gelöscht werden

#### v.0.1.0
- Kontostände, Budgets und offene Transaktionen werden beim Sperren automatisch gespeichert
- Budgeteintrag auf Gültigkeitszeitraum prüfen
- Datepicker implementiert (für Gültigkeitszeitraum der Budgets)
- Kontostände in die Kopfzeile verschoben
- Schaltfläche "Speichern" beim Löschen von Budgets und offenen Transaktionen anzeigen
