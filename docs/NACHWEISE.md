# Projektnachweise

## Anforderungen und Umsetzung

| Gegenstand | Anforderung | Umsetzung | Automatische Prüfung |
| --- | --- | --- | --- |
| Anforderungsverwaltung, Hooks und CI | [Issue #2](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/2) | [PR #3](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/3) nach dev | [Erfolgreicher pytest-Lauf](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37933992918) |
| Happiness | [Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5) | [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6) nach dev | [Erfolgreiche Happiness-CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37935212233) |
| HTTP-Prüfung des Laufzeit-Artefakts | [Issue #13](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/13) | [PR #15](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/15), tests/test_runtime.py und scripts/smoke_runtime.py | [Erfolgreiche dev-CI](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295594572) |
| Automatische Azure-Auslieferung | [Issue #14](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/14) | Workflow vorbereitet und derzeit gesperrt | Live-Nachweis ausstehend |

## GitHub Flow am Beispiel Happiness

Issue #5 beschreibt den Anforderungssatz und das Abnahmekriterium. Der Feature-Branch wurde aus `dev` angelegt. Test-Commit `536fb6a` liegt vor Implementierungscommit `e1fa937`. PR #6 hat die GitHub-CI bestanden und wurde mit `bd5d937` nach dev gemergt. Die Funktion wurde anschliessend nach main übernommen.

Die Nachweiskette lautet damit: **Issue → Feature-Branch → Test → Implementierung → geprüfter PR → Integration**. Der Happiness-Branch wird für die LB erhalten.

## Geprüftes Release-Artefakt

Der [Main-Lauf vom 2. November 2026](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/41464774961) bestätigt:

- 24 erfolgreiche Tests;
- Erstellung von deploy.zip mit Versions- und Commit-Metadaten;
- Start des entpackten ZIPs mit Gunicorn;
- HTTP-Prüfung von Health-Commit, falschem Passwort, Login, Happiness, Escaping und Logout;
- Aufbewahrung als Actions-Artefakt.

Der Job „Auf Azure ausliefern“ war gesperrt und wurde übersprungen. Eine laufende Azure-URL und die fachliche Live-Abnahme stehen noch aus. Details zur Prüfung: [TESTS.md](TESTS.md).
