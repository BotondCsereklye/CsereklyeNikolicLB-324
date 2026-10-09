# Azure Auslieferung

Status: noch nicht live durchgeführt. Ein lokaler Start ersetzt den geforderten Azure-Nachweis nicht.

## App Service und Geheimnisse

1. Im Azure-Schülerkonto einen Linux App Service mit Python 3.12 auswählen/anlegen. Wenn verfügbar den kostenlosen F1-Plan wählen; keinen kostenpflichtigen Plan ohne eigene Entscheidung auswählen. Namen und Ressourcengruppe notieren.
2. HTTPS aktivieren. Startbefehl: `gunicorn --bind=0.0.0.0 --timeout 600 --workers 1 app:app`.
3. Unter Umgebungsvariablen/App settings `PASSWORD` mit dem LB-Wert `BotondCsereklye`, einen zufälligen stabilen `SECRET_KEY` und `SCM_DO_BUILD_DURING_DEPLOYMENT=true` setzen. Speichern und Neustart abwarten. Oryx installiert dadurch die Abhängigkeiten aus `requirements.txt`.
4. Die lokale `.env` bleibt ausgeschlossen. `load_dotenv()` überschreibt bereits gesetzte Azure-Umgebungsvariablen nicht.

## GitHub Actions mit OpenID Connect

1. Repository-Environment `production` anlegen. In Azure Deployment Center/Microsoft Entra eine OIDC-Identität für GitHub Actions einrichten, mit Auslieferungsberechtigung auf den App Service.
2. Föderierte Berechtigung: Issuer `https://token.actions.githubusercontent.com`, Audience `api://AzureADTokenExchange`, Subject `repo:BotondCsereklye/CsereklyeBotondLB-324:environment:production`.
3. In GitHub Settings → Secrets and variables → Actions die Secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` sowie die Variable `AZURE_WEBAPP_NAME` setzen. Passwort/Session-Schlüssel bleiben in Azure App settings.
4. Den vorhandenen `deploy-azure.yml` verwenden. Keine zusätzliche vom Azure-Center erzeugte Workflow-Datei aktiv lassen, die auf einem anderen Ast ausliefert.

## Release und Nachweis

1. Happiness nach erfolgreicher PR-CI in `dev` übernehmen. Release-PR `dev` → `main` selbst prüfen und mergen.
2. „Azure Auslieferung main“ muss Tests, Artefakt, OIDC-Anmeldung, Auslieferung und HTTP-Prüfung erfolgreich durchführen. Ein übersprungener Job gilt nicht als Auslieferung.
3. `/health` muss `status=ok` und die Commit-ID dieses Releases zurückliefern. Das Prüfskript berücksichtigt Azure-Kaltstarts.
4. Die tatsächliche Azure-URL im README ergänzen. In einem privaten Browserfenster einloggen, Eintrag mit `😃` verfassen und sichtbare Stimmung prüfen.
5. URL, Actions-Lauf, Commit-ID, Datum und tatsächliche Login-Prüfung in `docs/NACHWEISE.md` eintragen. Keine Geheimnisse in Screenshots.

Die Vorlage verwendet Arbeitsspeicher statt persistenter Datenbank. Neustarts und Auslieferungen löschen die Demo-Einträge.

Quellen: [Microsoft Deployment mit GitHub Actions](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions), [Microsoft Python-App-Konfiguration](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python).
