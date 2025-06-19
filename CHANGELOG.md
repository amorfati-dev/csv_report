# Changelog
Alle erwähnten Änderungen folgen dem [Keep a Changelog](https://keepachangelog.com/de/1.1.0/)
Format und [SemVer](https://semver.org/lang/de/) (vX.Y.Z).

## [0.1.0] – 2025-06-21
### Hinzugefügt
- **CSV → REST**: Erste REST-Endpoints für hochgeladene CSV-Dateien
- **Swagger-UI / OpenAPI**: Automatisch generierte API-Doku
- **Docker-Setup**: `docker compose up` bringt alles zum Laufen
- **Health-Check-Route**: `/health` liefert Build-Commit & Timestamp

### Geändert
- Konsolidierte Parsing-Logik in `csv_report/core/parser.py`
- Environment-Config jetzt über Pydantic `Settings`

### Entfernt
- Legacy-Script `csv_to_json.py` (wird durch REST ersetzt)

[0.1.0]: https://github.com/<dein-repo>/releases/tag/v0.1.0


