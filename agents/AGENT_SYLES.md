# Interaction styles and prompts

Scenario:

An MA42021_agent_style_default with the 'default' style uses a tool named MA42021_tool_document to search for informational text.

An MA42021_agent_style_react with the 'react' style uses two tools named ToolService1 and ToolService2 to search for user information and activities.

An MA42021_agent_style_planner with the 'planner' style uses two tools named MA42021_tool_planner_1 and MA42021_tool_planner_2 to plan activities.


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

## 🟨 MA42021_agent_style_react — Stile **react** + Tools: **MA42021_user_data**, **MA42021_user_activities**

> The *react* style is designed for step-by-step thinking, making targeted tool calls, checking, debugging, and integrating—great for user-driven workflows.

### ✅ Prompt that works well (guided, with steps and checks)

```text
Objective: Check the current status and activities of user "Marco Rossi" (ID: U-94821).

Steps:
1) Use MA42021_user_data to retrieve user details and status (active/suspended), email, role, and team.
2) If the status is "active," use MA42021_user_activities to list the activities assigned in the last 14 days, with status (open/closed/pending) and priority.
3) If you don't find the user in MA42021_user_data, stop and report it.
4) Cross-reference the results: if you find any inconsistencies (e.g., user suspended but activity "open"), highlight them.
Output:
- Personal data summary (name, ID, team, status)
- Activity table (title, status, priority, date)
- 2 data-based actionable recommendations (e.g., ticket closure, escalation)
```

**Why it works (benefits):**

* **Clear actionable steps** → *react* can reason and decide when to call MA42021_user_data vs. MA42021_user_activities.
* **Conditions and branches** → Reduces errors (e.g., not searching for activities if the user is non-existent or suspended).
* **Cross-validation** → Encourages the agent to check data consistency.
* **Structured output** → Facilitates use and action (actionable recommendations).

***

### ❌ Prompt doesn't work well (confusing, out of sequence, ambiguous)

```text
Give me all the useful information about Marco Rossi and his recent activities.
```

**Why it doesn't work (flaws):**

* **Identity ambiguity** (“Marco Rossi” is a common name) → risk of mismatches or mixed results.
* **No tool sequencing** → *react* may make suboptimal or redundant calls.
* **Lack of timing and state criteria** → the agent may retrieve old or irrelevant activities.
* **No error handling** → if the user doesn't exist, the agent may invent or leave gaps unreported.

### Optimize using agent instructions

Add following instructions to the agent
```yaml
instructions: |
  Use the tool "MA42021_user_data" to get personal data of the user.
  Use the tool "MA42021_user_activities" to get the list of activities of the user.
  Steps:
    1) Use MA42021_user_data to retrieve user details and status (active/suspended), email, role, and team.
    2) If the status is "active," use MA42021_user_activities to list the activities assigned in the last 14 days, with status (open/closed/pending) and priority.
    3) If you don't find the user in MA42021_user_data, stop and report it.
    4) Cross-reference the results: if you find any inconsistencies (e.g., user suspended but activity "open"), highlight them.
  Output:
    - Personal data summary (name, ID, team, status)
    - Activity table (title, status, priority, date)
    - 2 data-based actionable recommendations (e.g., ticket closure, escalation)
```

***

## 🟩 MA42021_agent_style_planner — Planner Style + Tools: MA42021_tool_planner_1 (plan definition), MA42021_tool_planner_2 (task scheduling/execution)

> The planner style excels at breaking down objectives, choosing subtasks, deciding on orders, dependencies, and allocations, and then planning/scheduling with dedicated tools.

### ✅ Prompt that works well (objective, constraints, criteria, milestones)

```text
Objective: Plan the rollout of a new CRM module for the Italian Sales team within 6 weeks.

Constraints and Preferences:
- Maximum budget: €45,000
- User testing window: weeks 3–4
- No downtime during the 9:00–18:00 CET hours
- Involve 2 internal trainers

Success Criteria:
- 90% users trained
- <2 critical incidents post-go-live in the first 2 weeks

Required steps:
1) Use MA42021_tool_planner_1 to generate a plan with phases, dependencies, owners, risks, and mitigations.
2) Assess the risk for critical phases (data migration, training, go-live).
3) Use MA42021_tool_planner_2 to schedule calendared activities (weekly sprints) and assign owners.
Output:
- Phased roadmap (short, textual Gantt chart)
- Milestone list and tracking KPIs
- Risk log (probability/impact) with mitigation actions
- Activity calendar (dates, times)
```

**Why it works (benefits):**

* **Measurable objective with deadline** → allows the planner to build a coherent sequence.
* **Operational and business constraints** → guide MA42021_tool_planner_1/2 in creating a realistic plan.
* **Success criteria/KPIs** → support decisions (trade-offs) and progress monitoring.
* **Explicit phases and dependencies** → the planner excels at decomposition and orchestration.

***

### ❌ Prompt works poorly (without objective or constraints, too generic)

```text
Plan CRM adoption.
```

**Why it DOESN'T work (flaws):**

* **Undefined objective** (which CRM? which team? when?) → impossible to break down correctly.
* **Lack of constraints** → the planner may generate a theoretical plan that is difficult to apply.
* **No success criteria** → there is no way to verify the plan's validity.
* **Lack of resources and scheduling** → MA42021_tool_planner_2 has no parameters for a credible schedule.

***

## Quick Guidelines for Writing Effective Prompts (for each style)

### **Default** Style (search/single response)

* **Specify**: source (MA42021_tool_document), filters (time, repository), fields to extract.
* **Format**: expected structure (list, table, bullet), length.
* **Manage**: What to do if information is missing (report gaps).

### **React** Style (multi-tool reasoning)

* **Identity and disambiguation**: User ID, time range, definition of “activity”.
* **Sequence**: “first A, then B if condition C”.
* **Checks**: inconsistencies, errors, fallbacks.
* **Operational output**: summary + recommendations.

### **Planner** Style (decomposition, dependencies, scheduling)

* **SMART objective**: scope, time, quality/metrics.
* **Constraints**: budget, resources, windows, policies.
* **Risks and mitigations**: probability/impacts, plan Bs.
* **Calendar**: milestones, sprints, assignments.

***