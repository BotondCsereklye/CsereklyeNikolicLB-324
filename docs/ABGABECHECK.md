# Prüfung vor der Abgabe

Die konkrete LB bewertet 33 Punkte; Aufgabe 5 zählt doppelt. Offene Punkte sind keine erfüllten Kriterien.

| Kriterium | Prüfschritt |
| --- | --- |
| 0 Administration | Ordner und ZIP heissen `CsereklyeBotondLB-324`; ZIP enthält genau einen gleichnamigen Projektordner. **Offen:** Repository aktuell privat; öffentliche Sichtbarkeit und Push der Schlussdokumentation prüfen. |
| 1-1 Labels/Vorlage | Drei vorgeschriebene Typ-Labels in GitHub und Anforderungsvorlage mit der vollständigen Satzstruktur prüfen. |
| 2-1 Commit | Black formatiert auf pre-commit; tatsächliche Hook-Ausführung prüfen. |
| 2-2 Push | pytest läuft auf pre-push, immer und mit der ganzen Testsuite. |
| 2-3 Anleitung | Installation und Registrierung beider Hook-Typen anhand des README nachvollziehen. |
| 3-1 CI | Echter PR nach dev hat erfolgreichen pytest-Check; CI reagiert auf keine anderen Ereignisse. |
| 4-1 Azure-App | **Offen:** echte URL, Login und sichtbare App prüfen. |
| 4-2 Geheimnisse | **Offen:** Azure-App-settings und Login prüfen; `.env` fehlt in Git und Archiv. |
| 4-3 Deployment | **Offen:** Release-PR nach main und erfolgreichen Azure-Lauf mit gleicher Commit-ID prüfen. |
| 5-1 GitHub Flow | Issue → Feature aus dev → Tests/Commits → PR → grüner Check → Merge; Feature-Branch bleibt erhalten. |

- [ ] GitHub-Sichtbarkeit klären, Schlussdokumentation pushen und über PR nach dev übernehmen.
- [ ] Azure vervollständigen, bevor die LB als vollständig abgegeben wird.
- [ ] README, Nachweise und Quellcode selbst kontrollieren.
- [ ] Repository-URL und ZIP auf Moodle abgeben; dies wurde nicht automatisiert durchgeführt.
- [ ] Erst nach tatsächlichem Abschluss und Upload die lokale Löschvorgabe der Prüfungsdatei von Hand umsetzen.
