# Exact-statement gate: blocked

Item: `S56-M-0065-STATEMENT`

Theorem: `THM-M-0065`

Base revision: `9a1ce196889e32911beeeffa685084b48a969866` (tree
`00d5c1749015f44fb0c5694181253c3a08db5d47`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0065-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Dependency-ordered inspection is possible, but the
intake receipt is unaccepted and deliberately leaves the canonical human proposition, formal
expression, ordered binders, hypotheses, conclusion, and canonical-target fingerprint null.

More importantly, the repository record says only that a group's composition series is unique up
to isomorphism. It does not define a composition series, choose a finite-group theorem or a
conditional theorem for arbitrary groups possessing finite composition series, decide whether
existence is part of the root, select ascending or descending chains, state endpoints and successor
normality, define simple quotient factors, or specify the permutation-indexed factor isomorphisms.
These choices change the proposition and its boundary cases; they are not unresolved notation.

The inspected Milne v4.01 Definition 6.1, Theorem 6.2, and Remark 6.3(a) are a strong complete
modern source lead, but the catalog does not cite that source. The observed author-hosted copy is
not immutably preserved in this repository, its correction and one-day date discrepancy remain
unaudited, the finite versus conditional-arbitrary domain remains unselected, and no independent
group-theory reviewer has accepted the source-to-target mapping. Choosing one formulation from
mathematical familiarity would invent missing binders and assumptions.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is therefore no honest canonical group expression whose imports can be certified minimal,
no credited alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutation results are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the single direct import
`Mathlib.Order.JordanHolder`. It checks the abstract `JordanHolderLattice`, `CompositionSeries`,
`CompositionSeries.Equivalent`, its length consequence, and
`CompositionSeries.jordan_holder`. The probe succeeds and reports axioms `propext`,
`Classical.choice`, and `Quot.sound` for the generic theorem.

This does not elaborate the requested group theorem. The pinned module itself says a subgroup
realization is intended, then records as a TODO the provision of `JordanHolderLattice` instances
for subgroups and the associated group API. A bounded search found no
`JordanHolderLattice (Subgroup G)` instance, group-specific composition-series wrapper, or checked
transport from the abstract lattice relation to isomorphisms of group quotient factors. The
abstract theorem is therefore an adjacent interface, not an exact-statement substitute. Its import
is minimal for the discovery probe only and cannot be certified minimal for an absent group target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` artifact was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0065` | 0 | rank 1096; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD`; `git rev-parse HEAD^{tree}`; `git status --short --untracked-files=all` | 0 | base identities above; only the automation-provided `Formalizations/Lean/.lake` was untracked before this attempt |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}`; `git -C ... status --short` | 0 | pinned revision/tree recorded above; package source status empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0065/IntakeProbe.lean` | 0 | generic API probe elaborated; stdout SHA-256 `7190f0200066dabb70ed6a7281d3c8a35037d57ecab827a24206e5444b1bc6e5`; no group target declared |
| bounded `rg` search in pinned mathlib for a subgroup instance or group-specific wrapper | 0 | no matching realization or wrapper found |
| `python3 -B Stage1_Instances/THM-M-0065/check_intake.py` | 1 | intake-time validator is stale after integration changed the authoritative intake state to `[_]`; it is not statement evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0065/statement-blocker.json` and scoped `jq -e` assertions | 0 | blocker identity, null target/imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| scoped prohibited-construct scan over owned Lean files | 0 | no prohibited Lean declaration found; the inner `rg` returned the expected no-match exit 1 |
| scoped whitespace checks | 0 | no whitespace diagnostics in the owned blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact statement did not elaborate |

The intake checker is bound to the intake-time authoritative DAG state. Integration has since
recorded the intake as `[_]`, so that checker fails closed on a changed input. It was not edited or
represented as passing for this statement attempt.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one exact proposition, and map every incorporated definition,
ordered binder, hypothesis, conclusion, correction, and boundary case. They must decide the finite
or conditional-arbitrary domain, whether existence belongs to the root, chain orientation and
endpoints, successor normality, quotient construction, simplicity and nontriviality, factor
indexing, and isomorphism-permutation conclusion. A later statement run must then implement or pin
a faithful group realization, elaborate that exact claim, minimize its imports, serialize its
expression and environment fingerprints, compile any credited transports, and execute all four
mutation classes. Master acceptance of the intake remains required before an accepted statement
transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
