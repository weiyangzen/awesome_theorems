# Statement-phase blocker

Item: `S56-M-1004-STATEMENT`

Verdict: blocked; no exact canonical Lean target is accepted by this artifact.

## First failed gate

The target's authoritative source wording is only "martingale expectation at stopping times"
(`鞅在停时的期望`). It does not state the hypotheses or select one of the materially different
optional-stopping theorems. The intake deliberately left open:

- the exact primary-source edition, theorem, page, and errata;
- whether the stopping times are bounded, or only the later one is bounded;
- pointwise versus almost-everywhere ordering;
- the integrability or uniform-integrability conditions;
- discrete versus continuous time and the treatment of an infinite stopping time.

Choosing among these changes the mathematical proposition. Consequently, declaring any one of
them to be the exact target would invent missing mathematics and violate the rev-5.6 exact-statement
gate. This is a source-identity blocker, not a Lean elaboration blocker.

## Narrow Lean check

`CanonicalStatementCandidate.lean` records only the bounded, discrete-time, real-valued candidate
selected provisionally by intake. It uses the single direct import
`Mathlib.Probability.Martingale.OptionalStopping`. Successful elaboration shows that this candidate
is expressible in the pinned environment; it does not resolve source identity or accept the
candidate as canonical.

Base revision: `656a1be3548d492354ef99a755ef0bbcab9bd22b`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1004` | exit 0; rank 284, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1004/CanonicalStatementCandidate.lean` | exit 0; `CanonicalTargetCandidate.{uOmega} : Prop` |
| `git diff --check -- Stage1_Instances/THM-M-1004` | exit 0; no output |

Retry condition: a scope authority must identify a precise primary-source theorem (edition and
location), freeze its hypotheses and boundary conventions, and reconcile that source statement
with the intake candidate. Only then can the statement be truthfully marked exact and subjected to
the required statement mutation checks.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is not complete.
