# CsereklyeBotondLB-324

Leistungsbeurteilung M324 DevOps von **Botond Csereklye und Aleksandar Nikolic**. Ausgangspunkt ist die Tagebbbuch-Vorlage aus dem Modul. Die Aufgaben stehen in `LB-324.docx`.

## Stand und Orientierung

- `dev` enthält den geprüften Entwicklungsstand.
- `main` enthält den aktuellen Abgabestand. Der Azure-Deployment-Job ist bis zur Freigabe gesperrt.
- `feature/5-happiness` bleibt als vorgeschriebener Nachweis der Funktionsänderung erhalten.
- Azure-URL und erfolgreiche Cloud-Auslieferung stehen noch aus: [Issue #14](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/14).
- Das Repository ist privat. Die LB verlangt ein öffentliches Repository; diese Abgabevorgabe ist noch offen.

| Unterlage | Inhalt |
| --- | --- |
| [DEVOPS](docs/DEVOPS.md) | Grundlagen, Werkzeugvergleich und Entscheidungen |
| [RASTER](docs/RASTER.md) | Zuordnung der fünf Kompetenzbänder |
| [NACHWEISE](docs/NACHWEISE.md) | Issues, PRs, Tests und Artefakte |
| [TESTS](docs/TESTS.md) | Testfälle und vollständiger Integrationstest |

## Lokal starten

Voraussetzungen: Git und Python 3.12. Zuerst das Repository klonen und in den Entwicklungsast wechseln:

```bash
git clone https://github.com/BotondCsereklye/CsereklyeBotondLB-324.git
cd CsereklyeBotondLB-324
git switch dev
```

macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
```

Windows/PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

In `.env` ein lokales Passwort und einen zufälligen `SECRET_KEY` eintragen. Einen Schlüssel erzeugt `python -c "import secrets; print(secrets.token_hex(32))"`. Die Datei ist in Git ausgeschlossen.

```bash
python -m flask --app app run
```

Die App läuft auf http://127.0.0.1:5000. Einträge liegen wie in der Vorlage im Arbeitsspeicher. Ein Neustart löscht sie. Für Gunicorn auf Linux/macOS deshalb genau einen Worker verwenden:

```bash
python -m gunicorn --workers 1 --bind 127.0.0.1:5000 app:app
```

## Aufgabe 1 Anforderungen

Das Issue-Formular **Anforderung** erfasst Zielsystem, Priorität (`muss/soll/wird`), Systemaktivität, Ergänzungen, Funktionalität, Bedingungen und Abnahmekriterien. Die Typ-Labels **Funktionale Anforderung**, **Qualitätsanforderung** und **Randanforderung** werden manuell zugewiesen.

Vor jeder Codeänderung wird eine Issue angelegt. Branch, Commits und PR verweisen darauf. [Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5) zeigt dies für Happiness.

## Aufgabe 2 Hooks

Nach jedem Klonen die virtuelle Umgebung aktivieren und beide Hook-Typen installieren:

```bash
python -m pre_commit install --hook-type pre-commit --hook-type pre-push
```

| Zeitpunkt | Befehl | Wirkung |
| --- | --- | --- |
| Commit | `python -m black` | Formatiert geänderte Python-Dateien. Bei Änderungen erneut stagen und committen. |
| Push | `python -m pytest` | Prüft bei jedem Push die ganze Suite. Fehler verhindern den Push. |

Die Hooks verwenden `language: system`; die virtuelle Umgebung muss aktiv sein. Manuelle Prüfung:

```bash
python -m pre_commit run --all-files --hook-stage pre-commit
python -m pre_commit run --all-files --hook-stage pre-push
python -m pytest --cov=app --cov-report=term-missing
```

## Aufgabe 3 Integration

`.github/workflows/ci.yml` startet ausschliesslich bei Pull Requests nach `dev` und führt pytest aus. Die Suite prüft auch das gebaute ZIP: Gunicorn startet es separat, anschliessend werden Login, Happiness und Logout über HTTP geprüft. Negativtests erkennen falsche Commit-Metadaten und eine defekte Stimmung.

Ablauf: Issue → Feature-Branch aus `dev` → Commit und Push → PR nach `dev` → erfolgreiche CI → Merge. Geprüfte Änderungen werden anschliessend über einen PR von `dev` nach `main` übernommen. Die Auslieferung bleibt bis zur Freigabe pausiert.

## Aufgabe 4 Azure

**Pausiert bis zur Freigabe:** Der Deployment-Job ist im Workflow durch `&& false` gesperrt. Tests und Artefaktbau dürfen auf main laufen. Noch offen sind laufende App, URL und erfolgreicher Deployment-Nachweis.

Der Workflow `deploy-azure.yml` startet bei Pushes nach `main` und zusätzlich manuell. Seine Jobs laufen nur auf `main`. Zuerst werden Tests und das Laufzeit-ZIP geprüft. Der Deployment-Job übernimmt dasselbe Artefakt, liefert es über OIDC aus und prüft den Release-Commit auf `/health`.

In Azure App settings werden `PASSWORD`, ein stabiler zufälliger `SECRET_KEY` und `SCM_DO_BUILD_DURING_DEPLOYMENT=true` gesetzt. Für die LB entspricht `PASSWORD` dem GitHub-Benutzernamen **BotondCsereklye**. Speichern, Neustart abwarten und den Login auf der Azure-URL prüfen. Die lokale `.env` wird nicht hochgeladen.

GitHub benötigt die OIDC-Secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` und die Repository-Variable `AZURE_WEBAPP_NAME`. Ohne diese Variable wird der Deployment-Job übersprungen. Die Einrichtung ist in [AZURE.md](docs/AZURE.md) beschrieben.

## Aufgabe 5 Happiness

[Issue #5](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/5), `feature/5-happiness` und [PR #6](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/pull/6) belegen die Umsetzung. Der vorgegebene Test `test_add_entry_with_happiness` prüft Redirect, Inhalt und Stimmung. Ergänzende Tests prüfen Darstellung, Standardwert und ungültige Eingaben. Die Funktion ist in `dev` und `main` enthalten.

Der Happiness-Branch wird gemäss LB nicht gelöscht.

## Artefakte und Abgabe

`python scripts/package_release.py` erstellt `dist/deploy.zip` mit SHA-256 sowie `release.json` mit Version, Commit und Dateihashes. Enthalten sind nur Laufzeitdateien.

Auf Linux/macOS lässt sich das ZIP mit folgendem Befehl prüfen:

```bash
python scripts/smoke_runtime.py dist/deploy.zip --expected-commit <vollständige-Commit-ID>
```

Die Commit-ID liefert `git rev-parse HEAD`.

Auf Moodle werden Repository-URL und `CsereklyeBotondLB-324.zip` abgegeben. Das Archiv enthält genau einen gleichnamigen Projektordner mit Code, Tests und Dokumentation. `.env`, `.venv` und `.git` gehören nicht hinein. Das endgültige Archiv wird nach dem Deployment aus dem finalen Stand erstellt und auf Vollständigkeit und ausgeschlossene Geheimnisse geprüft.

Quellen: [pre-commit](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages), [GitHub Workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [Azure-Deployment](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions).
