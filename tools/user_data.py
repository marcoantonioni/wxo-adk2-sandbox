
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Dict, Any, Optional


@dataclass
class UserInfo:
    """
    Modello dei dati utente restituiti dal tool.
    - name: Nome e cognome dell'utente
    - ID: Identificativo univoco (stringa)
    - team: Team o organizzazione di appartenenza
    - status: Stato attivo/disattivo (booleano)
    - onboard: Data di onboarding (datetime.date, serializzata come 'YYYY-MM-DD')
    """
    name: str
    ID: str
    team: str
    status: bool
    onboard: date

    def to_dict(self) -> Dict[str, Any]:
        # Serializza in un dict con la data in formato ISO (YYYY-MM-DD)
        data = asdict(self)
        data["onboard"] = self.onboard.isoformat()
        return data


class UserRepository:
    """
    Repository di esempio: sostituisci con integrazione verso DB/API.
    Qui usiamo un dizionario in-memory come mock di dati corporate.
    """
    _MOCK_DB: Dict[str, Dict[str, Any]] = {
        "user1": {
            "name": "Alice Rossi",
            "ID": "user1",
            "team": "Digital Automation",
            "status": True,
            "onboard": "2023-09-15",
        },
        "user2": {
            "name": "Bruno Bianchi",
            "ID": "user2",
            "team": "AI Engineering",
            "status": False,
            "onboard": "2022-03-01",
        },
        "marco": {
            "name": "Marco Antonioni",
            "ID": "marco",
            "team": "AI Engineering",
            "status": True,
            "onboard": "2000-09-14",
        },
    }

    @classmethod
    def get_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        # In un caso reale: query al DB o chiamata ad API
        return cls._MOCK_DB.get(user_id)


def parse_date_iso8601(value: str) -> date:
    """
    Converte una stringa ISO 8601 ('YYYY-MM-DD') in datetime.date.
    Solleva ValueError se il formato è invalido.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Formato data non valido per 'onboard': '{value}'. Atteso 'YYYY-MM-DD'.") from exc

@tool(name="MA42021_user_data")
def get_user_info(user_id: str) -> Dict[str, Any]:
    """
    TOOL PRINCIPALE:
    Input user-id (stringa) output:
      - name (string)
      - ID (string)
      - team (string)
      - status (boolean)
      - onboard (date in formato 'YYYY-MM-DD')

    Eccezioni:
      - ValueError se user_id è vuoto o non trovato
      - ValueError se la data di onboarding ha formato non valido
    """
    # Validazione input
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("Parametro 'user_id' deve essere una stringa non vuota.")

    raw = UserRepository.get_by_id(user_id.strip())
    if raw is None:
        raise ValueError(f"Utente con ID '{user_id}' non trovato.")

    # Validazione/normalizzazione campi attesi
    name = str(raw.get("name", "")).strip()
    ID = str(raw.get("ID", "")).strip()
    team = str(raw.get("team", "")).strip()
    status = bool(raw.get("status", False))
    onboard_str = str(raw.get("onboard", "")).strip()

    if not name or not ID:
        raise ValueError(f"Dati incompleti per l'utente '{user_id}': 'name' e 'ID' sono obbligatori.")

    onboard_date = parse_date_iso8601(onboard_str)

    info = UserInfo(
        name=name,
        ID=ID,
        team=team,
        status=status,
        onboard=onboard_date,
    )

    return info.to_dict()


# ESEMPIO DI USO
if __name__ == "__main__":
    try:
        result = get_user_info("marco")
        print(result)
    except ValueError as e:
        print(f"Errore: {e}")
