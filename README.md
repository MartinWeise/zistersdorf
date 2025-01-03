# Web-Kalender Zistersdorf

Hobby-Projekt um die Zugänglichkeit (♿) des Web-Kalenders der 
Gemeinde [Zistersdorf](https://www.zistersdorf.gv.at/system/web/kalender.aspx) zu erhöhen durch automatisches Aufrufen
der Webseite und speichern in das iCal Format.

## Download

* Ganzer Kalender als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf.ics)

### Gefiltert nach Ort:

* Kalender *Stadt 1* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_stadt_1.ics)
* Kalender *Stadt 2* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_stadt_2.ics)
* Kalender *Ort 1* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_ort_1.ics)
* Kalender *Ort 2* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_ort_2.ics)

### Gefiltert nach Typ:

* Kalender *Stillgruppe* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_stillgruppe.ics)
* Kalender *Mutterberatung* als [.ics](https://github.com/MartinWeise/zistersdorf/releases/download/v2025/zistersdorf_mutterberatung.ics)

## Ausführen

Kompatibilität mit Python 3+

```shell
pipenv install
python3 ./crawler_trash.py
```

## Ausschluss

Dies ist **kein offizielles** Projekt der Gemeinde Zistersdorf. Für eventuelle Schäden wird keine Haftung übernommen.
Bitte nicht die Webseite der Gemeinde überlasten, es sind absichtlich Pausen von 3s zwischen den Anfragen eingebaut.

## Mitarbeit

Gerne einen Pull-Request erstellen, ich begrüße Mitarbeit!