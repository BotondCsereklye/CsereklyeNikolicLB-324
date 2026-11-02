# Tests und Integration

Die Tests prüfen konkrete Anforderungen der Tagebuch-App. `conftest.py` leert die gemeinsame Eintragsliste vor und nach jedem Test. Die Fixture `client` ist angemeldet; `anonymous_client` ist nicht angemeldet.

## Testfälle zu Anforderungen

| Anforderung | Ausgangslage und Aktion | Erwartetes Ergebnis | Automatisierter Test |
| --- | --- | --- | --- |
| Eintrag mit Stimmung erfassen, Issue #5 | Angemeldeter Client sendet Text und 😃 an POST /add_entry | HTTP 302 nach /; gespeicherter Inhalt und Stimmung stimmen | `test_add_entry_with_happiness` in test_app.py |
| Stimmung am Eintrag anzeigen | Eintrag mit 😃 erfassen, danach GET / | Text und Stimmung stehen am dargestellten Eintrag | `test_happiness_is_displayed` |
| Bestehende Aufrufe unterstützen | Eintrag ohne happiness senden | Gespeicherte Stimmung ist 😐 | `test_existing_calls_get_neutral_mood` |
| Ungültige Stimmung zurückweisen | Unbekannten Stimmungswert senden | HTTP 400; kein Eintrag gespeichert | `test_invalid_happiness_is_rejected` |
| Schreibzugriff schützen | Nicht angemeldeter Client sendet einen Eintrag | Weiterleitung zu /login; Eintragsliste unverändert | `test_anonymous_user_cannot_add_or_read_entries` |
| Eingabegrenzen einhalten | Leeren Text oder 5001 Zeichen senden | HTTP 400; keine Speicherung | `test_blank_and_too_long_entries_are_rejected` |
| Gültige Grenze annehmen | 5000 Zeichen senden | Eintrag mit Zeitstempel gespeichert | `test_entry_limit_and_timestamp` |
| HTML als Text darstellen | Script-Tags im Eintrag speichern und Seite laden | Tags werden escaped ausgegeben | `test_content_is_escaped` |
| Login und Logout | Richtiges Passwort senden, danach Logout aufrufen | Session wird gesetzt und anschliessend entfernt | `test_correct_password_and_logout` |

Die Anforderung aus Issue #5 lässt sich als Given/When/Then ausdrücken: **Given** ein angemeldeter Client und eine leere Eintragsliste. **When** Text und 😃 an /add_entry gesendet werden. **Then** folgt der Redirect nach / und der gespeicherte Eintrag enthält beide Werte. Der vorgegebene Test prüft genau dieses Verhalten.

Quellen im Repository: [test_app.py](../test_app.py), [tests/test_happiness.py](../tests/test_happiness.py), [tests/test_platform.py](../tests/test_platform.py).

## Automatische Ausführung

Lokal startet pytest vor jedem Push. Auf GitHub startet `.github/workflows/ci.yml` ausschliesslich bei einem Pull Request nach `dev`. Der Job verwendet Python 3.12, installiert `requirements-dev.txt` und führt `python -m pytest` aus.

Ein fachlicher Fehlertest zeigt, ob eine Anforderung erfüllt ist. Ein erfolgreicher Lauf belegt nur die abgedeckten Fälle. Der PR-Check ergänzt die lokalen Hooks, weil diese auf einem Notebook fehlen oder umgangen werden können.

## Vollständiger Integrationstest des Artefakts

`scripts/package_release.py` erstellt das Laufzeit-ZIP. Anschliessend prüft `scripts/smoke_runtime.py` genau dieses ZIP:

1. In ein neues temporäres Verzeichnis entpacken.
2. Einen eigenen Gunicorn-Prozess mit einem Worker starten und auf die HTTP-Erreichbarkeit warten.
3. /health auf Status und erwartete Commit-ID prüfen.
4. Ein falsches Passwort und einen anschliessenden unerlaubten Schreibversuch prüfen.
5. Mit dem korrekten Testpasswort anmelden.
6. Einen Eintrag mit 😃 und Script-Text erfassen; gespeicherten Inhalt, zugehörige Stimmung und HTML-Escaping anhand des zurückgegebenen HTML prüfen.
7. Abmelden und prüfen, dass Einträge danach verborgen sind.
8. Testprozess und temporäre Dateien auch bei einem Fehler aufräumen.

Dieser Ablauf verbindet Paketinhalt, Python-Abhängigkeiten, Webserver, HTTP-Routen, Session und Templates. Er prüft damit mehr als einen einzelnen Funktionsaufruf im Flask-Testclient.

`tests/test_runtime.py` enthält drei Fälle: korrektes Paket akzeptieren, falsche Commit-ID ablehnen und absichtlich defekte Happiness-Implementierung erkennen. `tests/test_artifacts.py` prüft zusätzlich die Dateiliste, das ZIP und die Dateihashes. Die Gunicorn-Tests laufen auf Linux in Actions; unter Windows werden sie übersprungen.

Der Main-Workflow führt nach der Testsuite erneut eine direkte HTTP-Abnahme des gebauten Release-ZIPs aus. Erst ein erfolgreicher Prüfjob könnte an den Deployment-Job übergeben werden. Dieser bleibt derzeit ausdrücklich gesperrt.

## Nachgewiesenes Ergebnis

Der [Prüflauf vom 2. November 2026](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/41464774961) bestätigt **24 erfolgreiche Tests** und die anschliessende HTTP-Abnahme des Laufzeit-ZIPs. Die Live-Abnahme auf Azure ist davon getrennt und steht noch aus.
