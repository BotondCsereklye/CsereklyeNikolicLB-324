# DevOps und Werkzeugwahl

## A1 Anforderungen und Zusammenarbeit

DevOps verbindet Entwicklung, Qualitätssicherung und Betrieb durch gemeinsame Verantwortung und automatisierte Abläufe. Betroffen sind Planung, Implementierung, Tests, Auslieferung und Überwachung. Kurze Rückmeldungen machen Fehler früh sichtbar und verringern manuelle Übergaben. Im Projekt verbinden Issues, Git, Hooks, pytest, Actions und Azure diese Schritte.

Continuous Integration prüft Änderungen vor der Integration. Continuous Delivery hält einen geprüften Stand zur Auslieferung bereit. Continuous Deployment liefert einen solchen Stand automatisch aus. Unsere dev-CI ist aktiv; die Azure-Auslieferung ist derzeit gesperrt.

| Begriff | Bedeutung im Projekt |
| --- | --- |
| Funktionale Anforderung | Gewünschtes Verhalten, beispielsweise Stimmung beim Eintrag erfassen; Issue #5 |
| Qualitätsanforderung | Geforderte Qualität, beispielsweise automatische Tests; Issue #13 |
| Randanforderung | Technische Vorgabe, beispielsweise Azure als Laufzeitplattform; Issue #14 |
| Priorität | muss, soll oder wird beschreibt die Verbindlichkeit |
| Abnahmekriterium | Beobachtbares Ergebnis, mit dem sich eine Anforderung prüfen lässt |
| Traceability | Verknüpfung von Anforderung, Commit, Test, PR und Release |
| Definition of Done | Änderung implementiert, erfolgreich geprüft und integriert; bei Deployment zusätzlich live nachgewiesen |

Die Issue-Vorlage erfasst Zielsystem, Priorität, Systemaktivität, Ergänzungen, Funktionalität und Bedingungen. Beispiel aus Issue #5: „Das Tagebbbuch muss dem Benutzer die Möglichkeit bieten, seine Stimmung als Emoji an einem Tagebucheintrag anzugeben, wenn er einen Eintrag verfasst, falls er angemeldet ist.“ Der Anforderungstyp wird manuell über das Label zugewiesen.

### Vergleich der Anforderungswerkzeuge

| Kriterium | GitHub Issues | Trello | Markdown im Repository |
| --- | --- | --- | --- |
| Struktur | Formular, Labels und Abnahmekriterien | Karten, Listen, Labels und Checklisten | Frei gestaltete Tabellen |
| Codebezug | Direkte Verknüpfungen zu Commits, PRs und Checks | Links; GitHub Power-Up für Branches, Commits, Issues und PR-Status | Manuell gepflegte Links |
| Zusammenarbeit | Zuweisung und Diskussion an der Anforderung | Visuelles Board mit Mitgliedern | Änderungen über Git; gleichzeitige Bearbeitung kann Konflikte erzeugen |
| Pflegeaufwand | Bereits mit dem Projekt verbunden | Zusätzliches Board mit eigener Pflege | Kein zusätzlicher Dienst, aber manuelle Statuspflege |
| Eignung für die LB | Führende Aufgabenverwaltung | Sinnvoll bei Bedarf an zusätzlicher visueller Planung | Ergänzende Erklärungen und Entscheidungen |

Wir wählen GitHub Issues, weil Anforderungen und Umsetzung am selben Ort liegen. Trello bietet eine GitHub-Anbindung, würde für dieses Zweierprojekt aber zusätzliche Pflege verursachen. Markdown ergänzt die Issues um länger gültige Erklärungen.

Quellen: [Microsoft DevOps](https://learn.microsoft.com/en-us/devops/what-is-devops), [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues), [Trello GitHub Power-Up](https://support.atlassian.com/trello/docs/using-the-github-power-up/).

## B1 Entwicklungsumgebung

| Möglichkeit | Vorteil | Grenze |
| --- | --- | --- |
| Lokales Python mit venv | Projektpakete sind von anderen Python-Projekten getrennt | Python und Betriebssystem müssen passend eingerichtet sein |
| Container | Betriebssystempakete und Werkzeuge können gemeinsam beschrieben werden | Zusätzliche Laufzeit und Konfiguration |
| Entfernte Entwicklungsumgebung | Gemeinsam vorbereitete Umgebung auf einem Server | Netzwerkzugang und Serververwaltung nötig |

Wir verwenden Python 3.12 mit venv und gepinnten requirements-Dateien. Das ist für die kleine Flask-App ausreichend. Actions verwendet ebenfalls Python 3.12. Die Gunicorn-Integrationstests laufen auf Linux; unter Windows werden diese drei Tests übersprungen.

Die [Einrichtungsanleitung](../readme.md#lokal-starten) zeigt den Aufbau für Windows und Linux/macOS. Eine Erweiterung erfolgt durch Anpassung der requirements-Dateien und der Hook-Konfiguration, anschliessend werden die Tests erneut ausgeführt.

Die Hooks müssen nach jedem Klonen registriert werden, weil .git/hooks lokal ist. Black läuft beim Commit. Verändert Black eine Datei, wird sie erneut gestagt und committed. pytest läuft beim Push und blockiert diesen bei einem Fehler. Die Einstellungen haben folgende Wirkung:

- `language: system`: die aktive Python-Umgebung liefert die Werkzeuge;
- `always_run: true`: der Push-Test läuft auch ohne passende geänderte Dateien;
- `pass_filenames: false`: pytest erhält keine einzelnen Dateinamen und prüft die ganze Suite;
- `stages`: trennt Formatierung bei pre-commit von Tests bei pre-push.

Die serverseitige CI ergänzt die lokalen Hooks, da diese auf einem Notebook fehlen oder umgangen werden können.

Quellen: [Python venv](https://docs.python.org/3.12/library/venv.html), [pre-commit Hook-Stufen](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages).

## C1 Versionsverwaltung und Artefakte

| Werkzeug | Arbeitsweise | Einordnung |
| --- | --- | --- |
| Git | Verteilt; vollständige Klone enthalten die Historie und erlauben lokale Commits | Im Projekt für Feature-Branches und Integration verwendet |
| Mercurial | Ebenfalls verteilt mit lokalen Commits und Historie | Alternative, hier nicht eingesetzt |
| Subversion | Zentral; gemeinsame Historie und Commits liegen auf dem Server | Alternative für zentral organisierte Entwicklung |

GitHub hostet Git-Repositories und ergänzt Issues, Pull Requests und Actions. GitHub ist somit eine Plattform für die Zusammenarbeit; Git ist die Versionsverwaltung. Quelle: [Pro Git](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control).

### Änderungen übernehmen

1. Anforderung oder Fehler als Issue mit Abnahmekriterium erfassen.
2. `git switch dev` und `git pull --ff-only` ausführen; mit `git switch -c feature/<issue>-<thema>` einen Branch anlegen.
3. Fachlichen Test formulieren und Änderung implementieren.
4. Mit Issue-Bezug committen und pushen; lokale Hooks laufen dabei automatisch.
5. PR nach dev öffnen, CI und Änderung prüfen, danach mergen.
6. Geprüften Stand über einen Release-PR nach main übernehmen.

dev enthält die abgeschlossene Entwicklung, main den übernommenen Release-Stand. Der Ablauf ist die in der LB verlangte Anpassung des GitHub Flow. Die konkrete Happiness-Nachweiskette steht in [NACHWEISE.md](NACHWEISE.md).

### Artefaktverwaltung

Quellcode und Dokumentation liegen in Git. `scripts/package_release.py` erzeugt daraus deploy.zip mit App, Runtime-Abhängigkeiten, Templates, CSS und release.json. Die Metadaten enthalten Version, vollständige Commit-ID und SHA-256 der Laufzeitdateien; neben dem ZIP wird dessen Prüfsumme gespeichert.

Die Version 0.2.0 bezeichnet den Funktionsstand. Die Commit-ID identifiziert den genauen Quellstand; Hashes dienen der Integritätsprüfung. Geheimnisse, virtuelle Umgebung und Git-Interna gehören nicht ins Paket.

Der Main-Prüfjob startet genau dieses ZIP mit Gunicorn und prüft es über HTTP. Er speichert es als Actions-Artefakt `tagebbbuch-<Commit-ID>` für 14 Tage. Der abhängige Azure-Job würde dasselbe Artefakt desselben Laufs laden. Dadurch wird das geprüfte Paket weitergegeben und nicht vor der Auslieferung neu gebaut.

Quelle: [GitHub Actions-Artefakte](https://docs.github.com/en/actions/tutorials/store-and-share-data).

D1 mit den konkreten Testfällen: [TESTS.md](TESTS.md). E1 mit Erklärung und Konfiguration: [AZURE.md](AZURE.md).
