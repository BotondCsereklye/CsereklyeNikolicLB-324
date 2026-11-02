# Abgleich mit dem Bewertungsraster M324

Grundlage: `M324_Bewertungsraster.xlsx`, Version 1.0, Blatt `Bewertungsraster`, Zeilen 8–12. Die Gewichtung beträgt 20/10/30/20/20 Prozent.

| Band | Gewicht | Vorhandene Nachweise | Noch erforderlich |
| --- | --- | --- | --- |
| A1 Anforderungen | 20 % | DevOps-Grundlagen und Begriffe in DEVOPS.md; Issue-Vorlage, Typ-Labels und Issue #5; Vergleich von GitHub Issues, Trello und Markdown mit begründeter Wahl | Begriffe und Entscheidung selbst erklären |
| B1 Umgebung | 10 % | Python 3.12, virtuelle Umgebung, gepinnte Abhängigkeiten und Hook-Anleitung im README; Konfiguration für Black bei Commit und pytest bei Push | Einrichtung auf dem eigenen Notebook nachvollziehen |
| C1 Sourcecode und Artefakte | 30 % | Git/Mercurial/SVN in DEVOPS.md; Issue #5, Feature-Branch, Commits und PR #6; Actions-Artefakt mit Commit und Hashes | Endgültiges Abgabe-ZIP aus dem finalen Stand prüfen |
| D1 Integration | 20 % | Fachliche Happiness-Tests; automatische dev-CI; ZIP mit Gunicorn und HTTP; Negativtests für falschen Commit und defekte Happiness | Aktuellen CI-Check am Abschluss-PR prüfen |
| E1 Deployment | 20 % | Erklärung, Azure-Anleitung, Workflow mit geprüftem Artefakt und HTTP-Prüfung der Release-ID | Echte Azure-Auslieferung, URL, Login und passender Release-Commit; Issue #14 |

Für Advanced verlangen A1 den Werkzeugvergleich, B1 die selbständige Einrichtung, C1 die angewendete Artefaktverwaltung, D1 den vollständigen Integrationstest und E1 den umfassenden praktischen Deploymentprozess. Die Unterlagen und Automatisierungen bilden die Grundlage; die persönliche Erklärung und praktische Durchführung gehören zur Kompetenzbewertung.

Die konkreten Tests, PRs und Actions-Läufe sind in [NACHWEISE.md](NACHWEISE.md) verlinkt.

## Konkrete LB-Aufgaben

`LB-324.docx` enthält einen separaten Aufgabenraster mit 33 gewichteten Punkten. Aufgabe 5 zählt doppelt. Er bewertet Administration, Vorlage/Labels, Hooks/Anleitung, dev-CI, Azure und GitHub Flow. Diese Punkte werden getrennt von den fünf Kompetenzbändern betrachtet.

Die [Abgabecheckliste](ABGABECHECK.md) folgt diesen konkreten Aufgaben. Die Lehrperson legt die endgültige Bewertung fest.
