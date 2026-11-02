# Azure Auslieferung

Status: pausiert bis zur Freigabe. Der Job `deploy` ist im Workflow ausdrücklich mit `&& false` gesperrt. Diese Sperre erst zur freigegebenen Deployment-Einrichtung entfernen. Tests und Artefaktbau auf main bleiben aktiv.

Offene Einrichtung und fachliche Abnahme werden in [Issue #14](https://github.com/BotondCsereklye/CsereklyeBotondLB-324/issues/14) verfolgt. Die Konfiguration ist vorbereitet; eine erfolgreiche Cloud-Auslieferung ist noch nicht nachgewiesen.

## Funktionsweise

Der Deploymentprozess überträgt ein geprüftes Release in eine konfigurierte Laufzeitumgebung. In diesem Projekt startet ein Push nach main zunächst Tests, Paketbau und die HTTP-Prüfung des Laufzeit-ZIPs. Der abhängige Deployment-Job lädt dasselbe Artefakt desselben Laufs. OIDC ermöglicht die Anmeldung von GitHub Actions bei Azure ohne dauerhaft gespeichertes Azure-Client-Passwort. Der App Service startet die Anwendung mit Gunicorn und installiert die Python-Abhängigkeiten aus requirements.txt.

Konfiguration und Programmdateien werden getrennt behandelt: PASSWORD und SECRET_KEY liegen in Azure App settings; die lokale .env gehört nicht zum Paket. Nach der Übertragung prüft /health, ob die erwartete Commit-ID tatsächlich läuft. Damit reicht eine erreichbare Startseite einer älteren Version nicht als erfolgreicher Auslieferungsnachweis.

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

1. Nach Freigabe die Workflow-Sperre entfernen und den geprüften Release über einen PR von `dev` nach `main` übernehmen.
2. „Azure Auslieferung main“ führt zuerst den Job `verify` aus: Tests, ZIP-Bau, echte Gunicorn-/HTTP-Prüfung und Aufbewahrung des geprüften Artefakts. Dieser Job benötigt keine Cloud-Zugangsdaten. Der abhängige Job `deploy` lädt genau dieses Artefakt und führt OIDC-Anmeldung, Auslieferung und HTTP-Prüfung durch. Fehlende OIDC-Secrets werden vor der Anmeldung nur mit ihrem Namen gemeldet. Ein übersprungener Deploy-Job gilt nicht als Auslieferung.
3. `/health` muss `status=ok` und die Commit-ID dieses Releases zurückliefern. Das Prüfskript berücksichtigt Azure-Kaltstarts.
4. Die tatsächliche Azure-URL im README ergänzen. In einem privaten Browserfenster einloggen, Eintrag mit `😃` verfassen und sichtbare Stimmung prüfen.
5. URL, Actions-Lauf, Commit-ID, Datum und tatsächliche Login-Prüfung in `docs/NACHWEISE.md` eintragen. Keine Geheimnisse in Screenshots.

Nach der Azure-Einrichtung kann der Workflow über Actions → Azure Auslieferung main → Run workflow auf `main` erneut gestartet werden. Ein manueller Start auf einem anderen Branch führt keine Release- oder Deployment-Jobs aus. Die Variable `AZURE_WEBAPP_NAME` muss auf Repository-Ebene gesetzt sein; die OIDC-Secrets können auf Repository-Ebene oder im Environment `production` liegen.

## Fehler und Wiederherstellung

Ein fehlerhafter Prüfjob stoppt den Ablauf vor der Auslieferung. Ein fehlgeschlagener Deployment- oder Health-Schritt muss untersucht werden; der gesamte Lauf gilt dann nicht als erfolgreiche Auslieferung. Für eine Rücknahme wird der problematische Code mit git revert auf einem neuen Feature-Branch rückgängig gemacht, durch die dev-CI geprüft und als neues Release übernommen. /health bestätigt anschliessend den Commit dieses korrigierten Releases.

Die Vorlage verwendet Arbeitsspeicher statt persistenter Datenbank. Neustarts und Auslieferungen löschen die Demo-Einträge; deshalb wird ein einzelner Gunicorn-Worker verwendet.

Quellen: [Microsoft Deployment mit GitHub Actions](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions), [Microsoft Python-App-Konfiguration](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python).
