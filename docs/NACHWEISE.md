# Nachweise

Die technische Gegenprüfung ist im [Prüfbericht](ABNAHME_ALEKSANDAR.md) dokumentiert. Die folgende Übersicht verbindet Anforderungen mit Umsetzung und automatisierten Prüfungen.

## Anforderungen und Umsetzung

| Arbeit | Issue | Umsetzung und Nachweis |
| --- | --- | --- |
| Ausgangsvorlage | #1 | Commit `51af91a` |
| Issue-Vorlage, Labels, Hooks und CI | #2 | [PR #3](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/3), Merge nach dev `40aacaa`; [CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37933992918) erfolgreich |
| Happiness | #5 | [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6), Merge `bd5d937`; [CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37935212233) erfolgreich |
| Frühere Abgabeunterlagen | #7 | PRs #9 bis #11; [dev-CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37936653040) erfolgreich |
| Grundlagen und Teamaufteilung | #12 | [PR #15](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/15) |
| HTTP-Prüfung des Laufzeit-ZIPs | #13 | PR #15, `tests/test_runtime.py` und `scripts/smoke_runtime.py` |
| Gegenprüfung und Abschlussunterlagen | #17 | [PR #18](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/18) |
| Echte Azure-Auslieferung | #14 | Offen |

## Happiness über GitHub Flow

Die Anforderung steht in [Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5). Der Branch `feature/5-happiness` stammt aus dem damaligen dev-Stand `40aacaa`. Test-Commit `536fb6a` liegt vor Implementierungscommit `e1fa937`. PR #6 wurde nach erfolgreicher CI in dev übernommen. Der Branch bleibt gemäss LB erhalten.

Das damalige lokale Protokoll beschreibt vier zunächst fehlgeschlagene Happiness-Tests und einen durch pytest blockierten Push. Nach der Umsetzung bestanden 21 Tests. Diese lokalen Hook-Ereignisse sind historische Angaben; die verlinkte GitHub-CI belegt den erfolgreichen integrierten Stand.

## Automatisierte Prüfung und Artefakt

Im [Release-Lauf vom 26. Oktober](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295820919) wurden für Commit `a30dbaa95720acd087e9f71776de18ff2d8b03df` folgende Schritte erfolgreich ausgeführt:

- 24 Tests;
- Laufzeit-ZIP mit Version, Commit-ID und Dateihashes;
- Start genau dieses ZIPs mit Gunicorn;
- HTTP-Prüfung von Health-Commit, falschem Passwort, Login, Happiness, Escaping und Logout;
- Upload als `tagebbbuch-a30dbaa95720acd087e9f71776de18ff2d8b03df`.

Der Job „Auf Azure ausliefern“ wurde wegen fehlender `AZURE_WEBAPP_NAME` übersprungen.

[CI-Lauf 40364160076](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40364160076) zu PR #18 bestätigt weitere 24 bestandene Tests. Beide Protokolle wurden am 2. November 2026 erneut gelesen. Spätere Dokumentationsänderungen werden durch den jeweils aktuellen Check an PR #18 geprüft.

## Frühere lokale Prüfungen

Der Bericht vom 9. Oktober nennt erfolgreiche Desktop-/Mobilansicht-Prüfungen, ausgeführte Hooks und ein separat gestartetes Laufzeit-ZIP. Der Bericht vom 26. Oktober nennt 97,62 % kombinierte Statement-/Branch-Abdeckung von app.py. Diese Ergebnisse gehören zu den damaligen Ständen. Die historischen Detailfassungen stehen in der Git-Historie dieser Datei.

## Noch offen

Azure-URL, erfolgreiche Auslieferung und fachliche Live-Abnahme werden in [Issue #14](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/14) ergänzt. Repository-Sichtbarkeit, endgültiges Abgabe-ZIP und Moodle-Upload stehen in [ABGABECHECK.md](ABGABECHECK.md).
