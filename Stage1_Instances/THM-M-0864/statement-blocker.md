# Exact-statement gate: blocked

Item: `S56-M-0864-STATEMENT`

Theorem: `THM-M-0864`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is the title `Tutte连通度定理`, the attribution William Tutte, the year
1961, and the gloss `3-连通图的轮分解` ("wheel decomposition of 3-connected graphs"). It gives no
bibliography, exact proposition, incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, corrections, errata, formal artifact, or reviewer. Stage0 repeats that gloss while
explicitly leaving the formal system, definitions, premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifacts open. The catalog's `已验证` label is untrusted inventory
metadata under rev-5.6.

The intake identifies the primary publication bibliographically and inspects a precise modern
theorem-family lead. Carmesin and Kurkofka, arXiv `2304.00945v3`, Section 2.7, Theorem 2.7.1,
states that every minimally 3-connected finite graph is a wheel, where deleting or contracting any
edge destroys 3-connectivity. That result is not an accepted replacement for the catalog's broader
"wheel decomposition" wording. The original 1961 theorem and its incorporated definitions were not
inspected, and no independent review establishes that the catalog selects this minimal
characterization rather than a contraction reduction, inverse splitting construction, or another
decomposition theorem.

Those choices are proposition-changing. The repository also does not fix:

- finite simple input graphs versus multigraphs at contraction boundaries;
- the exact vertex 3-connectivity predicate and its low-cardinality convention;
- edge deletion, contraction, loop removal, parallel-edge simplification, and carrier transports;
- the hub-and-rim wheel definition, rim-size boundary, and equality versus graph isomorphism;
- whether the root concludes a wheel characterization or supplies a reduction/construction
  sequence, including allowed operations and termination; or
- universes, finiteness and decidability assumptions, binder order, boundary cases, and credited
  alternate encodings.

Selecting the familiar minimal characterization would therefore invent or substitute mathematics.
Tutte's perfect-matching theorem, `SimpleGraph.IsFiveWheelLike`, ordinary connectedness, a fixed
wheel, and a planar or polyhedral special case are also non-equivalent substitutes.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical human statement,
Lean module and expression, minimal imports, and expression/environment fingerprints null at
`[H1, M4, R4]`. Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, invented graph interface, weakened special case, or broadened
theorem was introduced.

The prerequisite `S56-M-0864-INTAKE` has only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and contains
no accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt, but
master acceptance remains independently required before any future statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its three direct imports
authenticate eight adjacent APIs for ordinary connectivity, vertex deletion, cycle graphs, graph
isomorphism, vertex replacement, a single edge, and edge deletion. The probe does not define vertex
3-connectivity, an ordinary wheel, edge contraction, minimal 3-connectivity, a decomposition
sequence, a canonical target, or a proof body. Its imports are substrate evidence only and cannot
be certified minimal for an absent canonical target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no direct
Tutte wheel theorem, ordinary wheel predicate, vertex 3-connectivity predicate, edge-contraction
definition, or minimal 3-connectivity declaration. This is narrow discovery evidence, not the
downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0864` | 0 | rank 1418; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the record does not select an exact theorem variant; the intake deliberately leaves the canonical claim and formal target null |
| authority, source, intake, toolchain, lockfile, probe, and pinned-mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0864/check_intake.py` | 1 | the historical intake checker stops at its frozen blueprint hash after integration advanced the authoritative checklist; historical evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the recorded environment |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; the dependency worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0864/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; complete stdout SHA-256 `3d6040d1564a9ea4fc42594ec8e9ca555a38d4122be45de05f15b28dacf94fcb`; no canonical target or proof body |
| bounded exact-topic search over repository-local and pinned-mathlib Lean, excluding the owned intake prose | 1, expected no match | no direct target interface was located; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker assertions, and whitespace checks | 0 | identity, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
reviewers must then lawfully preserve and hash an immutable primary or approved authoritative
source, locate the exact theorem and incorporated definitions, select the minimal characterization
or a fully specified reduction/construction root, and approve every graph carrier, connectivity,
wheel, operation, transport, binder, hypothesis, conclusion, correction, erratum, and boundary
choice.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
