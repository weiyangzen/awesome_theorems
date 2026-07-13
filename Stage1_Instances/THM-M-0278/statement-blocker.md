# THM-M-0278 exact-statement gate: blocked

Item: `S56-M-0278-STATEMENT`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0278-INTAKE` is only in provisional
worker state `[_]`; `intake-receipt.json` has `accepted: false`, is not content-addressed, and
contains no accepted receipt ID. More importantly, that intake deliberately leaves the exact human
claim, canonical Lean module and expression, minimal imports, expression fingerprint, and
canonical-target environment fingerprint unresolved.

The repository supplies only the title "Riesz representation theorem," Frigyes Riesz, 1909, and
the gloss "representation of linear functionals on Hilbert spaces." It gives no bibliography,
formula, definitions, ordered binders, assumptions, conclusion, or boundary convention. This
identifies the Frechet-Riesz theorem family, but it does not fix:

- `Real`, `Complex`, both as separate claims, or a common `RCLike` generalization;
- an algebraic, bounded, or continuous scalar-valued linear functional;
- how Hilbert-space completeness is expressed;
- which inner-product argument contains the representative, including complex conjugation;
- existence alone, existence and uniqueness, surjectivity, isometric equivalence, or norm equality;
- zero spaces, zero functionals, one-dimensional spaces, or nonseparable spaces.

Those are proposition-changing choices, not notation cleanup. The modern Einsiedler/Ward book
cited by mathlib is a credible source lead, but no immutable edition and theorem/page locator,
incorporated-definition and premise map, proof boundary, correction or errata audit, historical
1909 reconciliation, or independent review has been accepted. Selecting the familiar mathlib
formulation now would therefore invent or substitute clauses that the received claim does not
authorize.

Rev-5.6 treats this ambiguity as a hard blocker. There is no canonical expression whose direct
imports can be certified minimal, no exact expression or environment-expression fingerprint, and
no approved alternate encoding for a checked transport. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are not meaningful rather than
passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment.
Its sole direct import, `Mathlib.Analysis.InnerProductSpace.Dual`, exposes
`InnerProductSpace.toDual`, a conjugate-linear isometric equivalence from a complete inner-product
space over an `RCLike` field to its strong dual, and its forward and inverse pointwise equations.
The probe also elaborates the prospective proposition that every `ell : StrongDual K E` has a
unique `y : E` satisfying `forall u : E, ell u = inner K y u`. The checked proof term is retained
in `IntakeProbe.lean`; it is discovery evidence only, not the source-authorized canonical target.

This authenticates a direct and strong formal candidate, which is why the machine axis remains
`M3` rather than falling to `M4`. It does not select the source-authorized scalar domain or theorem
strength, establish source identity, or make that import minimal for an absent canonical target.
The candidate axiom reports are `[propext, Classical.choice, Quot.sound]`; neither the candidate nor
those reports receive statement, proof, or trust-closure credit here.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0278` | 0 | rank 1284; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1999,2004 -L 2225,2230 -- Docs/researches/math_theorems.md` | 0 | both sparse catalogue copies originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0278/IntakeProbe.lean` | 0 | five direct Frechet-Riesz interfaces and one candidate `ExistsUnique` wrapper elaborated; stdout is 1217 bytes with SHA-256 `93f3c131b916d8eb29ae1480e5fc06f3d3ea81cc77da50cce84615bbb9ba2ea7`; both axiom reports are `[propext, Classical.choice, Quot.sound]` |
| `python3 -B Stage1_Instances/THM-M-0278/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`, while integration now records `[_]`; it was not edited or represented as statement evidence |
| `rg -n '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0278 --glob '*.lean'` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| JSON, scoped invariant, newline, trailing-whitespace, `git diff --check`, and per-file `git diff --no-index --check` checks | 0 aggregate | the structured blocker and both new owned artifacts passed validation at the recorded blocker snapshot; each no-index check returned only the expected new-file difference exit 1 with no diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

There is no applicable `lake env lean <canonical-statement>.lean` command: the exact proposition
has not been identified. Treating the candidate probe as that command would manufacture the target
and misstate feasibility evidence as exact-statement validation.

## Retry Condition

The integration lane must master-accept the intake. Accountable reviewers must lawfully preserve
and hash an immutable primary or authoritative source, select and independently approve one exact
proposition, and crosswalk every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, historical relationship, and boundary case. They must decide
the scalar field, continuous-dual encoding, completeness, inner-product orientation, theorem
strength, norm clause, universes, and degenerate cases.

A fresh statement run may then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change, statement receipt, worker `[_]`, master acceptance, proof credit, or theorem completion is
claimed. Because the assigned exact-statement phase did not pass, no
`.stage1-worker-selftest.json` is emitted.
