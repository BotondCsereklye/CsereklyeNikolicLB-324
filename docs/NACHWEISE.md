# Durchgeführte Arbeit und Nachweise

## Ausgangslage

Am 9. Oktober 2026 wurden die Modulaufträge in `M324_Aufgaben` und die konkrete `LB-324.docx` ausgewertet. Das dortige `tagebbbuch.zip` liefert den Ausgangscode. Die `.env` aus dem Archiv und die enthaltene verschachtelte Dublette wurden nicht übernommen. Alte Prüfungen oder private Projekte werden nicht verwendet.

Öffentliches Repository: https://github.com/BotondCsereklye/CsereklyeBotondLB-324

| Schritt | Tatsächlicher Nachweis |
| --- | --- |
| Ausgangsvorlage | [Issue #1](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/1), Commit `51af91a` mit Issue-Bezug |
| CI/CD-Anforderung vor Änderung | [Issue #2](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/2); Branch `feature/2-ci-cd` aus `dev` |
| Tests zuerst | Vor der Plattform-Anpassung: 4 fehlgeschlagene, 8 erfolgreiche Tests; nach Anpassung 13 erfolgreiche Tests mit 94,81 % kombinierter Statement-/Branch-Abdeckung |
| Zusätzlicher Fehlerfall | Umlaut-Passwort löste einen TypeError aus; eigener Negativtest führte zur Verwendung eines UTF-8-Bytevergleichs |
| Labels | Funktionale Anforderung, Qualitätsanforderung und Randanforderung als echte GitHub-Labels angelegt |

Weitere endgültige Prüfergebnisse, PRs und Commit-IDs werden nach den tatsächlichen Läufen ergänzt. Diese Zwischenbeschreibung behauptet noch keinen erfolgreichen Feature-Merge und kein menschliches Review.

## Offene Nachweise

- Azure-App, OIDC-Identität, Runtime-Geheimnisse und reale App-URL sind noch nicht eingerichtet/verifiziert.
- Kein erfolgreicher Azure-Deployment-Lauf und keine Azure-Anmeldeprüfung werden behauptet.
- Die manuelle Schlussprüfung und der Moodle-Upload erfolgen durch den Benutzer.
