# Navin's Master Checklist — everything I need to do

> Everything on my plate, in order, with the command/action for each. Tick as
> you go. Recreated fresh — **nothing is done yet** (this is the full list).

---

## ⚡ 1. Get my machine running (do this first)

- [ ] **1.1** Download the latest workspace (or `git pull` if I already have a copy)
- [ ] **1.2** Install prerequisites: Python 3.12, `uv`, Docker Desktop, Make
- [ ] **1.3** Set up the repo environment (from `docs/development/local-setup.md`):
      `uv venv .venv --python 3.12` · `source .venv/bin/activate` ·
      `uv pip install -e` (the 4 packages) · `cp .env.example .env`
- [ ] **1.4** Re-add git remote + identity (the download doesn't carry them):
      `git remote add origin <github-url>` · `git config user.name/email`
- [ ] **1.5** Start the stack and make sure it's GREEN:
      `make infra-up` → `docker compose ps -a` (all Up, healthy) → `curl -s localhost:9001/health` → `curl -s localhost:9001/products`

## 🐙 2. GitHub housekeeping

- [ ] **2.1** Rename repo `AegisSRE` → **`AegisDeploy`** (Settings → General → Repository name)
- [ ] **2.2** Push: `git push -u origin main`
- [ ] **2.3** Confirm CI green on GitHub Actions (Config · K8s · Docs · Backend · Container jobs)
- [ ] **2.4** Invite the team (Settings → Collaborators → Add people): Jegatheesan K, Gokul J, Dhanush K

## 📚 3. Learn the codebase (so I can explain it)

- [ ] **3.1** Read `docs/members/navin-lead/study-path.md` §0 (emergency prep, 45 min) — do this tonight
- [ ] **3.2** Work through the full path (§1–§9) over the next days
- [ ] **3.3** Drill the §7 explainers until I can recite them (elevator pitch + 2-min core loop)

## 🤝 4. The team kickoff sync

- [ ] **4.1** Send pre-reads to the team (kickoff-guide §1 table: setup guide, working-rules, own phase-plan)
- [ ] **4.2** Run the kickoff sync (kickoff-guide: demo §2 → contracts walk → decisions §3 → commitments)
- [ ] **4.3** Record **D1–D9** in `docs/planning/README.md` §2 (copy from kickoff-guide §4, replace `[SYNC-DATE]`)

## 🔒 5. Contracts freeze (deadline 2026-09-08)

- [ ] **5.1** Walk the 3+ contract files with Jega (C2 — contract freeze review)
- [ ] **5.2** Freeze the contracts on 09-08 (post-freeze changes = contract PRs only)

## 🗓️ 6. Lead track — ongoing rhythm (rest of P2)

- [ ] **6.1** Weekly syncs (Mondays, 30 min) — status round, edge-case walk, demo-of-week, decisions recorded
- [ ] **6.2** Keep `p2-tracker.md` + `integration-edge-cases.md` updated each week
- [ ] **6.3** Rehearsal (integration checkpoint) — **2026-10-15**
- [ ] **6.4** P2 gate — **2026-10-31** ("one command shows every service in Grafana AND the console")

---

**Order of attack right now:** 1.1 → 1.4 → 1.5 → 2.1 → 2.2 → 2.3 → 3.1 → 4.x
**Everything else follows the dates.**
