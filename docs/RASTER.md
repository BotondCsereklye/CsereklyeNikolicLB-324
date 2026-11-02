# Abgleich mit dem Bewertungsraster M324

Stand: 26. Oktober 2026. Grundlage sind `M324_Bewertungsraster.xlsx`, Version 1.0, Blatt `Bewertungsraster`, Zeilen 8–12, und die konkrete `LB-324.docx`. Das Raster gewichtet A1 mit 20 %, B1 mit 10 %, C1 mit 30 %, D1 mit 20 % und E1 mit 20 %. Hier werden Nachweise zugeordnet; es wird keine Lehrpersonenbewertung vorweggenommen.

| Kompetenzband | Beginner und Intermediate | Zusätzlicher Advanced-Nachweis | Stand und Grenzen |
| --- | --- | --- | --- |
| A1: Anforderungen | Definition, Nutzen, Begriffe und Nachweiskette in [DEVOPS.md](DEVOPS.md); Issue-Vorlage, Labels, Issues und PR-Verknüpfungen | Vergleich GitHub Issues, Trello und Markdown einschliesslich Trellos GitHub Power-Up mit begründeter Werkzeugwahl | KI-gestützte Gegenprüfung im Auftrag Aleksandars in [ABNAHME_ALEKSANDAR.md](ABNAHME_ALEKSANDAR.md); persönliche Erläuterung durch die Lernenden bleibt erforderlich. |
| B1: Entwicklungsumgebung | Python 3.12, virtuelle Umgebung und Installation im [README](../readme.md); Black bei Commit und pytest bei Push | Eigenständige Konfiguration über `.pre-commit-config.yaml`, gepinnte Abhängigkeiten und tatsächliche Hook-Nachweise in [NACHWEISE.md](NACHWEISE.md) | Einrichtung und Nachweise vorhanden; nach einem neuen Klon beide Hook-Typen installieren. |
| C1: Sourcecode und Artefakte | Git, Mercurial und SVN sowie Abgrenzung GitHub in DEVOPS.md; Ablauf über `main`, `dev` und Feature-Branches; Issue #5, Test-/Implementierungscommits, PR #6 und erhaltener Feature-Branch | Laufzeit-ZIP mit Commit und Hashes; automatische isolierte Laufzeitprüfung; Actions-Artefakt | PR #6 und erhaltener Branch sowie erfolgreicher Release-Prüfjob live gegengeprüft. Ältere Abgabe-ZIPs und Git-Bundles wurden in dieser Prüfung nicht erneut geöffnet; Details in ABNAHME_ALEKSANDAR.md. |
| D1: Automatische Integration | Fachliche Tests zu Happiness; pre-push-Tests und CI ausschliesslich für PRs nach `dev` | `tests/test_runtime.py` und `scripts/smoke_runtime.py` prüfen das ZIP mit Gunicorn und HTTP; Negativtests erkennen falschen Commit und defekte Happiness | Automatisiert umgesetzt; erfolgreiche lokale und GitHub-Ergebnisse mit Lauf-URLs in NACHWEISE.md festhalten. |
| E1: Automatisches Deployment | Erklärung in DEVOPS.md und konkrete [Azure-Anleitung](AZURE.md); Workflow für `main` | Separater Prüf- und Deployment-Job, dasselbe ZIP und HTTP-Prüfung der Release-ID | **Offen:** kein authentifizierter Azure-Zugang und keine erfolgreiche Cloud-Auslieferung. Konfiguration allein erfüllt den praktischen Nachweis nicht; Issue #14. |

## Weitere Vorgaben der konkreten LB

| Vorgabe | Nachweis oder verbleibende Aktion |
| --- | --- |
| Ordner- und ZIP-Name | `CsereklyeBotondLB-324`, genau ein gleichnamiger Projektordner im Abgabe-ZIP. |
| Öffentliches Repository | Auf Wunsch vorerst privat; bewusst aufgeschoben. Keine Sichtbarkeitsänderung ohne neuen Auftrag. |
| Vorlage und drei Typ-Labels | `.github/ISSUE_TEMPLATE/anforderung.yml` und echte GitHub-Labels. |
| Black bei Commit, Tests bei Push | Konfiguration und ausgeführte Hooks; Anleitung im README. |
| Integrations-CI nur für PRs nach dev | `.github/workflows/ci.yml`; der getrennte Release-Workflow prüft zusätzlich auf `main` das auszuliefernde Artefakt. |
| Happiness über GitHub Flow | Issue #5, `feature/5-happiness`, PR #6 und `test_add_entry_with_happiness`. |
| Azure-App und automatische Auslieferung | Issue #14 bleibt offen, bis echte URL, Login und Release-SHA nachgewiesen sind. |
| Teamzuordnung | Beide Projektpartner und Abschlusszuständigkeiten in [TEAM.md](TEAM.md); historische Einzelbeiträge nur nach Bestätigung ergänzen. |
| Moodle-Abgabe | Repository-Link und aktualisiertes ZIP durch die Lernenden abgeben. |

Die ergänzten Unterlagen schliessen die Dokumentationslücken. Sie ersetzen weder die praktische Azure-Auslieferung noch persönliche Kompetenznachweise.

Das Kompetenzraster bewertet die fünf Bänder mit 20/10/30/20/20 Prozent. Die konkrete LB nennt daneben einen Aufgabenraster mit 33 gewichteten Punkten. Diese beiden Berechnungen werden nicht vermischt; die endgültige Bewertung und die anzuwendende Notenberechnung legt die Lehrperson fest. Die Programmierfunktion dient als Gegenstand für die geforderten Werkzeug- und Prozessnachweise.
