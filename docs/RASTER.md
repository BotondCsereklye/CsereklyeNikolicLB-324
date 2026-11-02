# Nachweise zum Bewertungsraster M324

Grundlage: `M324_Bewertungsraster.xlsx`, Version 1.0, Blatt Bewertungsraster, Zeilen 8–12.

| Kompetenzband | Gewicht | Erklärung und Anwendung | Praktischer Nachweis |
| --- | --- | --- | --- |
| A1 Anforderungen | 20 % | [DEVOPS](DEVOPS.md): Definition und Nutzen von DevOps, Anforderungsbegriffe, Traceability und Vergleich von GitHub Issues, Trello und Markdown | Issue-Vorlage, drei Typ-Labels und Issue #5 mit verknüpftem PR #6 |
| B1 Entwicklungsumgebung | 10 % | [README](../readme.md): Einrichtung für Windows und Linux/macOS, Registrierung und Verwendung beider Hooks. [DEVOPS](DEVOPS.md): Alternativen, Werkzeugwahl und Erweiterung der Umgebung | Python 3.12, gepinnte Abhängigkeiten und .pre-commit-config.yaml mit Black bei Commit und pytest bei Push |
| C1 Sourcecode und Artefakte | 30 % | [DEVOPS](DEVOPS.md): Git/Mercurial/SVN, Branch-Ablauf, Paketinhalt, Commit-Zuordnung und Artefaktaufbewahrung | [NACHWEISE](NACHWEISE.md): Happiness über GitHub Flow; geprüftes ZIP als Actions-Artefakt |
| D1 Integration | 20 % | [TESTS](TESTS.md): Anforderung zu Testfall, automatische Ausführung und vollständiger HTTP-Integrationstest des ZIPs | dev-CI, drei Laufzeit-Tests einschliesslich Negativfällen sowie erfolgreicher Main-Prüfjob |
| E1 Deployment | 20 % | [AZURE](AZURE.md): Funktionsweise und Konfiguration des automatisierten Deploymentprozesses | Workflow vorhanden; Deployment gesperrt, praktische Azure-Auslieferung und Live-Abnahme noch ausstehend |

Für A1 ist der begründete Werkzeugvergleich dokumentiert. B1 verbindet die Einrichtung mit der selbständigen Anpassung von Hooks und Abhängigkeiten. C1 verknüpft Versions- und Artefaktverwaltung. D1 prüft das gebaute Artefakt mit echtem Webserver und HTTP. Für E1 ist die Vorbereitung dokumentiert; die praktische Durchführung folgt separat.

Die konkrete LB enthält daneben einen Aufgabenraster mit 33 gewichteten Punkten. Dieser wird getrennt von den fünf Kompetenzbändern betrachtet.
