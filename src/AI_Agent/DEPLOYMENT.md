# CUE Deployment Introduction — Blue Team Day Emulation

This is the practical install/run guide for putting a generated blue-team
persona profile onto a node using the Cluster User Emulation System (CUE).
It follows the setup steps documented in the upstream repo README plus the
config template shipped in `src/actionScheduler`.

Repo: https://github.com/LiuYuancheng/Cluster_User_Emulation_System

## 1. Components you are deploying

CUE has three parts; for one persona's one-day emulation you normally deploy
two of them:

1. **Activities Generation Modules Repository** — the library of Action API
   modules (network/application/human/system). Can live centrally on a
   shared DB/file server or be copied locally to each node.
2. **User Action Emulator** — runs *on the target node*, loads the
   persona's profile, and executes the day's timeline.
3. **Orchestrator (Scheduler Monitor Hub)** — optional but recommended;
   a central web dashboard that aggregates task state from every emulator
   node and lets you monitor/deactivate scheduled actions in real time.

## 2. Prerequisites

- Target OS: Windows (primary supported target for the human-activity
  modules like PPT editing, mouse/keyboard simulation); Linux is fine for
  network/system-only personas.
- Python 3.7.4 (repo's tested baseline; newer 3.x generally works for the
  network/system modules, verify UI-automation modules like PyAutoGUI on
  your target Python version).
- Python packages (from repo's Program Setup section):
  ```
  beautifulsoup4 keyboard mouse numpy paramiko Pillow PyAutoGUI
  pythonping requests schedule selenium pyscreenshot python-nmap
  pynput scp
  ```
- Network reachability between the node and the Orchestrator hub (UDP/HTTP
  per your `scheduleCfg.txt` settings).
- Any lab-only credentials/targets the persona's timeline needs (SSH hosts,
  FTP, mailbox, PLC/RTU addresses) — never production credentials.

## 3. Step-by-step: deploy the User Action Emulator on a node

1. **Clone the repo** on the target node:
   ```
   git clone https://github.com/LiuYuancheng/Cluster_User_Emulation_System.git
   cd Cluster_User_Emulation_System
   ```
2. **Install dependencies** by running the profile's `setup.bat`
   (Windows) — or `pip install` the package list above manually on Linux.
3. **Place the generated persona files** into
   `src/actionScheduler/`:
   - `scheduleCfg.txt`
   - `scheduleProfile_<Name>.py`
   - `actorFunctions_<Name>.py`
   (These three are exactly what the SKILL.md workflow produces for a
   persona.)
4. **(Windows autostart, optional)** Copy the auto-execution script (e.g.
   `runCUE_<Name>.bat`) into:
   ```
   C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```
   so the emulator relaunches the persona's daily timeline on every login/boot.
5. **Edit `scheduleCfg.txt`** for this node/persona (template from the
   repo, one `key:val` per line):
   ```
   # Own identity
   Own_ID:<Name>

   # This node's IP
   OWN_IP:<node_ip>

   # UDP port this scheduler listens on
   HOST_PORT:3001

   # Register with the Orchestrator hub on start
   RPT_MD:True
   HUB_IP:<orchestrator_ip>
   HUB_PORT:5000

   # Which profile module to import (no .py extension)
   PROFILE:scheduleProfile_<Name>
   ```
6. **Run the emulator**, either:
   - `src/runScheduler_win.bat`, or
   - `cd src/actionScheduler && python ScheduleRun.py`
7. **Verify**: the emulator spawns a data-manager sub-thread plus daily/
   weekly/random handler threads; as each scheduled action's timestamp is
   reached, it spins up a sub-actor thread that imports the mapped Action
   API module and executes it, then logs the result locally and reports
   status to the Orchestrator (if `RPT_MD:True`).

## 4. Step-by-step: deploy the Orchestrator (Scheduler Monitor Hub)

Run this once, centrally (cloud VM or a management node in the cluster) —
not per persona.

1. From the cloned repo:
   - `src/runMonitor_win.bat`, or
   - `cd src/monitorHub/frontend && python app.py`
2. Confirm the hub's IP/port match every node's `HUB_IP`/`HUB_PORT` in
   their `scheduleCfg.txt`.
3. Open the web dashboard to confirm each emulator node registers and its
   scheduled daily/weekly/random tasks appear.
4. From the dashboard you can monitor execution state per persona and
   remove/deactivate a specific scheduled action if you need to adjust the
   day mid-run (adding/editing actions from the web UI is marked
   "under development" upstream — edits should be made in
   `scheduleProfile_<Name>.py` and the emulator restarted).

## 5. Multi-persona / multi-node rollout

For a cyber-range cluster with several blue-team personas:

1. Generate one profile package per persona (Alice = SOC analyst, Bob =
   network admin, etc.) via the SKILL.md workflow.
2. Give each a unique `Own_ID` and `HOST_PORT` (repo's template shows
   `HOST_PORT:3001` / `3002` for different personas on the same subnet).
3. Point every `scheduleCfg.txt` at the same `HUB_IP`/`HUB_PORT` so the one
   Orchestrator dashboard shows the whole cluster's activity.
4. Stagger start times slightly if all nodes boot simultaneously, so the
   hub's registration traffic doesn't spike at once.

## 6. Validating a generated one-day profile before wide rollout

- Dry-run on a single lab node first with `RPT_MD:False` (no hub
  dependency) and watch local logs for each action firing at the expected
  time.
- Check that every external target referenced (SSH host, FTP server, mail
  account, PLC IP) is a lab-only placeholder or an address you control.
- Confirm the emulator's local DB is writable and the log path exists.
- Only then set `RPT_MD:True`, point at the shared Orchestrator, and scale
  out to the rest of the cluster.

## 7. Troubleshooting quick reference

| Symptom | Likely cause |
|---|---|
| Emulator doesn't register on hub dashboard | `HUB_IP`/`HUB_PORT` mismatch or `RPT_MD:False` |
| Scheduled action never fires | Timestamp format/timezone mismatch in `scheduleProfile_<Name>.py` |
| Action fires but throws import error | `actorFunctions_<Name>.py` references a module not present under the Action Modules Repository path on this node |
| UI-automation actions (PPT edit, mouse/keyboard) fail | Not running on the intended Windows session / missing PyAutoGUI permissions |
| Nmap/Modbus/RTU actions time out | Target unreachable — confirm this node has route to the lab target, not production network |

See also `doc/ProblemAndSolution.md` in the upstream repo for maintainer-
documented issues.
