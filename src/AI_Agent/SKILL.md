---
name: cue-blueteam-day-emulation
description: >
  Use this skill to auto-generate a Blue Team member's realistic one-day
  activity timeline (network, application, human, and system actions) using
  the Cluster User Emulation System (CUE) by LiuYuancheng
  (https://github.com/LiuYuancheng/Cluster_User_Emulation_System). Trigger
  this skill whenever a user/operator asks to: simulate a blue team analyst's
  daily activity, build a defender persona for a cyber range/exercise,
  generate benign SOC/IT-admin traffic for DFIR training, create a
  scheduleProfile_<name>.py + scheduleCfg.txt deployment package, or populate
  a cyber range node with "normal user" background noise.
license: Refer to upstream repo LICENSE (GPL-3.0 for CUE core, MIT for
  Action API modules as marked in doc/Action_API_Doc.md).
---

# CUE Blue Team One-Day Activity Emulation Skill

## 1. What this skill does

This skill lets an agent act as the "Behavior Module Assembly" step of the
Cluster User Emulation System (CUE) workflow: given a blue-team role
(SOC analyst, network admin, incident responder, OT/ICS defender, IT support,
etc.), the agent selects Action API modules from CUE's Organic Actions
repository, arranges them into a timed playbook, and emits the deployable
profile files CUE expects (`scheduleProfile_<Name>.py`, `scheduleCfg.txt`,
and an `actorFunctions_<Name>.py` wrapper) so a `User Action Emulator`
instance can run that person's realistic one-day activity on a target node.

CUE itself does **not** take a natural-language prompt — it takes Python
profile/config files. This skill is the missing "compiler" layer: it maps a
role + narrative day into the exact code CUE needs.

## 2. When to use this skill

Use it when asked to:
- "Generate a day in the life of a SOC analyst / network admin / IR responder for our cyber range."
- "Create blue team background traffic/activity for a DFIR exercise."
- "Build a CUE profile for user Alice who is a network administrator."
- "Add realistic defender noise to node X for 8 hours."

Do **not** use it to generate red-team/malware profiles (CUE's Malicious
repository) unless the user explicitly asks for adversary emulation and the
context is an authorized exercise — flag that distinction back to the user
if ambiguous.

## 3. Required inputs (ask if missing)

| Input | Purpose | Default if unspecified |
|---|---|---|
| Persona name | Used as `<Name>` in file names / `Own_ID` | `Analyst01` |
| Role | Picks the activity mix (see §5) | `SOC_Analyst` |
| Shift window | Start/end time for the day | `08:00–17:00` |
| Target OS | Windows vs Linux affects which Action modules apply | `Windows` |
| Node network identity | `OWN_IP`, `HOST_PORT` | `127.0.0.1:3001` |
| Orchestrator hub | `HUB_IP`, `HUB_PORT`, whether to auto-register (`RPT_MD`) | `127.0.0.1:5000`, `True` |
| Realism level | Regular fixed-time tasks vs randomized jitter | `randomized ±10 min` |

If the user hasn't specified these, proceed with the defaults and state the
assumption — don't block on asking unless the target environment (real vs
lab) is unclear, since that changes IP/credential handling.

## 4. Action API quick reference (from `doc/Action_API_Doc.md`)

Only Organic (benign) modules are listed — these are the safe building
blocks for a blue-team day. Group by CUE's four module categories:

**Network Activities** (`Action 01–15`)
- 01 Ping targets (`pingActor.py`) — health checks / connectivity sweeps
- 02 Webpage screenshot (`WebScreenShoter.py`) — dashboard capture for reports
- 03 Download webpage contents (`webDownloader.py`) — threat-intel page pull
- 04 FTP connect (`networkServiceProber.py`)
- 05 SSH connect + run command (`SSHconnector.py`) — log/server checks
- 06 SCP file transfer (`SCPconnector.py`) — pull logs, push reports
- 07 SSH port forward (`SSHforwarder.py`)
- 08 UDP client (`udpCom.py`)
- 09 TCP client (`tcpCom.py`)
- 10 SQLite3 query (`databaseHandler.py`) — local case DB checks
- 11 InfluxDB query (`databaseHandler.py`) — metrics/telemetry checks
- 12 Send/receive email (`emailActor.py`) — inbox triage, ticket replies
- 13 Browser open URL (`functionActor.py`) — dashboards, SIEM console, intel feeds
- 14 NTP check (`networkServiceProber.py`) — time-sync verification
- 15 HTTP GET/POST (`networkServiceProber.py`) — API/webhook checks, ticketing system calls

**Application Activities** (`Action 16–26`)
- 16 Start application (`funcActor.py`)
- 17 Edit PPT (`funcActor.py`) — incident/shift report
- 18 Zoom meeting (`zoomActor.py`) — shift handover, IR bridge call
- 19 Git clone/pull (`gitDownloader.py`) — pull detection-rule/playbook updates
- 20 Wireshark capture / open pcap (`tsharkUtils.py`) — traffic triage
- 21 FTK Imager memory dump (`ftkMemDumper.py`) — forensics collection
- 22 Modbus PLC command (`modbusTcpCom.py`) — OT/ICS monitoring (if role is OT defender)
- 23 Siemens RTU command (`snap7Comm.py`) — OT/ICS monitoring
- 25 Nmap scan (`nmapUtils.py`) — asset/port audit
- 26 Speed test (`speedChecker.py`) — network health check

**Human Activities** (`Action 27–33`)
- 27 Record mouse/keyboard (`UserActionrecorder.py`)
- 28 Keyboard type-in (`keyEventActor.py`) — ticket notes, chat replies
- 29 Mouse event (`mouseInput.py`)
- 30 Browser mini-game (`dinoActor.py`) — idle/break behavior realism
- 31 Telegram chat message (`telebotActor.py`) — team comms
- 32 Open local media file (`telebotActor.py`)
- 33 Web camera capture (`cameraClient.py`)
- 33(b) Sudoku game (`pyQt5_Sudoku_Calculator.py`) — break-time realism

**System Activities** (`Action 34–41`)
- 34 Run OS commands (`c2MwUtils.py` CmdRunner) — routine admin commands
- 35 Local camera capture (`cameraServer.py`)
- 36 RS232/485 serial read/write (`serialCom.py`) — OT serial device checks
- 37 OS/process/disk state check (`localServiceProber.py`) — health monitoring
- 38 Ettercap traffic mirror (`ettercapWrapper.py`) — defensive traffic inspection
- 39 Google Maps directions (`geoLRun.py`) — commute/onsite-visit realism
- 40 Cytoscape graph → JSON (`Cytoscape_2_Json.py`) — network graph analysis
- 41 Python obfuscation encode/decode (`pyObfuscator.py`) — rarely relevant to blue team; skip unless asked

## 5. Role → activity mix presets

| Role | Emphasize | De-emphasize |
|---|---|---|
| SOC Analyst | 01, 05, 10, 11, 13, 15, 20, 25, 31, 37 | 22, 23, 36, 39 |
| Network Administrator | 01, 04, 05, 06, 14, 25, 26, 34, 37 | 21, 22, 23 |
| Incident Responder | 05, 12, 17, 18, 20, 21, 40 | 22, 23, 36 |
| OT/ICS Blue Team | 01, 22, 23, 34, 36, 37 | 21, 39 |
| IT Support / Helpdesk | 04, 12, 13, 16, 17, 34 | 20, 21, 22, 23, 38, 40 |

Always include a small amount of "human realism" filler (13, 28, 30/33b, 31)
spread through the day — a persona that only does security tooling all day
reads as artificial.

## 6. Workflow the agent should follow

1. **Clarify persona** using §3 table; confirm role preset from §5 or accept
   a custom action list from the user.
2. **Build the timeline** — draft a table: `time | Action # | module | purpose`
   covering the full shift, with 8–20 events for a normal day (fewer for a
   short demo, more for a dense exercise). Space actions realistically
   (mornings: triage/inbox/dashboards; midday: investigation/meetings;
   afternoon: reporting/handover). Add ± jitter if "randomized" realism was
   requested.
3. **Generate the profile package**, producing these files (see the
   Deployment Introduction doc for the full template):
   - `scheduleCfg.txt` — connection/runtime config (`Own_ID`, `OWN_IP`,
     `HOST_PORT`, `RPT_MD`, `HUB_IP`, `HUB_PORT`, `PROFILE`)
   - `scheduleProfile_<Name>.py` — the timeline/playbook definition
   - `actorFunctions_<Name>.py` — thin wrapper functions that import and
     call the specific Action API classes/functions from §4 for each
     scheduled event
4. **Sanity-check** the package: every action in the timeline must map to a
   module that exists in the Action API doc; every credential/target field
   must be a placeholder (`<FILL_IN>`) unless the user supplied real lab
   values — never invent real IPs/credentials/URLs.
5. **Hand off** the package with the Deployment Introduction steps so the
   user can install it on the target node and register it with the
   Orchestrator / Scheduler Monitor Hub.
6. **Do not** wire up real destructive or intrusive actions (Modbus/RTU
   writes, Ettercap mirroring, nmap sweeps) against anything other than a
   user-confirmed lab/range target — these can affect real OT/network
   equipment.

## 7. Safety boundaries

- This skill is for **benign/organic** activity generation only. If asked to
  wire in the Malicious repository (credential theft, DoS, ransomware-style
  modules), stop and clarify scope; that is a distinct red-team capability
  of the same project and requires explicit, clearly-authorized-exercise
  framing.
- Never populate real target IPs, hostnames, credentials, PLC/RTU addresses,
  or email accounts unless the user explicitly provides them for their own
  authorized environment.
- Nmap scans, Modbus/Siemens writes, and Ettercap mirroring can affect live
  industrial or network equipment — confirm the target is a lab/cyber-range
  asset before including them in a generated profile.

## 8. Related documents in this package

- `DEPLOYMENT.md` — install/config/run steps for the emulator + monitor hub.
- `EXPLANATION.md` — CUE architecture, component levels, and how a
  generated "one day" playbook maps onto them.
- Upstream references:
  - Repo: https://github.com/LiuYuancheng/Cluster_User_Emulation_System
  - Action API doc: https://github.com/LiuYuancheng/Cluster_User_Emulation_System/blob/main/doc/Action_API_Doc.md
  - `ReadMe_User_Actions_Emulator.md`, `ReadMe_User_Actions_Repository.md`,
    `ReadMe_Scheduler_Monitor_Hub.md` in the repo root.
