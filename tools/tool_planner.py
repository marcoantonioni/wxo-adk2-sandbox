from ibm_watsonx_orchestrate.agent_builder.tools import tool


from dataclasses import dataclass, asdict
from datetime import date, datetime
from decimal import Decimal
from typing import List, Dict, Optional

@dataclass(frozen=True)
class AgentError:
    error_description: str
    error_datetime: datetime

@dataclass(frozen=True)
class Activity:
    activity_name: str
    activity_duration: int  # in minuti o altra unità coerente


@dataclass(frozen=True)
class Plan:
    plan_name: str
    total_cost: Decimal
    scheduled: bool
    executed: bool
    date: date
    total_duration: int  # in minuti o altra unità coerente
    activities: List[Activity]


class PlanRepository:
    """
    Repository interno con 3 plan statici predefiniti.
    Il lookup è case-insensitive sul plan_name.
    """

    def __init__(self) -> None:
        self._plans: Dict[str, Plan] = {}

        # Piano 1
        plan_alpha = Plan(
            plan_name="Alpha",
            total_cost=Decimal("1250.50"),
            scheduled=True,
            executed=False,
            date=date(2025, 1, 15),
            total_duration=240,
            activities=[
                Activity(activity_name="Data Ingestion", activity_duration=60),
                Activity(activity_name="Normalization", activity_duration=90),
                Activity(activity_name="Quality Checks", activity_duration=90),
            ],
        )

        # Piano 2
        plan_beta = Plan(
            plan_name="Beta",
            total_cost=Decimal("3200.00"),
            scheduled=True,
            executed=True,
            date=date(2025, 3, 10),
            total_duration=360,
            activities=[
                Activity(activity_name="Pre-Deployment Tests", activity_duration=120),
                Activity(activity_name="Canary Release", activity_duration=90),
                Activity(activity_name="Metrics Review", activity_duration=150),
            ],
        )

        # Piano 3
        plan_gamma = Plan(
            plan_name="Gamma",
            total_cost=Decimal("980.75"),
            scheduled=False,
            executed=False,
            date=date(2025, 6, 1),
            total_duration=180,
            activities=[
                Activity(activity_name="Bottleneck Analysis", activity_duration=60),
                Activity(activity_name="Index Tuning", activity_duration=60),
                Activity(activity_name="Cache Strategy", activity_duration=60),
            ],
        )

        # Dizionario interno (key normalizzata in lowercase)
        for p in (plan_alpha, plan_beta, plan_gamma):
            self._plans[p.plan_name.lower()] = p

    def get(self, plan_name: str) -> Optional[Plan]:
        if not isinstance(plan_name, str) or not plan_name.strip():
            raise ValueError("Il parametro 'plan_name' deve essere una stringa non vuota.")
        return self._plans.get(plan_name.lower())


# Istanza riutilizzabile del repository
_repository = PlanRepository()

def get_plan_by_name(plan_name: str) -> Plan:
    """
    Receives a name and returns a Plan object.
    Raises KeyError if the plan does not exist.
    """
    plan = _repository.get(plan_name)

#    if plan is None:
#        raise KeyError(f"Piano '{plan_name}' non trovato. "
#                       f"Piani disponibili: {', '.join(sorted(_repository._plans.keys()))}")

    return plan


@tool(name="MA42021_tool_planner")
def get_plan_by_name_as_dict(plan_name: str) -> Dict:
    """
    Return a Plan object identified by its name.
    Raises KeyError if the plan does not exist.
    """
    plan = get_plan_by_name(plan_name)
    if plan is not None:
        d = asdict(plan)

        # Normalizza i tipi non nativamente JSON-serializzabili
        d["total_cost"] = str(plan.total_cost)  # "1250.50"
        d["date"] = plan.date.isoformat()       # "2025-01-15"
        return d
    else:
        d = AgentError(error_description="Boom!", error_datetime=datetime.now())
        return asdict(d)



# Esempio d'uso (puoi rimuoverlo in produzione):
if __name__ == "__main__":
    try:
        p = get_plan_by_name("alpha")
        print("Oggetto Plan:", p)

        p_dict = get_plan_by_name_as_dict("beta")
        print("Dict Plan:", p_dict)
    except (ValueError, KeyError) as e:
        print("Errore:", e)
