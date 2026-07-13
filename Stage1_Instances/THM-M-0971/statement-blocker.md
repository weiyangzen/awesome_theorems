# THM-M-0971 exact-statement gate: blocked

- Item: `S56-M-0971-STATEMENT`
- Base revision: `f3910e9d9c9dde383801913343b9244462e6173a`
- Base tree: `28f0e995eac01d75999b013a02e02eb792c07754`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title `Shearer界` (Shearer bound), attribution to James
Shearer in 1985, and the gloss `Lovász局部引理的最优条件` (the optimal condition for the Lovasz
Local Lemma). The catalog cites no work or theorem and contains no definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, reviewer, or formal declaration.
Stage0 explicitly leaves precise definitions and premises open, and the catalog's `已验证` label is
untrusted under rev-5.6.

The matching source lead does not select a unique root. The publisher abstract for J. B. Shearer's
1985 paper *On a problem of spencer* mentions both a sharp symmetric maximum-degree threshold and a
sharp general lower bound for the probability that no event occurs. Later accounts formulate
independent-set-polynomial positivity criteria and separate sufficiency from necessity or
optimality. These claims are not interchangeable. Nor does the repository fix:

- the original general bound, a polynomial criterion, the symmetric threshold, a positivity
  corollary, or an optimality converse as the root;
- open- versus closed-neighborhood dependence, the sigma-algebra or intersection formulation, or
  a lopsided conditional formulation;
- the finite graph and probability domains, event measurability, coordinate bounds, polynomial
  indexing, sign, normalization, strictness, and exact conclusion; or
- empty and singleton index sets, edgeless or complete graphs, isolated vertices, empty or full
  events, zero or one probabilities, zero polynomial values, equality at the boundary, and degree
  zero or one cases.

Choosing one familiar candidate would invent, narrow, broaden, strengthen, or substitute
proposition-changing mathematics rather than elaborate the received target. The neighboring
ordinary Lovasz Local Lemma, Moser-Tardos algorithm, and Janson inequality are separately owned
targets and cannot supply a statement by implication.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves `canonical_statement`, `canonical_claim`,
the Lean module and expression, target imports, elaborated-expression hash, and canonical-target
environment fingerprint null at `[H1, M4, R4]`. Consequently, minimal target imports, alternate
transports, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, axiom, placeholder,
assumed event-system interface, weakened corollary, or broadened theorem was introduced.

The prerequisite `S56-M-0971-INTAKE` is only provisional worker state `[_]`. Its historical receipt
declares `accepted: false`, is not content-addressed, supplies no accepted receipt ID, and remains
unaccepted by the master. That independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. It checks
eight adjacent event-independence, finite-intersection, complement-measure, simple-graph
independent-set, neighborhood, and maximum-degree APIs. The probe defines no dependency-graph event
condition, Shearer polynomial, avoidance bound, sharp threshold, canonical target, checked source
transport, or proof body. Its imports therefore cannot be certified as minimal imports for an
absent target and receive no statement or proof credit.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources identified no
Shearer, Lovasz Local Lemma, or independent-set-polynomial target. This is discovery-only
feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's exact stdout SHA-256 is
`193db404721fea00fab2f0c15cc6ef284389ab600b5affb298fd5242ad38dac2`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact executable
arguments for executable checks, exits, result summaries, and current input fingerprints are
preserved where applicable in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0971` | 0 | rank 1505, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads of the standard, skill, guideline, target manifest, catalog, Stage0 projection, execution DAG, and complete intake dossier | 0 | confirmed the provisional dependency, null canonical target, distinct candidate roots, and unresolved proposition-defining inputs |
| current `sha256sum` over named authority, source, intake, probe, toolchain, lockfile, and directly relevant pinned mathlib files | 0 | exact digests are recorded in the structured blocker |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib worktree passed |
| `lake env lean ../../Stage1_Instances/THM-M-0971/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; complete stdout SHA-256 `193db404...8dac2`; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 expected | no target match; discovery only, not an anchor audit or absence proof |
| `python3 -B Stage1_Instances/THM-M-0971/check_intake.py` | 1 | the intake-only historical checker expects the pre-integration state `[ ]`, while the current DAG records `[_]`; it is not a statement-phase validator |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, absent self-test, valid JSON, and clean whitespace agree |

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence bound to current authority.
Accountable reviewers must then preserve and hash one lawful immutable primary or approved
authoritative source, select and independently approve one exact theorem and every incorporated
definition, and transcribe every ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, and boundary case. They must explicitly reconcile the general,
independent-set-polynomial, symmetric, positivity, and optimality candidates.

A fresh statement attempt can then freeze the graph, dependency, probability, and polynomial
encodings; strictness, equality, and degenerate cases; foundation/TCB/computation profiles; and
alternate forms. It can encode precisely the approved claim in Lean, prove its pinned direct
imports minimal, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
