# Example: Incident Response Process

## User Input

> We keep having incidents where the on-call person doesn't know what to do
> and escalates everything to the CTO. I want to create runbooks for every
> service. Thoughts?

## Phase 0: Assert P

**Restated problem:** Incident response is bottlenecked on a single person
(CTO) because on-call engineers lack the context to resolve issues
independently.

User confirmed: the problem is not that incidents happen — it's that
resolution depends on one person regardless of severity.

## Phase 1: Extract Constraints

| Type | Constraint |
|------|-----------|
| Hard | CTO cannot remain the escalation point for everything |
| Hard | On-call rotation exists and must continue |
| Soft | "Runbooks for every service" — user prefers documentation-based solution |
| Implicit | Team is small (~8 engineers) — heavyweight process will be ignored |
| Implicit | Not all services are equally critical or complex |

## Phase 2: S(P) Loop

**S_0: Comprehensive runbooks for every service**

- Advocate: runbooks capture institutional knowledge. On-call reads the
  runbook, follows the steps, resolves without escalation.
- Skeptic: who writes them? Who maintains them? Runbooks rot faster than
  almost any other documentation. With 8 engineers, you'll get initial
  enthusiasm followed by stale docs that actively mislead.
- Pragmatist: writing runbooks for "every service" is weeks of work. The
  Pareto distribution of incidents means 3 services cause 80% of pages.
- User-proxy: the on-call person's problem isn't "no documentation" — it's
  "I don't know if this is serious and I'm afraid to make it worse." That's
  a confidence and escalation-path problem, not a docs problem.

**Problems found** -> Phase 3.

## Phase 3: Account For Problems

1. **Runbook maintenance burden** — blocker
   - Stale runbooks are worse than no runbooks — they give false confidence.
   - User chose: Resolve now -> scope to top 5 services by incident
     frequency. Runbook review added to deploy checklist for those 5 only.

2. **Root cause is escalation ambiguity, not missing docs** — risk
   - On-call escalates everything because there's no clear severity
     classification or "safe to try" actions.
   - User chose: Resolve now -> add severity matrix (S1-S3) with clear
     escalation rules. S3 = on-call owns it. S2 = on-call + buddy. S1 =
     wake the CTO.

3. **8-person team can't sustain heavy process** — annoyance
   - Any process that adds friction to deploys or incidents will get
     bypassed.
   - User chose: Note and accept -> keep it lightweight. One-page runbooks,
     severity matrix on a single card.

## Phase 4: Present Candidate

**Recommended:** Two-part approach:
1. Severity matrix (S1/S2/S3) with explicit escalation rules — who to call,
   when, and what "safe to try" actions exist per severity level
2. One-page runbooks for top 5 incident-generating services only, reviewed
   on deploy

- Satisfies: CTO no longer default escalation, on-call has clear decision
  framework, lightweight enough for small team
- Trade-offs: remaining services have no runbooks (but they rarely page),
  severity classification requires initial calibration
- Accepted risks: severity matrix may need tuning after first month of use
- Discarded: "runbooks for everything" (maintenance burden kills it),
  "dedicated SRE hire" (team size doesn't justify it yet), "just train
  everyone on every service" (knowledge doesn't stick without practice)
