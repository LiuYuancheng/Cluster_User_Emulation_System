# CUE Explanation Document — How a Blue Team "One Day" Gets Built

This explains the Cluster User Emulation System's (CUE) architecture and how
the SKILL.md workflow's output maps onto it, so an agent or reviewer
understands *why* the generated files look the way they do — not just how
to run them.

Repo: https://github.com/LiuYuancheng/Cluster_User_Emulation_System

## 1. Three-part system

```
Activities Generation Modules Repository   (library: 33 organic + 24 malicious plugins)
              |
              v
        User Action Emulator               (runs on each node, executes a persona's day)
              |
              v
       System Orchestrator                 (cloud/central web dashboard, monitors all nodes)
```

- The **Modules Repository** is just code — reusable building blocks like
  "ping a host," "send an email," "edit a PPT." It doesn't know about
  personas or schedules.
- The **User Action Emulator** is what turns modules into a *character*: it
  loads a profile, follows a timeline, and calls the right modules at the
  right times.
- The **Orchestrator** is purely observability/control: it never executes
  actions itself, it just aggregates state from every emulator and gives
  humans a dashboard.

## 2. Four levels of emulator components

CUE's emulator is explicitly layered (see `ReadMe_User_Actions_Emulator.md`):

| Level | Name | What it is | Example |
|---|---|---|---|
| 0 | Basic Action Function | One raw call into an Action API module | `pingActor.runPing()` |
| 1 | User Action | A handful of basic functions + a small schedule | "check + reply to email" (uses Action 12 twice) |
| 2 | Actor | Several user actions + schedule | "morning triage" (email check, dashboard open, ping sweep) |
| 3 | User Emulator | Actors + a full daily/weekly/monthly timeline | "Alice, SOC Analyst, Mon–Fri 08:00–17:00" |

When the skill "generates a one-day activity," it is authoring **Level 3**:
a `scheduleProfile_<Name>.py` that arranges Level 2 Actor-style groupings
(built from Level 0/1 Action API calls) along a timeline.

## 3. Why the persona files look the way they do

`scheduleCfg.txt` = the emulator's *runtime identity and network config*
(who am I, what port do I listen on, who's my orchestrator, which Python
profile module do I load). It's deliberately separate from the timeline so
the same profile logic could be reused with a different node identity.

`scheduleProfile_<Name>.py` = the *timeline/playbook*: a data structure
mapping times to actions. This is the "when" and "what" of the day.

`actorFunctions_<Name>.py` = the *glue*: thin wrapper functions the profile
calls, each of which imports one Action API module and invokes it with the
parameters documented in `Action_API_Doc.md`. This keeps the Action API
modules generic and reusable across many different personas — the wrapper
is where persona-specific values (which mailbox, which dashboard URL) live.

This mirrors CUE's stated 5-step workflow (Behavior Module Assembly →
Activities Profile Building → Customized User Emulator → Activities/Traffic
Generation → Procedure Monitoring): the skill performs steps 1–2, the
emulator performs steps 3–5.

## 4. Worked example: "Alice," SOC Analyst, one day

Assumes an 08:00–17:00 shift, Windows node, lab Orchestrator at
`10.0.0.5:5000`.

| Time | Action # | Module | What it emulates |
|---|---|---|---|
| 08:05 | 12 | `emailActor.py` | Check overnight alert-mailbox for tickets |
| 08:15 | 37 | `localServiceProber.py` | Check own workstation CPU/RAM/disk health |
| 08:20 | 13 | `functionActor.py` | Open SIEM dashboard in browser |
| 08:30 | 01 | `pingActor.py` | Ping sweep of monitored hosts |
| 09:00 | 05 | `SSHconnector.py` | SSH to a server, run log-tail command |
| 09:30 | 20 | `tsharkUtils.py` | Open a pcap for a flagged alert, inspect traffic |
| 10:15 | 10 | `databaseHandler.py` | Query local SQLite case DB for related incidents |
| 11:00 | 31 | `telebotActor.py` | Post status update to team chat |
| 11:30 | 30/33b | `dinoActor.py` / Sudoku | Short break — human realism filler |
| 13:00 | 18 | `zoomActor.py` | Join shift-handover / IR bridge call |
| 14:00 | 25 | `nmapUtils.py` | Periodic asset/port audit of a subnet segment |
| 15:00 | 15 | `networkServiceProber.py` | HTTP GET to ticketing-system API for status sync |
| 15:30 | 02 | `WebScreenShoter.py` | Capture dashboard screenshot for report |
| 16:00 | 17 | `funcActor.py` | Edit end-of-shift PPT report |
| 16:45 | 12 | `emailActor.py` | Send shift-handover email with report attached |

Notes on realism:
- Actions aren't evenly spaced — investigation-heavy mid-morning, meeting
  mid-day, reporting near end of shift, matching a real analyst's rhythm.
- A short "human filler" action (browser mini-game, chat) is included so
  the traffic isn't 100% security-tool calls, which is what makes emulated
  traffic look organic rather than scripted.
- Every target in this table (mailbox, SSH host, subnet, ticketing API) is
  a placeholder — the actual `scheduleProfile_Alice.py` must have these
  filled with lab-specific values before deployment.

## 5. Why this is useful (business context from the upstream project)

Per the CUE README's stated purposes, generating this kind of blue-team day
supports:
- DFIR training environments that need a realistic backdrop of legitimate
  user/analyst activity, so trainees learn to distinguish signal from noise.
- Cyber-range exercises where blue-team "defense activity" needs to be
  visible to red-team/monitoring tooling as a live target, not just static
  config.
- Regression/stress testing of SIEM or detection rules against known-benign
  traffic patterns (to check false-positive rates).
- AI/ML detection-model testing, where a repeatable, labeled "normal
  analyst day" is a valuable negative-class dataset.

## 6. What this system is *not*

- It is not a natural-language chatbot interface — CUE takes Python profile
  files, not prompts. The SKILL.md workflow is the translation layer an
  agent provides on top of it.
- It is not, by itself, a detection or monitoring tool — the Orchestrator
  shows *emulator* task state, not real security telemetry from the wider
  network.
- The same framework can emulate red-team/malware behavior via its separate
  Malicious modules repository — that is a distinct, more sensitive
  capability and is intentionally out of scope for the blue-team-day skill
  described here (see SKILL.md §7 safety boundaries).
