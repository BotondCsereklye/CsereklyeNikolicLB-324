# Technische Gegenprüfung

## KI-Unterstützung

Codex wurde zur Prüfung von Code, Tests und Dokumentation sowie zur Überarbeitung der Unterlagen eingesetzt. Die Prüfungen vom 26. Oktober 2026 erfolgten KI-gestützt im Auftrag von Aleksandar Nikolic. Auch die Bereinigung und GitHub-Prüfung vom 2. November 2026 erfolgt mit Codex. Diese Unterstützung ist kein Nachweis einer persönlichen manuellen Abnahme durch die Projektpartner.

## Prüfung vom 26. Oktober 2026

Geprüfter Ausgangsstand: `debedb40ecbc27703bc8eb4e446ac4c25e4245f0` auf `dev`. Der damalige Bericht nennt Linux mit Python 3.12.14, eine neue virtuelle Umgebung, installierte Commit-/Push-Hooks, 24 erfolgreiche Tests und 97,62 % kombinierte Statement-/Branch-Abdeckung von `app.py`.

Ausgeführte Befehle laut Prüfprotokoll:

```bash
python -m pip install -r requirements-dev.txt
python -m pre_commit install --hook-type pre-commit --hook-type pre-push
python -m pre_commit run --all-files --hook-stage pre-commit
python -m pre_commit run --all-files --hook-stage pre-push
python -m pytest --cov=app --cov-report=term-missing
python scripts/package_release.py
python scripts/smoke_runtime.py dist/deploy.zip --expected-commit debedb40ecbc27703bc8eb4e446ac4c25e4245f0
```

| HTTP-Szenario | Damaliges Ergebnis |
| --- | --- |
| Falsches Passwort und Schreibversuch | Weiterleitung zu /login; kein Eintrag angelegt |
| Richtiges Passwort | Anmeldung erfolgreich |
| Alle drei Stimmungen | Inhalt und Stimmung nach erneutem GET korrekt |
| Fehlender oder leerer Inhalt, nur Leerzeichen | HTTP 400; keine Änderung |
| 5000 / 5001 Zeichen | 5000 akzeptiert, 5001 zurückgewiesen |
| Leere oder unbekannte Stimmung | HTTP 400 |
| HTML und Script im Inhalt | Als Text escaped |
| Logout | Einträge verborgen; Schreiben führt zum Login |
| Erneutes Login im selben Prozess | Vorhandene Einträge sichtbar |

Das ZIP wurde mit Gunicorn und HTTP geprüft. Diese Prüfung erfasst Serververhalten und HTML, keine interaktive Bildschirmdarstellung. Die Suite enthält ausserdem Negativtests für falsche Commit-Metadaten und eine defekte Happiness-Implementierung.

## GitHub-Nachweise

- [PR #18](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/18) enthält die Gegenprüfung und Dokumentationskorrekturen.
- Der [CI-Lauf 40364160076](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40364160076) zu Commit `7f9026d` bestätigt 24 bestandene Tests.
- Der [Release-Lauf 40295820919](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295820919) bestätigt ebenfalls 24 Tests, ZIP-Bau, HTTP-Prüfung und Artefakt-Upload. Sein Azure-Job wurde übersprungen.

Am 2. November wurden diese beiden Laufprotokolle, die offenen Issues, Branches und der PR erneut über GitHub geprüft. Die lokale Prüfung vom 26. Oktober und ihre Coverage-Angabe wurden dabei nicht erneut ausgeführt.

## Dokumentationskorrekturen

Der Werkzeugvergleich berücksichtigt Trellos GitHub Power-Up. Git, Mercurial und SVN werden von der Hosting-Plattform GitHub unterschieden. Der manuelle Workflow-Start auf main ist erklärt. Bewertungsraster und Aufgabenpunkte sind getrennt dargestellt.

Die Überarbeitung vom 2. November kürzt wiederholte Statusmeldungen und technische Zugriffsdetails. Die ursprünglichen Fassungen bleiben in der Git-Historie erhalten.

## Ausstehend

Die Abnahme auf der echten Azure-URL, die persönliche Schlussprüfung und die Moodle-Abgabe stehen noch aus. Details sind in [ABGABECHECK.md](ABGABECHECK.md) festgehalten.
