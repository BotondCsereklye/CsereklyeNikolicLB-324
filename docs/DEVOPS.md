# DevOps und Werkzeugwahl

## Zweck und betroffene Bereiche

DevOps verbindet Entwicklung, Qualitätssicherung und Betrieb durch gemeinsame Verantwortung, kurze Rückmeldungen und automatisierte Abläufe. Es betrifft Planung, Implementierung, Test, Auslieferung und Überwachung. Im Tagebbbuch werden diese Schritte durch Issues, Git, Hooks, pytest, GitHub Actions und Azure verbunden. Fehler werden vor der Integration sichtbar; ein Release lässt sich einem geprüften Commit zuordnen. Grundlage: [Microsoft: What is DevOps?](https://learn.microsoft.com/en-us/devops/what-is-devops).

Continuous Integration (CI) prüft Änderungen automatisch vor ihrer Integration. Hier testet ein Pull Request nach `dev` die Anwendung einschliesslich des gebauten ZIPs. Continuous Delivery stellt einen geprüften Stand zur Auslieferung bereit. Continuous Deployment liefert ihn ohne weiteren manuellen Freigabeschritt aus. Der Azure-Workflow ist für automatische Auslieferung nach `main` vorbereitet; eine reale Cloud-Auslieferung bleibt bis zur Konfiguration offen.

Black formatiert beim Commit, pytest prüft vor dem Push. Serverseitige CI prüft auch dann, wenn lokale Hooks fehlen. Die Branch-Regeln verlangen einen PR und auf `dev` einen erfolgreichen `pytest`-Check. Ein Review durch eine zweite Person ist erst nach deren tatsächlicher Prüfung nachgewiesen.

## Anforderungen und nachvollziehbare Entwicklung

| Begriff | Bedeutung und Umsetzung |
| --- | --- |
| Funktionale Anforderung | Beschreibt ein Verhalten, etwa eine Stimmung beim Eintrag zu speichern; Issue #5. |
| Qualitätsanforderung | Beschreibt eine messbare Qualität, etwa automatische Prüfungen; Issues #2 und #13. |
| Randanforderung | Gibt technische oder organisatorische Grenzen vor, etwa Azure als Ziel; Issue #14. |
| Priorität | `muss`, `soll` oder `wird` in der Vorlage; kein Ersatz für den Anforderungstyp. |
| Abnahmekriterium | Prüft eine Anforderung mit Ausgangslage, Aktion und erwartetem Ergebnis. |
| Traceability | Verbindet Anforderung, Commit, Test, PR und Release. |
| Definition of Done | Implementiert, Tests erfolgreich, PR geprüft und integriert; bei Deployment-Anforderungen zusätzlich echte URL und Release-Commit nachgewiesen. |

Beispiel: „Das Tagebbbuch muss dem Benutzer die Möglichkeit bieten, seine Stimmung anzugeben, wenn er einen Eintrag verfasst, falls er angemeldet ist.“ Die Vorlage erfasst Zielsystem, Priorität, Systemaktivität, Ergänzungen, Funktionalität und Bedingungen. Das passende Typ-Label wird manuell gesetzt.

Die Nachweiskette für Happiness ist [Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5) → `feature/5-happiness` → Test-Commit `536fb6a` → Implementierung `e1fa937` → [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6) mit erfolgreicher CI → Merge `bd5d937` nach `dev`. Der Feature-Branch bleibt erhalten. Der zugehörige Test ist `test_add_entry_with_happiness` in `test_app.py`.

## Vergleich der Anforderungswerkzeuge

Für diese LB zählen die Verknüpfung mit Code und Tests, eine verständliche Aufgabenaufteilung und geringer Pflegeaufwand. Diese Eignungsbeurteilung bezieht sich auf unser Zweierprojekt.

| Kriterium | GitHub Issues | Trello | Markdown im Repository |
| --- | --- | --- | --- |
| Struktur | Issue-Formular, Labels und Abnahmekriterien | Karten, Listen, Labels und Checklisten | Frei gestaltete Tabellen und Checklisten |
| Nachvollziehbarkeit | Referenzen in Commits und PRs mit automatischen Verknüpfungen | Repository- und PR-Links müssen an der Karte gepflegt werden | Links und Status im Text; Änderungshistorie in Git |
| Zuständigkeiten | Zuweisung an berechtigte GitHub-Konten; Namen zusätzlich im Text | Mitglieder und Checklisten auf Karten | Namen im Text |
| Zusammenarbeit | Diskussion neben Anforderung und Codeänderung | Visuelle Übersicht über den Arbeitsstand | Einfach für wenige Aufgaben; parallele Änderungen können Git-Konflikte erzeugen |
| Aufwand für diese LB | Bereits mit Repository, PRs und CI verbunden | Zusätzliches Board und Abgleich mit GitHub | Kein weiterer Dienst, aber manuelle Statuspflege |
| Eignung | Führende Aufgabenverwaltung | Zusätzliche visuelle Planung bei Bedarf | Ergänzende Entscheidungen und Checklisten |

Wir verwenden GitHub Issues als führende Aufgabenverwaltung. Anforderungen, PRs und Actions am selben Ort verkürzen die Nachweiskette. Markdown dokumentiert Entscheidungen und Prüfungen. Ein zusätzliches Trello-Board bringt für die vorliegende LB keinen ausreichenden Nutzen, um die doppelte Statuspflege zu rechtfertigen.

Die Funktionsbeschreibungen stützen sich auf [GitHub: About issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues) und [Atlassian: Add and customize cards and lists](https://support.atlassian.com/trello/docs/add-and-customize-cards-and-lists/). Die projektspezifische Eignungsbewertung ist unsere daraus abgeleitete Beurteilung. Es wurden keine zusätzlichen Dienste eingerichtet.

## Umgebung, Versionen und Artefakte

Eine virtuelle Python-Umgebung trennt Projektabhängigkeiten vom Betriebssystem. Die gepinnten Dateien `requirements.txt` und `requirements-dev.txt` halten Laufzeit und Entwicklung reproduzierbar. Ein Container wäre eine weitere Möglichkeit zur Isolation; für den vorgegebenen Python App Service genügt hier die virtuelle Umgebung mit demselben Python 3.12 wie in Actions.

Git versioniert Quellcode und Dokumentation. `main` enthält den Release-Stand, `dev` geprüfte Integration und ein Feature-Branch die konkrete Änderung. Die Version `0.2.0` bezeichnet den Funktionsstand; die vollständige Git-Commit-ID identifiziert den genauen Quellstand.

`deploy.zip` enthält nur freigegebene Laufzeitdateien und `release.json` mit Version, Commit und Dateihashes. Der Release-Job prüft genau dieses ZIP mit Gunicorn und HTTP und speichert es als Actions-Artefakt `tagebbbuch-<Commit-ID>` für 14 Tage. Der Azure-Job lädt dasselbe Artefakt desselben Laufs. Das Abgabe-ZIP enthält zusätzlich Tests und Dokumentation; das Git-Bundle sichert Branches und Historie. `.env`, `.venv` und Git-Interna gehören nicht ins Abgabe-ZIP.

## Deployment und Betrieb

GitHub Actions meldet sich nach der Konfiguration über OIDC bei Azure an. `PASSWORD` und `SECRET_KEY` gehören in die Runtime-Einstellungen des App Service. Nach dem Deploy prüft `/health` den erwarteten Commit. Login und Happiness auf der echten Azure-URL ergänzen diese technische Prüfung. Eine lokale ZIP-Prüfung belegt keine Azure-Auslieferung.

Bei einem fehlerhaften Release wird der betreffende Commit mit `git revert` in einem neuen Feature-Branch rückgängig gemacht, per PR nach `dev` geprüft und anschliessend nach `main` übernommen. Die Historie bleibt erhalten. Demo-Einträge liegen im Arbeitsspeicher und gehen bei Neustart oder Deployment verloren. Deshalb ist genau ein Gunicorn-Worker vorgesehen.

Konkrete Nachweise: [NACHWEISE.md](NACHWEISE.md). Rasterabgleich: [RASTER.md](RASTER.md). Zuständigkeiten: [TEAM.md](TEAM.md).
