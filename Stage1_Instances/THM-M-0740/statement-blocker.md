# Exact-statement gate: blocked

Item: `S56-M-0740-STATEMENT`  
Theorem: `THM-M-0740`  
Worker base revision: `3159849a5319960dea505779c7c20894ea30487c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `单调电路下界` / `单调电路的下界` ("monotone circuit lower
bounds"). The record supplies no theorem locator, circuit model, function family, parameter
regime, lower-bound expression, ordered binders, hypotheses, or conclusion. The source status
`已验证` is explicitly untrusted under rev-5.6.

A separate computer-science inventory row says `CLIQUE的单调电路下界`, which makes Razborov's
CLIQUE result a plausible discovery lead but does not identify the exact target of this separately
scheduled theorem. Even after choosing CLIQUE, proposition-changing choices remain open:

- the finite graph/input encoding and whether the predicate is an exactly-`k` or at-least-`k`
  clique predicate;
- the relation between `k` and the vertex count and all lower thresholds on those parameters;
- the monotone gate basis, fan-in, constants, circuit DAG sharing, and nonuniformity convention;
- the resource measure and exact finite or asymptotic lower-bound function;
- exact computation versus one-sided approximation and the order of all quantifiers;
- Razborov's 1985 result versus a later strengthened monotone CLIQUE lower bound.

Selecting values for these fields would invent or substitute mathematics. Consequently there is
no canonical expression to serialize or hash, no sound alternate-form transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary mutation test. The statement
gate in section 5.1 of the rev-5.6 blueprint therefore fails before proof evidence may be
inspected. The prerequisite intake node is also only worker-provisional (`[_]`) and has not received
master acceptance.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated to distinguish an available pinned Lean
environment from the missing mathematical proposition. With only
`Mathlib.Combinatorics.SimpleGraph.Clique` and `Mathlib.Order.Monotone.Basic`, it checks finite
simple-graph clique predicates and the generic order-theoretic `Monotone` predicate. A scoped
search of pinned mathlib found no Boolean-circuit complexity datatype or monotone-circuit lower
bound API. The probe is encoding reconnaissance only and receives no canonical-statement or proof
credit. No `sorry`, `admit`, or `axiom` occurs in the target's Lean source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing canonical `.lake` artifacts were
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0740` | 0 | rank 776; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English labels, Razborov, and CLIQUE wording | 0 | only the underspecified target metadata and the separate secondary CLIQUE clue were found |
| pinned-mathlib `rg` search for Boolean-circuit declarations, monotone circuits, and circuit complexity | 0 | matches were only unrelated matroid/graph uses of "circuit"; no Boolean-circuit complexity interface was found |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0740/IntakeProbe.lean)` | 0 | all six graph/clique/order API checks elaborated; no canonical theorem asserted |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0740 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact result with a theorem/page locator, audit errata, freeze every circuit,
function, parameter, resource, quantifier, and boundary convention above, and independently approve
the mapping to this repository ID. After master acceptance of the intake dependency, a later
statement run can encode that exact claim, minimize pinned imports, fingerprint the elaborated
expression, check alternate transports, and execute all four required mutation classes.

This node remains `[ ]`, with machine state `M4`, `audit_complete: false`, and
`theorem_complete: false`. The assigned phase is not genuinely self-tested to its completion gate,
so no `.stage1-worker-selftest.json` is emitted.
