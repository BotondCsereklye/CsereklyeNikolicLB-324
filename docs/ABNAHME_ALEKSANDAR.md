# Gegenprüfung im Auftrag von Aleksandar Nikolic

Datum: 26. Oktober 2026, Europe/Zurich. Projektpartner: Aleksandar Nikolic und Botond Csereklye. Bezug: [Issue #17](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/17).

Die Prüfungen wurden durch Codex mit KI-Unterstützung im Auftrag Aleksandars tatsächlich ausgeführt. Sie sind keine Bestätigung einer persönlichen manuellen Prüfung oder bereits erklärter Kompetenzen. Botonds bisherige Implementierung und ältere gemeinsame Projektergebnisse werden dadurch nicht Aleksandar zugeschrieben.

## Geprüfter Stand und Arbeitsweise

Ausgangspunkt ist der aktuelle `dev`-Commit **`debedb40ecbc27703bc8eb4e446ac4c25e4245f0`**, Dateibaum `2240ca3b33a497bf66c13a15b696ba1f0dea730d`. Vor den Änderungen wurden README, TEAM, DEVOPS, RASTER und NACHWEISE gelesen und Quellcode, Tests und Workflows geprüft. Der eigene Branch `feature/17-aleksandar-abnahme` wurde nach Issue #17 aus diesem Stand erstellt. `dev` und `main` werden nicht direkt geändert; der Feature-Branch bleibt erhalten.

Ein direkter HTTPS-Klon scheiterte an fehlender Git-Authentifizierung in dieser Umgebung. Über die authentifizierte GitHub-Verbindung wurden alle 35 versionierten Dateien desselben Commits bezogen. Der lokale Git-Dateibaum und das rekonstruierte originale Commit-Objekt stimmen per Git-Hash mit den obigen IDs überein. Das ist ein flacher Arbeitsstand, kein vollständiger Historienklon. Es lagen hier keine fremden lokalen Änderungen vor. Vorhandene Remote-Branches bleiben unverändert.

Die GitHub-Verbindung gehört zum Profil `AleksZyro` mit Schreibzugriff. Die lokale Identität wurde anhand dieses Profils auf Aleksandar gesetzt, statt die globale Vorgabe `Codex` zu verwenden. Es werden keine KI-Coauthor-Trailer hinzugefügt. Die Veröffentlichung der Änderungen erfolgt über die authentifizierte GitHub-Verbindung; deren API-Aufrufe lösen keine lokalen Git-Hooks aus. Die Hook-Stufen wurden deshalb zusätzlich ausdrücklich ausgeführt.

## Verwendete Modulunterlagen

| Datei | Relevanz für die Abgabe |
| --- | --- |
| LB-324.docx | Verbindliche konkrete Aufgaben: Issues/Vorlage, Hooks, dev-CI, Azure und Happiness über GitHub Flow. Die Programmierarbeit selbst wird laut LB nicht bewertet. |
| Die drei M324_Bewertungsraster-Dateien | Bytegleich, SHA-256 `851f7f3fece83e3ed6012f7314966dea80a25ab6b4e8730a1562f4c952d489fd`. Fünf Kompetenzbänder, Gewichtung 20/10/30/20/20 Prozent. |
| tagebbbuch.zip | Passende Ausgangsvorlage mit Flask, Eintragsliste und Happiness-Test als Erweiterung. Die verschachtelte Dublette ist kein zusätzlicher Auftrag; enthaltene Zugangsdaten werden nicht übernommen. |
| LA_324_1640_Musterloesung.docx | Relevante Erklärung lokaler Hooks und ihrer Grenzen; die LB verlangt abweichend Tests beim Push und CI für PRs nach dev. Die Label-Automatik der Übung wird nicht verlangt. |
| LA_324_1601_Musterloesung.docx | Hilfreich für Flask, Templates und Aufgabenteilung der Beispieldateien; kein zusätzlicher Funktionsauftrag. |
| LA_324_1650_Musterloesung.docx | SQLite-Lernbeispiel; eine Datenbank wird für diese Tagebbbuch-LB nicht zusätzlich verlangt. |
| Stateless-ZIP und test_helper.py | To-do-Beispiele mit Datum/Sortierung. Keine Happiness-Abnahmetests für diese Anwendung; deshalb nicht in die Suite kopiert. |

## Tatsächlich ausgeführte Prüfungen

Umgebung: Linux, Python 3.12.14, neue `.venv`, vollständige Installation von `requirements-dev.txt`. Ein lokales zufälliges Passwort und ein Schlüssel liegen ausschliesslich in der ignorierten `.env`.

```bash
python -m pip install -r requirements-dev.txt
python -m pre_commit install --hook-type pre-commit --hook-type pre-push
python -m pre_commit run --all-files --hook-stage pre-commit
python -m pre_commit run --all-files --hook-stage pre-push
python -m pytest --cov=app --cov-report=term-missing
python scripts/package_release.py
python scripts/smoke_runtime.py dist/deploy.zip --expected-commit debedb40ecbc27703bc8eb4e446ac4c25e4245f0
```

Beide Hook-Dateien wurden installiert. Black und die vollständige pre-push-Prüfung bestanden. Die Coverage-Ausführung ergab **24 bestandene Tests und 97,62 % kombinierte Statement-/Branch-Abdeckung von app.py**. Die nicht ausgeführte Zeile 30 betrifft den Startfehler bei fehlendem Azure-Session-Schlüssel; die Abdeckung ist keine vollständige Azure-Abnahme.

Das gebaute ZIP wurde getrennt entpackt und mit einem echten Gunicorn-Prozess über HTTP geprüft. Version `0.2.0` und die vollständige Commit-ID stimmten überein. Die bestehende Suite prüft zusätzlich, dass falsche Release-Metadaten und absichtlich defekte Happiness erkannt werden und der Testserver beendet wird. Die ZIP-Allowlist und die Dateihashes bestanden ihre Prüfung.

Eine zusätzliche HTTP-Prüfung mit Cookie-Sitzung lief gegen einen separat gestarteten Gunicorn-Prozess aus dem unveränderten ZIP:

| Szenario | Beobachtetes Ergebnis |
| --- | --- |
| Falsches Passwort und anschliessender Schreibversuch | Weiterleitung zu `/login`; nach richtigem Login kein unerlaubter Eintrag vorhanden. |
| Richtiges Passwort | Anmeldung und Anzeige der Eintragsseite erfolgreich. |
| 😃, 😐 und 😞 | Je ein Eintrag gespeichert; Inhalt und Stimmung am jeweiligen Eintrag nach erneutem GET korrekt. |
| Inhalt fehlt, ist leer oder besteht nur aus Leerzeichen | HTTP 400; Eintragsliste unverändert. |
| 5001 Zeichen | HTTP 400; kein neuer Eintrag. |
| 5000 Zeichen | Erfolgreich gespeichert und vollständig angezeigt. |
| Leere oder unbekannte Stimmung | HTTP 400; kein neuer Eintrag. |
| Script- und HTML-Tags im Inhalt | Escaped als Text dargestellt; keine unverpackten Script-Tags im HTML. |
| Logout | Einträge unsichtbar; erneutes Schreiben wird zum Login umgeleitet. |
| Erneutes Login | Vorherige Einträge unverändert vorhanden, solange derselbe Prozess läuft. |

Die HTTP-Prüfung wurde ohne interaktiven Browser ausgeführt. Sie bestätigt Serververhalten und erzeugtes HTML, keine manuell geprüfte Bildschirmdarstellung. Testprozesse und temporäre Laufzeitverzeichnisse wurden danach beendet bzw. entfernt.

## Fachliche Gegenprüfung und Korrekturen

Es wurde in den verlangten Anwendungsszenarien kein funktionaler Fehler nachgewiesen. Deshalb wurden weder App-Funktionen geändert noch zusätzliche Anforderungen oder Regressionstests erfunden.

Korrigiert wurden fachliche Dokumentationslücken: Der Werkzeugvergleich berücksichtigt jetzt Trellos GitHub Power-Up. Für C1/LZ 3.1 werden Git, Mercurial und SVN unterschieden und GitHub als Hosting-Plattform eingeordnet. Das README benennt sowohl den automatischen als auch den manuellen Workflow-Start auf main. TEAM kennt nun das verifizierte Konto `AleksZyro`. Raster- und Aufgabenbewertung werden getrennt erklärt. Grundlage sind die jeweils in DEVOPS.md und README verlinkten Herstellerquellen und das hochgeladene Raster.

Die Nachweise wurden mit echten GitHub-Daten gegengeprüft:

- Die drei verlangten Typ-Labels sind tatsächlich an Issues #5, #13 und #14 vorhanden; die Issue-Vorlage enthält die verlangten Felder.
- [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6) wurde nach `dev` gemergt; `feature/5-happiness` besteht noch und zeigt auf `e1fa937cb0f998631a5830acd933a650be3dd70c`.
- Die dev-CI-Läufe [40295449518](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295449518) und [40295594572](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295594572) melden einen erfolgreichen pytest-Job.
- Im [Release-Lauf 40295820919](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/actions/runs/40295820919) bestanden Test, ZIP-Bau, HTTP-Prüfung und Artefakt-Upload. Der Job „Auf Azure ausliefern“ wurde übersprungen. Dieser Lauf belegt keine Cloud-Auslieferung.

Ältere lokale Screenshots, die behauptete damalige Hook-Blockierung und frühere Abgabe-ZIPs/Git-Bundles wurden nicht erneut beobachtet oder geöffnet. Sie bleiben historische Angaben in NACHWEISE.md. Die hier neu ausgeführten Prüfungen stehen separat und ersetzen diese Vorgeschichte nicht.

## Veröffentlichung und offene Punkte

Der eigene PR nach `dev` und sein tatsächliches CI-Ergebnis werden nach der Veröffentlichung ergänzt. Ein Merge ist nicht Teil dieser Abnahme.

Die Azure-Abnahme bleibt in [Issue #14](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/14) offen: README und Issue enthalten noch keine reale App-URL oder Zugangsmöglichkeit. Sobald Botond bereitgestellt hat, sind auf dieser URL Login, alle Stimmungen, Logout und `/health` gegen den tatsächlichen Release-Commit zu prüfen. Die Azure-Konfiguration wird hier nicht übernommen.

Das Repository bleibt privat. Damit ist die öffentliche Sichtbarkeit der konkreten LB weiterhin nicht erfüllt; der Zugang der Lehrperson muss vor der Abgabe geklärt sein. Moodle-Upload, endgültiges Abgabe-ZIP und persönliche Erläuterung der Kompetenzen stehen noch aus. Es wurde keine Note vergeben.
