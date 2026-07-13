# THM-M-0970 exact-statement gate: blocked

- Item: `S56-M-0970-STATEMENT`
- Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b`
- Base tree: `64c5aacf7cf3eb79008f5a1970151e3e53cb9966`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The entire catalog claim is the name "Moser-Tardos algorithm," its 2010 attribution, and the gloss
"a constructive proof of the Lovasz Local Lemma." It gives no bibliography, proposition, ordered
binders, probability model, algorithm, quantitative conclusion, or boundary convention. Stage0
explicitly leaves the precise definitions and premises, proof route, equivalent forms, logical
principles, machine state, and artifacts open. The catalog's verified label is untrusted inventory
metadata under rev-5.6.

The inspected source lead narrows the family but does not supply repository authority to choose a
root. Moser and Tardos's archived paper, arXiv `0903.0544v3`, presents Algorithm 1.1 and Theorem 1.2:
for finite mutually independent variables and a finite bad-event family, the asymmetric product
criterion gives an avoiding valuation, while sequential resampling has eventwise and total expected
resampling bounds. The paper also contains parallel, deterministic, and lopsided variants. Neither
the catalog nor an independent accepted review adopts Theorem 1.2, decides whether its existential
and quantitative conclusions form one package, or excludes the variants by an authoritative map.

Even after selecting Theorem 1.2, proposition-changing choices remain open: general measure spaces
versus finite probability mass functions and transport to the product of marginal laws used by the
algorithm; stored versus minimal determining-variable supports;
dependency-neighborhood representation; deterministic or randomized scheduler quantification;
fresh-resampling and unchanged-variable semantics; finite or infinite execution; almost-sure and
expected termination; per-event count and total expectation; real arithmetic and integrability;
ordered binders; and all degenerate cases. Selecting these choices in this worker would invent,
narrow, broaden, or substitute mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The provisional intake record therefore leaves the canonical
human statement, Lean module and expression, target imports, expression hash, binders, hypotheses,
and canonical-target environment fingerprint null or empty at `[H1, M4, R4]`. Minimal imports,
checked transports, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, assumed theorem,
proof body, weaker existential lemma, or broadened theorem package was introduced.

The prerequisite `S56-M-0970-INTAKE` is only provisional worker state `[_]`. Its receipt has
`accepted: false`, is unsigned and not content-addressed, and exposes no accepted receipt ID. That
independently prevents an accepted statement transition.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` imports these adjacent pinned interfaces:

- `Mathlib.Probability.Independence.Basic`
- `Mathlib.Probability.Moments.Basic`
- `Mathlib.Probability.ProbabilityMassFunction.Basic`

A narrow replay elaborated indexed independence, finite product-law, probability-measure, PMF,
moment, and integral declarations. The three axiom diagnostics reported only `propext`,
`Classical.choice`, and `Quot.sound`. The probe defines no bad-event support predicate, dependency
graph, Algorithm 1.1, resampling process, scheduler, stopping semantics, expected count, canonical
target, checked source transport, or proof body. Its imports are candidate-interface imports, not a
certified minimal set for an absent target, and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No dependency update, build, clone, fetch, or
other `.lake` mutation was run.

## Validation Evidence

All commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai). Exact arguments,
exits, result summaries, and input hashes are also preserved in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0970` | 0 | rank 1504; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| mathlib revision, tree, and status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0970/IntakeProbe.lean` | 0 | nine adjacent interfaces and three axiom diagnostics elaborated; 2154 output bytes; SHA-256 `06c4d8ba4c5725ea6fbbcc62f7be8fcea3a1e96898204050cd466618e5713471` |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 1 (expected no match) | no Moser-Tardos, algorithmic local-lemma, witness-tree, or bad-event resampling declaration found outside the owned intake/blocker records; scoped discovery only |
| `python3 -B Stage1_Instances/THM-M-0970/check_intake.py` | 1 | historical checker stops at its hardcoded intake-item equality because integration changed intake from `[ ]`, attempt 0 to `[_]`, attempt 1; it was not rewritten or represented as statement evidence |
| structured JSON and scoped blocker assertions | 0 | identity, null target/imports, four undefined mutations, unchanged vector, false completion fields, two-file change scope, and blocked state agree |
| token-anchored prohibited-declaration scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| scoped tracked and new-file whitespace checks | 0 for diagnostics | no whitespace error in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

A passing discovery probe is not a statement-node self-test.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one complete primary or approved authoritative edition, select and
independently approve Theorem 1.2 or another explicit source-defined package, and transcribe every
incorporated definition, binder, premise, conclusion, algorithm step, proof boundary, correction,
erratum, and degenerate case. They must approve the probability model, determining supports,
dependency neighborhood, scheduler, resampling execution, termination and expectation semantics,
and every source-to-Lean transport.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This is a blocked-attempt record, not completion of this statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its deliverable, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
