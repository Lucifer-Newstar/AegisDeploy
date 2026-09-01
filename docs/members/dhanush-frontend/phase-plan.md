# Dhanush — Phase Plan (Frontend)

> My view of each phase: what I deliver, what I need, what I hand over, and when my
> track is "done". Mirrors [docs/planning/phases.md](../../planning/phases.md).

---

## Phase Overview

| Phase | My deliverables | Depends on | Integration output | Done when |
|---|---|---|---|---|
| **P2** | Console scaffold, design system (dark theme tokens), Command Center + Service pages on **mock data** | OpenAPI contract (P2 start) | Rendered console showing AegisShop services (mock) | Scaffold runs; design tokens documented |
| **P3** | Service detail page w/ anomaly bands; incident list page | Incident APIs (P3 end) | Incident list renders live incidents | Fault-to-incident demo shows in UI |
| **P4** | Incident detail (timeline + AI reasoning panel + evidence cards); Ask Aegis UI | RCA APIs, Ask engine API | AI reasoning visible on live incident; chat answers with citations | P4 checkpoint demo passes |
| **P5** | Approvals queue UI (approve/reject/defer), autonomy-mode indicator, audit viewer (C5) | Approval APIs | Approval + auto-execution visible live | Full-loop demo passes |
| **P6** | Remaining C1 pages (postmortem C4, runbooks C3, **deployments DI page**), polish, empty states | Postmortem + runbook APIs, deploy APIs | 8/8 pages live from real APIs | Product walkthrough passes |
| **P7** | Final UX pass on the cluster; support chaos demos | Cluster (Gokul) | Console fully functional on kind | Cluster demo clean |
| **P8** | Demo video, screenshots for the report | Evaluation runs | Submission-ready demo materials | Video + report assets done |

## My Track's Key Risks

| Risk | Mitigation |
|---|---|
| API delays block UI | Mock server from OpenAPI contract; swap per feature when API lands |
| Chart/visualization complexity | Start with a proven chart lib; anomaly bands as shaded regions |
| Scope creep (extra pages/effects) | Only pages in features.md (C1/C3/C4/C5); polish via P6/P7 |
| Demo-day UI bugs | P7 UX pass + P8 video as rehearsal |

## Definition of Done (per page)

- [ ] Renders from live API (or documented mock with swap date)
- [ ] Follows design tokens; responsive at demo resolution (1920×1080)
- [ ] AI-generated content clearly badged ("AI · evidence-cited")
- [ ] Code commented (rule 3), linted, CI green
- [ ] This file updated; page listed in docs/planning/product-vision.md
