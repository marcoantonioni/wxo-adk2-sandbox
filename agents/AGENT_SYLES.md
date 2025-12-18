# Interaction styles and prompts

Scenario:

An MA42021_agent_style_default with the 'default' style uses a tool named MA42021_tool_document to search for informational text.

An Agent2 with the 'react' style uses two tools named ToolService1 and ToolService2 to search for user information and activities.

An Agent3 with the 'planner' style uses two tools named ToolPlan1 and ToolPlan2 to plan activities.


## 🟦 MA42021_agent_style_default — Stile **default** + Tool: **MA42021_tool_document** (search for informational texts)

### ✅ Prompt that works well (clear, contextual, focused)

```text
I need to prepare a one-page summary on the "IT services co-sourcing model" for management.
Use Document Tool to search company repositories for:
- Official guidelines
- Internal whitepapers from 2023 onwards
Extract: definition, benefits, risks, suggested KPIs, an internal use case.
Respond with: title, 5 main bullet points, 3 measurable KPIs, 1 real-world example (if applicable).
If any parts are missing, please explicitly indicate what was not found.
```

**Why it works (benefits):**

* **Clear objective and expected format** → the "default" agent excels at **single-shot** execution: one request, one output.
* **Restricted search scope** (corporate repositories, documents from 2023) → reduces noise and hallucinations.
* **Explicit extraction criteria** (definition/benefits/KPIs/use case) → guides the MA42021_tool_document to search for relevant strings.
* **Gap management** (“if parts are missing…”) → avoids misleading output and increases reliability.

***

### ❌ Prompt that works poorly (vague, non-contextual, unconstrained)
```text
Tell me about co-sourcing.
```

**Why it doesn't work (flaws):**

* **Total vagueness** → the "default" agent does not plan or disambiguate; a generic response not based on document content will be needed.
* **No tool instructions** → it is unclear whether it should query MA42021_tool_document.
* **No output format** → the agent may return garbled, difficult-to-use text.
* **No time or quality filtering** → possible inclusion of obsolete or non-compliant content.
***

## 🟨 Agent2 — Stile **react** + Tools: **ToolServizio1** (anagrafica), **ToolServizio2** (attività)

> Lo stile *react* è pensato per **ragionare passo-passo**, effettuare chiamate mirate ai tool, verificare, correggere e integrare—ottimo per flussi basati su dati utente.

### ✅ Prompt che lavora bene (guidato, con step e controlli)

```text
Obiettivo: verificare stato e attività correnti dell’utente “Rossi Marco” (ID: U-94821).

Passi:
1) Usa ToolServizio1 per recuperare anagrafica e stato (attivo/sospeso), email, ruolo, team.
2) Se lo stato è “attivo”, usa ToolServizio2 per elencare le attività assegnate negli ultimi 14 giorni, con stato (aperta/chiusa/in attesa) e priorità.
3) Se non trovi l’utente in ToolServizio1, fermati e segnalalo.
4) Incrocia i risultati: se trovi incongruenze (es. utente sospeso ma attività “aperta”), evidenziale.
Output:
- Riepilogo anagrafico (nome, ID, team, stato)
- Tabella attività (titolo, stato, priorità, data)
- 2 raccomandazioni operative (es. chiusura ticket, escalation) basate sui dati
```

**Perché funziona (pregi):**

*   **Passi operativi chiari** → il *react* può ragionare e decidere quando chiamare ToolServizio1 vs ToolServizio2.
*   **Condizioni e ramificazioni** → riduce errori (es. non ricercare attività se l’utente è inesistente o sospeso).
*   **Convalida incrociata** → spinge l’agente a controllare consistenza dei dati.
*   **Output strutturato** → facilita la fruizione e l’azione (raccomandazioni operative).

***

### ❌ Prompt che lavora male (confuso, senza sequenza, ambiguo)

```text
Dammi tutte le informazioni utili su Marco Rossi e le sue attività recenti.
```

**Perché NON funziona (difetti):**

*   **Ambiguità sull’identità** (“Marco Rossi” è un nome comune) → rischio di mismatch o risultati mescolati.
*   **Nessuna sequenza di tool** → il *react* può fare chiamate in ordine subottimale o ridondanti.
*   **Assenza di criteri temporali e di stato** → l’agente potrebbe recuperare attività vecchie o irrilevanti.
*   **Nessuna gestione errori** → se l’utente non esiste, l’agente potrebbe inventare o lasciare vuoti non segnalati.

***

## 🟩 Agent3 — Stile **planner** + Tools: **ToolPlan1** (definizione piano), **ToolPlan2** (schedulazione/esecuzione attività)

> Lo stile *planner* eccelle nel **scomporre obiettivi**, scegliere sotto-attività, decidere ordini, dipendenze e allocazioni, poi pianificare/schedulare con tool dedicati.

### ✅ Prompt che lavora bene (obiettivo, vincoli, criteri, milestone)

```text
Obiettivo: pianificare il rollout di un nuovo modulo CRM per il team Sales Italia entro 6 settimane.

Vincoli e preferenze:
- Budget massimo: 45.000 €
- Finestra di test utente: settimane 3–4
- Nessun downtime in orario 9:00–18:00 CET
- Coinvolgere 2 trainer interni

Criteri di successo:
- 90% utenti formati
- <2 incidenti critici post-go-live nelle prime 2 settimane

Passi richiesti:
1) Usa ToolPlan1 per generare un piano con fasi, dipendenze, owner, rischi e mitigazioni.
2) Valuta il rischio per fasi critiche (migrazione dati, formazione, go-live).
3) Usa ToolPlan2 per schedulare le attività in calendario (Sprint settimanali) e assegnare owner.
Output:
- Roadmap a fasi (Gantt sintetico testuale)
- Elenco milestone e KPI di tracking
- Registro rischi (probabilità/impatti) con azioni di mitigazione
- Calendario attività (date, orari)
```

**Perché funziona (pregi):**

*   **Obiettivo misurabile con scadenza** → permette al planner di costruire una sequenza coerente.
*   **Vincoli operativi e di business** → guidano ToolPlan1/2 nel creare un piano realistico.
*   **Criteri di successo/KPI** → supportano decisioni (trade-off) e controllo di avanzamento.
*   **Fasi e dipendenze esplicite** → il planner eccelle nel decomporre e orchestrare.

***

### ❌ Prompt che lavora male (senza obiettivo né vincoli, troppo generico)

```text
Pianifica l’adozione del CRM.
```

**Perché NON funziona (difetti):**

*   **Obiettivo non definito** (quale CRM? quale team? quando?) → impossibile decomporre correttamente.
*   **Assenza di vincoli** → il planner potrebbe generare un piano teorico poco applicabile.
*   **Nessun criterio di successo** → non c’è modo di verificare la bontà del piano.
*   **Mancano risorse e scheduling** → ToolPlan2 non ha parametri per una schedulazione credibile.

***

## Linee guida rapide per scrivere prompt efficaci (per ogni stile)

### Stile **default** (ricerca/risposta singola)

*   **Specificare**: fonte (MA42021_tool_document), filtri (tempo, repository), campi da estrarre.
*   **Formattare**: struttura attesa (lista, tabella, bullet), lunghezza.
*   **Gestire**: cosa fare se manca l’informazione (segnalare le lacune).

### Stile **react** (ragionamento con tool multipli)

*   **Identità e disambiguazione**: ID utente, range temporale, definizione di “attività”.
*   **Sequenza**: “prima A, poi B se condizione C”.
*   **Controlli**: incongruenze, errori, fallback.
*   **Output operativo**: riepilogo + raccomandazioni.

### Stile **planner** (decomposizione, dipendenze, schedulazione)

*   **Obiettivo SMART**: scopo, tempo, qualità/metriche.
*   **Vincoli**: budget, risorse, finestre, policy.
*   **Rischi e mitigazioni**: probabilità/impatti, piani B.
*   **Calendario**: milestone, sprint, assegnazioni.

***

