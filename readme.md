# CsereklyeBotondLB-324

Leistungsbeurteilung M324 DevOps, Botond Csereklye. Grundlage: die offizielle Tagebbbuch-Vorlage aus `tagebbbuch.zip` und die fünf Aufgaben in `LB-324.docx`. Es wird kein privates Projekt übernommen.

Repository: https://github.com/BotondCsereklye/CsereklyeBotondLB-324

**Azure-URL: noch offen.** Es ist noch keine laufende Azure-Auslieferung nachgewiesen. Aufgabe 4 ist deshalb nicht vollständig erfüllt.

## Lokal starten

Voraussetzungen: Git und Python 3.12; dieselbe Version wird lokal und in Actions verwendet.

```bash
git clone https://github.com/BotondCsereklye/CsereklyeBotondLB-324.git
cd CsereklyeBotondLB-324
git switch dev
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
```

Windows/PowerShell: `py -3.12 -m venv .venv`, danach `.venv\Scripts\Activate.ps1` und `Copy-Item .env.example .env`.

In `.env` ein lokales Passwort setzen und einen zufälligen `SECRET_KEY` eintragen. Einen Schlüssel erzeugt `python -c "import secrets; print(secrets.token_hex(32))"`. `.env` niemals einchecken.

```bash
python -m flask --app app run
```

Öffnen: http://127.0.0.1:5000. Produktionsnah auf macOS/Linux: `python -m gunicorn --workers 1 --bind 127.0.0.1:5000 app:app`.

Die offizielle Vorlage speichert Einträge in der Liste `entries`, nicht in einer Datenbank. Ein Neustart löscht diese Daten. Mehrere Worker hätten unterschiedliche Listen; deshalb genau einen Worker verwenden. Die LB bewertet den CI/CD-Prozess, keine produktionsreife Tagebuchspeicherung.

## Aufgabe 1 Vorlage und Labels

Issues → New issue → **Anforderung** verwendet `.github/ISSUE_TEMPLATE/anforderung.yml`. Die Vorlage erfasst Zielsystem, Priorität (muss/soll/wird), Systemaktivität, Ergänzungen, Funktionalität, Bedingungen und Abnahmekriterien. Beispiel: „Das Tagebbbuch muss dem Benutzer die Möglichkeit bieten, eine Stimmung anzugeben, wenn er einen Eintrag verfasst.“

Die manuell zuweisbaren GitHub-Labels **Funktionale Anforderung**, **Qualitätsanforderung** und **Randanforderung** sind angelegt. Jeder Änderung geht eine Issue voraus. Issue #1 dokumentiert die Ausgangsvorlage und Issue #2 die CI/CD-Einrichtung. Commits und PRs referenzieren die Issue. Die zusätzlichen Label-Aktionen der Modulübung werden hier nicht benötigt.

## Aufgabe 2 pre-commit installieren

Nach jedem Klonen die virtuelle Umgebung aktivieren und beide Hook-Typen installieren:

```bash
python -m pip install -r requirements-dev.txt
python -m pre_commit install --hook-type pre-commit --hook-type pre-push
```

| Ereignis | Befehl | Verhalten |
| --- | --- | --- |
| Commit | `python -m black` | Formatiert geänderte Python-Dateien automatisch, ausschliesslich auf `pre-commit`. Ändert Black Dateien, erneut stagen und committen. |
| Push | `python -m pytest` | Testet die ganze Anwendung bei jedem Push auf `pre-push`, mit `always_run: true` und ohne Dateinamen. Fehler blockieren den Push. |

Die Umgebung muss beim Commit/Push aktiviert sein, da `language: system` verwendet wird. Werkzeugversionen sind in `requirements-dev.txt` gepinnt.

```bash
python -m pre_commit run --all-files --hook-stage pre-commit
python -m pre_commit run --all-files --hook-stage pre-push
python -m pytest --cov=app --cov-report=term-missing
```

Hooks laufen lokal und können umgangen werden. Deshalb ergänzt serverseitige CI die frühen Rückmeldungen; sie ersetzt diese nicht.

## Aufgabe 3 CI auf dev

`.github/workflows/ci.yml` reagiert ausschliesslich auf Pull Requests mit Ziel `dev`. Der einzige Job `pytest` installiert die Testumgebung und führt `python -m pytest` aus. Keine Push-/Issue-/Tag-Ereignisse, keine Auslieferung und kein zusätzlicher Job werden in dieser CI gestartet.

```text
Issue → Feature-Branch aus dev → Commit → Push → PR nach dev
      → erfolgreicher pytest-Check → Merge nach dev
      → geprüfter Release-PR dev nach main → Azure-Auslieferung
```

`main` ist für die auszuliefernde Version reserviert. Bis Azure eingerichtet ist, bleibt die Happiness-Änderung in `dev`. Die Feature-Äste bleiben für die LB erhalten.

## Aufgabe 4 Azure und Passwort übertragen

Die vollständige Anleitung steht in [docs/AZURE.md](docs/AZURE.md). Der separate Workflow `deploy-azure.yml` reagiert ausschliesslich auf Pushes nach `main`, also auch auf einen PR-Merge. Er prüft das Release, verpackt nur Laufzeitdateien, hält ein Artefakt mit Commit-ID fest, liefert es über OIDC nach Azure aus und prüft die Commit-ID auf `/health`.

Im Azure App Service unter Einstellungen → Umgebungsvariablen/App settings `PASSWORD` anlegen. Für die LB ist der Wert der GitHub-Benutzername **BotondCsereklye**. Zusätzlich einen zufälligen, stabilen `SECRET_KEY` setzen. Änderungen speichern und den App-Neustart abwarten. Die Anwendung liest die Azure-Umgebungsvariablen; die lokale `.env` wird nicht hochgeladen. Den Erfolg durch Login auf der echten Azure-URL prüfen.

GitHub erhält die OIDC-Secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` und die Variable `AZURE_WEBAPP_NAME`. `PASSWORD` und `SECRET_KEY` gehören in Azure, niemals in den Quellcode. Solange `AZURE_WEBAPP_NAME` fehlt, ist der Deployment-Job sichtbar übersprungen; das gilt nicht als erfolgreiche Auslieferung.

## Aufgabe 5 Happiness über GitHub Flow

Eine eigene Issue und ein aus `dev` erstellter Feature-Branch dokumentieren die Änderung. Der vorgegebene Test `test_add_entry_with_happiness` prüft POST `/add_entry`, Redirect `/`, Inhalt und Stimmung `😃`. Die `client`-Fixture meldet den Testclient an; die Eintragsliste wird vor und nach jedem Test geleert.

Tatsächliche Issues, Branches, PRs, Commits und Prüfergebnisse stehen in [docs/NACHWEISE.md](docs/NACHWEISE.md). Es wird kein fremdes Review behauptet.

## Artefakte und Abgabe

`python scripts/package_release.py` erstellt `dist/deploy.zip` und dessen SHA-256. Das ZIP enthält nur App, Runtime-Abhängigkeiten, Templates, CSS und Versionsdatei; weder `.env` noch `.venv`, Tests oder Unterrichtsdateien.

Moodle erhält die Repository-URL und `CsereklyeBotondLB-324.zip` mit genau einem gleichnamigen Ordner. Vor dem Upload [docs/ABGABECHECK.md](docs/ABGABECHECK.md) selbst prüfen. Azure, Moodle-Upload und die verlangte Löschung nach tatsächlichem Abschluss werden nicht fälschlich als erledigt angegeben.

Grundlagen: Modulaufträge zu Anforderungen, pytest, Hooks, GitHub Flow und CI. Die konkreten Abweichungen der LB (Tests bei Push, Zielast dev, Stimmung) haben Vorrang. Technische Quellen: [pre-commit Hook-Stufen](https://pre-commit.com/#confining-hooks-to-run-at-certain-stages), [GitHub Workflow-Syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [Azure GitHub-Actions-Deployment](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions), [Azure Python-Konfiguration](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python).
