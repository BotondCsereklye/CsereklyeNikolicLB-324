# Prüfung vor der Abgabe

Die konkrete LB bewertet 33 Punkte; Aufgabe 5 zählt doppelt. Offene Punkte sind keine erfüllten Kriterien.

Das zusätzlich bereitgestellte Kompetenzraster gewichtet A1 bis E1 mit 20/10/30/20/20 Prozent. Die Nachweise dafür stehen in [RASTER.md](RASTER.md); die endgültige Bewertung erfolgt durch die Lehrperson. Die aktuelle KI-gestützte Gegenprüfung im Auftrag Aleksandars steht in [ABNAHME_ALEKSANDAR.md](ABNAHME_ALEKSANDAR.md).

| Kriterium | Prüfschritt |
| --- | --- |
| 0 Administration | Ordner und ZIP heissen `CsereklyeBotondLB-324`; ZIP enthält genau einen gleichnamigen Projektordner. **Bewusst aufgeschoben:** Das Repository bleibt gemäss Auftrag vom 26. Oktober 2026 privat; die öffentliche Sichtbarkeit der LB ist noch nicht erfüllt. |
| 1-1 Labels/Vorlage | Drei vorgeschriebene Typ-Labels in GitHub und Anforderungsvorlage mit der vollständigen Satzstruktur prüfen. |
| 2-1 Commit | Black formatiert auf pre-commit; tatsächliche Hook-Ausführung prüfen. |
| 2-2 Push | pytest läuft auf pre-push, immer und mit der ganzen Testsuite. |
| 2-3 Anleitung | Installation und Registrierung beider Hook-Typen anhand des README nachvollziehen. |
| 3-1 CI | Echter PR nach dev hat erfolgreichen pytest-Check; CI reagiert auf keine anderen Ereignisse. |
| 4-1 Azure-App | **Offen:** echte URL, Login und sichtbare App prüfen. |
| 4-2 Geheimnisse | **Offen:** Azure-App-settings und Login prüfen; `.env` fehlt in Git und Archiv. |
| 4-3 Deployment | **Offen:** Release-PR nach main und erfolgreichen Azure-Lauf mit gleicher Commit-ID prüfen. |
| 5-1 GitHub Flow | Issue → Feature aus dev → Tests/Commits → PR → grüner Check → Merge; Feature-Branch bleibt erhalten. |

- [x] GitHub-Sichtbarkeit mit dem Benutzer geklärt: vorerst privat lassen.
- [ ] Öffentliche Sichtbarkeit gemäss LB erst nach neuem Auftrag umsetzen.
- [x] Botond Csereklye und Aleksandar Nikolic als Projektpartner ergänzen; Abschlusszuständigkeiten in `TEAM.md` festhalten.
- [ ] Bisherige individuelle Beiträge von Aleksandar anhand der Rückmeldung konkret ergänzen.
- [x] DevOps-Grundlagen, Werkzeugvergleich und Rasterzuordnung dokumentieren.
- [ ] Azure vervollständigen, bevor die LB als vollständig abgegeben wird.
- [ ] README, Nachweise und Quellcode selbst kontrollieren.
- [ ] Repository-URL und ZIP auf Moodle abgeben; dies wurde nicht automatisiert durchgeführt.
- [ ] Erst nach tatsächlichem Abschluss und Upload die lokale Löschvorgabe der Prüfungsdatei von Hand umsetzen.
