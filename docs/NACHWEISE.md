# Durchgeführte Arbeit und Nachweise

## Ausgangslage

Am 9. Oktober 2026 wurden die Modulaufträge in `M324_Aufgaben` und die konkrete `LB-324.docx` ausgewertet. Das dortige `tagebbbuch.zip` liefert den Ausgangscode. Die `.env` aus dem Archiv und die enthaltene verschachtelte Dublette wurden nicht übernommen. Alte Prüfungen oder private Projekte werden nicht verwendet.

Repository: https://github.com/BotondCsereklye/CsereklyeBotondLB-324. Es wurde öffentlich angelegt, ist bei der Schlussprüfung am 9. Oktober 2026 jedoch privat. Die GitHub-API meldet `disabled: false`; die Anforderung „öffentlich“ ist aktuell nicht erfüllt.

| Schritt | Tatsächlicher Nachweis |
| --- | --- |
| Ausgangsvorlage | [Issue #1](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/1), Commit `51af91a` mit Issue-Bezug |
| CI/CD-Anforderung vor Änderung | [Issue #2](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/2); Branch `feature/2-ci-cd` aus `dev` |
| Tests zuerst | Vor der Plattform-Anpassung: 4 fehlgeschlagene, 8 erfolgreiche Tests; nach Anpassung 13 erfolgreiche Tests mit 94,81 % kombinierter Statement-/Branch-Abdeckung |
| Zusätzlicher Fehlerfall | Umlaut-Passwort löste einen TypeError aus; eigener Negativtest führte zur Verwendung eines UTF-8-Bytevergleichs |
| Labels | Funktionale Anforderung, Qualitätsanforderung und Randanforderung als echte GitHub-Labels angelegt |

## Happiness über GitHub Flow

1. [Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5) wurde vor der Änderung angelegt, mit dem Typ „Funktionale Anforderung“ und den Abnahmekriterien der LB.
2. `feature/5-happiness` wurde aus `dev` erstellt. `dev` stand dabei auf `40aacaa`, dem geprüften Merge der CI/CD-Einrichtung.
3. Der vorgegebene Test und drei ergänzende Tests wurden zuerst geschrieben. Alle vier scheiterten vor der Implementierung.
4. Der tatsächliche Commit-Hook formatierte die beiden Testdateien automatisch und stoppte den ersten Commitversuch. Nach erneutem Staging entstand Commit `536fb6a` mit Bezug zu #5.
5. Ein tatsächlicher Push dieses Test-Commits wurde vom pre-push-Hook verhindert: 4 fehlgeschlagene und 17 erfolgreiche Tests; der fehlerhafte Stand wurde nicht als Remote-Branch veröffentlicht.
6. Erst danach wurde `Entry.happiness` ergänzt, das Formular erweitert und die Stimmung am Eintrag dargestellt. Fehlende Werte bleiben für bestehende Aufrufe neutral; ungültige Werte werden abgelehnt. Die Version steigt von 0.1.0 auf 0.2.0.

7. [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6) zielte auf `dev` und bestand die echte GitHub-CI: [Lauf 37935212233](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37935212233). Danach wurde er mit Merge-Commit `bd5d937` übernommen. Der Feature-Branch bleibt lokal und auf GitHub vorhanden.
8. Issue #5 wurde nach dem erfolgreichen Merge nach `dev` manuell als erledigt geschlossen. GitHubs `Closes`-Automatik schliesst Issues erst beim Merge auf den Standardast `main`; deshalb wird die manuelle Schliessung hier ausdrücklich angegeben.

## Abschlussprüfungen

| Prüfung | Ergebnis |
| --- | --- |
| Gesamte lokale Testsuite | 21 Tests erfolgreich; inklusive des in der LB vorgegebenen Happiness-Tests |
| Coverage der Anwendung | 97,62 % kombinierte Statement-/Branch-Abdeckung; Mindestwert 80 % durch Konfiguration geprüft |
| Formatierung beim Commit | Tatsächlich automatisch ausgeführt und Dateien verändert; danach erfolgreich erneut committed |
| Tests beim Push | Fehlerhafter Stand tatsächlich blockiert; korrigierter Stand anschliessend erfolgreich gepusht |
| Plattform-CI | [PR #3](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/3), [erfolgreicher Lauf 37933992918](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37933992918), Merge nach dev `40aacaa` |
| Infrastruktur auf Standardast | [PR #4](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/4), Merge `bc8773e`; kein Azure-Erfolg damit behauptet |
| Funktionsstand auf Standardast | Während der Schlussprüfung wurde [PR #8](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/8) von `feature/7-abgabenachweise` nach `main` gemergt (`88f71a9`). Damit liegt Happiness auch auf main; [Azure-Lauf 37936394976](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37936394976) ist **übersprungen**, nicht erfolgreich ausgeliefert. |
| Schlussdokumentation auf dev | [PR #9](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/9), erfolgreicher [pytest-Lauf 37936403673](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/37936403673), Merge `dee4358` |
| Branch-Schutz | `dev` verlangt PR und erfolgreichen `pytest`-Check; `main` verlangt PR; Regeln gelten auch für Administratoren; automatische Branch-Löschung ausgeschaltet |
| Browser auf Desktop | Isoliertes Chrome-Fenster mit Playwright, 1280 × 900: falsches/richtiges Passwort, Eintrag mit 😃, Neuladen und Logout erfolgreich; Screenshot visuell geprüft |
| Browser in Mobilansicht | Isolierter Browser-Kontext, 390 × 844: derselbe Ablauf erfolgreich; kein horizontaler Überlauf; Screenshot visuell geprüft. Kein physisches Mobilgerät behauptet. |
| Gebautes Laufzeit-ZIP | In getrennten Ordner entpackt und mit echtem Gunicorn-Prozess gestartet. Version 0.2.0 und Commit `bd5d937` über HTTP bestätigt; Login, Stimmung, Escaping und Logout erfolgreich. |
| Geheimnisse | Lokale `.env` ist ignoriert und unversioniert; Laufzeit-ZIP enthält nur die feste Allowlist aus `package_release.py` |

Die abschliessende Dokumentation gehört zu [Issue #7](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/7). Der erste Push von `feature/7-abgabenachweise` wurde mit „Your repository is disabled“ und HTTP 403 abgewiesen, obwohl die anschliessende API-Abfrage `disabled: false` und Administrator-/Push-Rechte meldete. Die Ursache ist nicht bestätigt. Der erneute Push war erfolgreich, einschliesslich des Test-Hooks. Die Schlussdokumentation ist lokal und auf GitHub vorhanden. Ein fremdes oder menschliches Review wurde nicht durchgeführt.

## Offene Nachweise

- Öffentliche GitHub-Sichtbarkeit steht aus; der Benutzer wurde zur beabsichtigten Änderung auf privat gefragt.
- Azure-App, OIDC-Identität, Runtime-Geheimnisse und reale App-URL sind noch nicht eingerichtet/verifiziert.
- Kein erfolgreicher Azure-Deployment-Lauf und keine Azure-Anmeldeprüfung werden behauptet.
- Die manuelle Schlussprüfung und der Moodle-Upload erfolgen durch den Benutzer.
