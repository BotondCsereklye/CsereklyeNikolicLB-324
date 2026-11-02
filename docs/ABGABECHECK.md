# Abgabecheckliste

Prüfstand: 2. November 2026, vor der Azure-Einrichtung. Grundlage sind `LB-324.docx` und das Kompetenzraster. Diese Checkliste wird beim endgültigen Release nochmals aktualisiert.

## Vor dem Deployment

- [x] Projektname `CsereklyeBotondLB-324` entspricht dem geforderten Namensschema.
- [x] Drei Typ-Labels sind an echten Issues vorhanden: Funktionale Anforderung (#5), Qualitätsanforderung (#13), Randanforderung (#14).
- [x] Issue-Vorlage enthält Zielsystem, Priorität, Systemaktivität, Ergänzungen, Funktionalität, Bedingungen und Abnahmekriterien.
- [x] Black ist für pre-commit konfiguriert.
- [x] pytest ist für pre-push konfiguriert; ganze Suite, `always_run: true`, `pass_filenames: false`.
- [x] README enthält Installation, Registrierung und Verwendung beider Hook-Typen.
- [x] Integrations-CI startet ausschliesslich bei Pull Requests nach dev und führt pytest aus.
- [x] Happiness ist über Issue #5, Test-/Implementierungscommits und PR #6 nachvollziehbar integriert.
- [x] `feature/5-happiness` ist als vorgeschriebener Nachweis vorhanden.
- [x] Reale GitHub-Protokolle bestätigen 24 bestandene Tests und eine HTTP-Prüfung des Laufzeit-ZIPs.
- [x] Laufzeit-Paket verwendet eine feste Dateiliste; `.env`, `.venv`, Tests und Git-Interna gehören nicht zum Deployment-ZIP.
- [x] DevOps-Grundlagen, Werkzeugvergleich, Versionsverwaltung und Rasterzuordnung sind dokumentiert.
- [x] Beide Projektpartner und Abschlusszuständigkeiten sind genannt.
- [x] PR #18 nach erfolgreicher CI in dev integriert; geprüfter Stand über PR #19 nach main übernommen.
- [x] Vier vollständig integrierte Feature-Branches entfernt; main, dev und feature/5-happiness bleiben erhalten.
- [x] Einmaligen Bereinigungsworkflow nach erfolgreicher Ausführung aus dem Projekt entfernt.
- [ ] Beide Partner prüfen die Unterlagen persönlich und ergänzen ihre tatsächlichen bisherigen Beiträge.

Die Haken zur Konfiguration beruhen auf Datei- und GitHub-Prüfung. Lokale Hook-Ausführung und Coverage vom 26. Oktober sind historische Nachweise im [Prüfbericht](ABNAHME_ALEKSANDAR.md). Ein aktueller lokaler Testlauf auf beiden Notebooks ist damit nicht bestätigt.

Ergebnisse vom 2. November: [dev-CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/41463752367), [Main-Prüfung](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/41464034617) und [Branch-Bereinigung](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/41464034661) erfolgreich. Der Azure-Job war gesperrt. Abschlussänderungen werden nochmals über dev-CI und Main-Prüfung kontrolliert.

## Deployment

Der Azure-Job ist bis zur Freigabe im Workflow mit `&& false` gesperrt.

- [ ] Deployment nach Freigabe im Workflow wieder aktivieren.

- [ ] Azure App Service und OIDC-Zugang einrichten.
- [ ] `PASSWORD`, `SECRET_KEY` und `SCM_DO_BUILD_DURING_DEPLOYMENT` in Azure setzen.
- [ ] GitHub-OIDC-Secrets und `AZURE_WEBAPP_NAME` konfigurieren.
- [ ] Geprüften Release über PR von dev nach main übernehmen.
- [ ] Erfolgreichen Azure-Deployment-Job nachweisen.
- [ ] Echte App-URL im README ergänzen.
- [ ] `/health` bestätigt den erwarteten Release-Commit.
- [ ] Login mit LB-Passwort, alle drei Stimmungen und Logout auf der echten URL prüfen.
- [ ] Datum, Release-Commit und Actions-Lauf in NACHWEISE.md ergänzen; Issue #14 erst dann schliessen.

## Endgültige Abgabe

- [ ] Öffentliche Sichtbarkeit gemäss LB herstellen oder abweichende Freigabe der Lehrperson festhalten. Aktuell ist das Repository privat.
- [ ] Finales `CsereklyeBotondLB-324.zip` mit genau einem gleichnamigen Projektordner erstellen.
- [ ] Archiv öffnen und Code, Tests, README und Dokumentation auf Vollständigkeit prüfen.
- [ ] Keine `.env`, lokalen Zugangsdaten, `.venv` oder `.git` im Archiv.
- [ ] Archivstand und finalen main-Commit abgleichen.
- [ ] Repository-URL auf Moodle abgeben.
- [ ] Projektarchiv auf Moodle hochladen und Upload kontrollieren.
- [ ] Die Löschvorgabe der LB erst nach tatsächlichem Abschluss und Upload persönlich umsetzen.

Bewertung der konkreten LB: 33 gewichtete Punkte, Aufgabe 5 doppelt. Die Gewichtung der fünf Kompetenzbänder steht separat in [RASTER.md](RASTER.md).
