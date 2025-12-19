from ibm_watsonx_orchestrate.agent_builder.tools import tool

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


# Stati consentiti per activity_status
ALLOWED_STATUSES = {"open", "closed", "suspended"}


@dataclass
class Activity:
    """
    Modello dati per un'attività.
    - activity_title: Titolo dell'attività (stringa)
    - activity_status: Stato (string: open | closed | suspended)
    - priority: Intero 0..10
    - date: datetime (serializzato ISO 8601)
    """
    activity_title: str
    activity_status: str
    priority: int
    date: datetime

    def to_dict(self) -> Dict[str, Any]:
        # Serializza la datetime in ISO 8601 con offset di timezone se presente
        # Esempio: "2025-12-19T09:54:59+01:00"
        return {
            "activity_title": self.activity_title,
            "activity_status": self.activity_status,
            "priority": self.priority,
            "date": self.date.isoformat(),
        }


class ActivityRepository:
    """
    Repository MOCK: sostituisci con una integrazione reale (DB/API/CSV/CRM).
    La chiave è lo user_id e il valore è una lista di record attività.
    """
    _MOCK_DB: Dict[str, List[Dict[str, Any]]] = {
        "user1": [
            {
                "activity_title": "Preparare proposta per cliente ACME",
                "activity_status": "open",
                "priority": 8,
                # Stringa ISO: si può usare anche con timezone ('Z' o '+01:00')
                "date": "2025-12-18T16:30:00+01:00",
            },
            {
                "activity_title": "Aggiornare playbook di automazione",
                "activity_status": "suspended",
                "priority": 5,
                "date": "2025-12-10T11:00:00+01:00",
            },
            {
                "activity_title": "Revisionare contratto fornitore",
                "activity_status": "closed",
                "priority": 3,
                "date": "2025-12-01T09:15:00+01:00",
            },
        ],
        "marco": [
            {
                "activity_title": "Workshop interno su watsonx Orchestrate",
                "activity_status": "open",
                "priority": 7,
                "date": "2025-11-28T14:00:00+01:00",
            },
            {
                "activity_title": "Revisionare contratto fornitore",
                "activity_status": "closed",
                "priority": 3,
                "date": "2025-12-01T09:15:00+01:00",
            }
        ],
        # Aggiungi altri user_id e record secondo necessità
    }

    @classmethod
    def get_activities_by_user(cls, user_id: str) -> Optional[List[Dict[str, Any]]]:
        return cls._MOCK_DB.get(user_id)


def parse_iso_datetime(value: str) -> datetime:
    """
    Converte una stringa ISO 8601 in datetime.
    Supporta:
      - 'YYYY-MM-DDTHH:MM:SS'
      - 'YYYY-MM-DDTHH:MM:SSZ'
      - 'YYYY-MM-DDTHH:MM:SS+/-HH:MM'
    Se priva di timezone, imposta UTC per coerenza.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Formato datetime non valido: stringa vuota.")

    v = value.strip()
    # Gestione della 'Z' per UTC
    if v.endswith("Z"):
        dt = datetime.fromisoformat(v[:-1])  # rimuove 'Z'
        return dt.replace(tzinfo=timezone.utc)
    # Prova con fromisoformat: supporta offset tipo +01:00
    try:
        dt = datetime.fromisoformat(v)
        # Se naive (senza tz), normalizza a UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError as exc:
        raise ValueError(f"Formato datetime non valido: '{value}'. Atteso ISO 8601.") from exc


def validate_status(value: str) -> str:
    """
    Valida e normalizza lo stato attività.
    Consente solo: open, closed, suspended.
    Case-insensitive in input, ritorna in lowercase.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("activity_status deve essere una stringa non vuota.")
    normalized = value.strip().lower()
    if normalized not in ALLOWED_STATUSES:
        raise ValueError(
            f"activity_status '{value}' non valido. Consentiti: {sorted(ALLOWED_STATUSES)}."
        )
    return normalized


def validate_priority(value: Any) -> int:
    """
    Valida che priority sia un intero tra 0 e 10.
    Converte da stringhe numeriche se necessario.
    """
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"priority '{value}' non è un intero valido.")
    if ivalue < 0 or ivalue > 10:
        raise ValueError("priority deve essere compreso tra 0 e 10.")
    return ivalue

@tool(name="MA42021_user_activities")
def get_user_activities(user_id: str) -> List[Dict[str, Any]]:
    """
    TOOL PRINCIPALE:
    Riceve uno user-id (stringa) e ritorna una lista di attività,
    ciascuna con:
      - activity_title (string)
      - activity_status (string: open | closed | suspended)
      - priority (integer 0..10)
      - date (datetime in ISO 8601)

    Eccezioni:
      - ValueError se user_id è vuoto/non stringa
      - ValueError se utente non presente o attività non disponibili
      - ValueError se uno dei campi ha formato non valido
    """
    # Validazione input
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("Parametro 'user_id' deve essere una stringa non vuota.")
    uid = user_id.strip()

    raw_activities = ActivityRepository.get_activities_by_user(uid)
    if raw_activities is None:
        raise ValueError(f"Nessuna attività trovata per user_id '{uid}'.")

    results: List[Activity] = []
    for i, raw in enumerate(raw_activities, start=1):
        title = str(raw.get("activity_title", "")).strip()
        if not title:
            raise ValueError(f"Record #{i}: 'activity_title' è obbligatorio.")

        status = validate_status(raw.get("activity_status", ""))
        priority = validate_priority(raw.get("priority", None))
        dt = parse_iso_datetime(str(raw.get("date", "")).strip())

        results.append(
            Activity(
                activity_title=title,
                activity_status=status,
                priority=priority,
                date=dt,
            )
        )

    # Serializza tutti i record per output JSON-friendly
    return [a.to_dict() for a in results]


# ESEMPIO DI USO
if __name__ == "__main__":
    try:
        activities = get_user_activities("marco")
        for a in activities:
            print(a)
        # Esempio output:
        # {
        #   'activity_title': 'Preparare proposta per cliente ACME',
        #   'activity_status': 'open',
        #   'priority': 8,
        #   'date': '2025-12-18T16:30:00+01:00'
               # }
    except ValueError as e:
        print(f"Errore: {e}")
