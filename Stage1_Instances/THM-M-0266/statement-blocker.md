# Exact-statement gate: blocked

Item: `S56-M-0266-STATEMENT`

Theorem: `THM-M-0266`

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0266-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Dependency-ordered preparation is possible, but the
intake receipt is unaccepted and deliberately leaves the canonical proposition and formal target
null.

More decisively, the exact source-statement gate fails. The complete repository record names the
Stone-Weierstrass theorem, attributes it to Marshall Stone in 1937, and says only "density of
algebras of continuous functions." It supplies no citation, formula, incorporated definitions,
ordered binders, premises, conclusion, proof boundary, correction history, or reviewer. Stage0
repeats that gloss while explicitly leaving precise definitions and assumptions open. The catalog
label `verified` is untrusted metadata and supplies neither source identity nor kernel credit.

The bibliographic leads recorded at intake do not resolve the scope. Stone's 1937 paper
"Applications of the theory of Boolean rings to general topology" matches the catalog year, while
his two-part 1948 article "The Generalized Weierstrass Approximation Theorem" is the later
name-specific lead. No exact theorem passage or definition chain from either source has been
admitted, immutably preserved, mapped, checked for corrections or errata, and independently
reviewed. Their respective roles therefore remain open.

Several proposition-changing choices follow. The root might be a real unital subalgebra theorem or
an `RCLike` star-subalgebra theorem; global density on a compact space or approximation on a compact
subset of a noncompact space; closure equality, elementwise closure membership, uniform-norm
epsilon approximation, or a pointwise epsilon form. The source must also fix the domain and
Hausdorff convention, topology, constants/unitality, star closure, separation predicate, scalar
field, universes, binder order, and treatment of empty or singleton spaces and trivial algebras.
Selecting the familiar real mathlib declaration would invent those missing choices rather than
elaborate an exact received target.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is therefore no honest canonical expression whose imports can be certified minimal, no
approved alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutations are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the single direct import
`Mathlib.Topology.ContinuousMap.StoneWeierstrass`. It checks six pinned interfaces:

- real subalgebra closure equality;
- real elementwise closure membership;
- bundled uniform-norm epsilon approximation;
- unbundled pointwise epsilon approximation;
- compact-set approximation in a possibly noncompact ambient space; and
- the `RCLike` star-subalgebra closure-equality form.

All six interfaces elaborate. The representative real and `RCLike` declarations report
`propext`, `Classical.choice`, and `Quot.sound`. This authenticates adjacent APIs only. It does not
select a source-faithful target, certify minimal imports for an absent canonical target, compile a
transport, audit terminal proof provenance, or supply statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0266` | 0 | rank 1274; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; the base revision and tree appear above |
| `git blame -L 1915,1920 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, intake, toolchain, lockfile, and mathlib-source `sha256sum` checks | 0 | exact current input fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0266/check_intake.py` | 1 | historical intake checker rejected the integration-updated DAG entry; it is stale intake evidence, not statement evidence, and was not modified |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0266/IntakeProbe.lean` | 0 | all six adjacent interfaces elaborated; output SHA-256 `0aae7fba94eb9a61012a6a5bc541de1cd0337ae61992ab0301b335b366fe9380`; representative axioms recorded above |
| bounded Stone-Weierstrass `rg` search over repo-local Lean and pinned mathlib | 0 | located the six candidate family interfaces and downstream uses; no source-identical mapping was inferred |
| prohibited-declaration scan over owned Lean files | 0 | inner `rg` returned the expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| JSON syntax and scoped semantic assertions on `statement-blocker.json` | 0 | blocker identity, null target/imports, unchanged vector, undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped tracked and new-file whitespace checks | 0 / expected new-file difference | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time authority hashes and the intake's original DAG state.
The integration lane has since recorded intake as `[_]`, so the checker fails closed on that changed
input. It was not edited or represented as passing for this statement attempt.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, identify the exact theorem and all incorporated definitions, decide the 1937
and 1948 source roles, map every ordered binder, premise, conclusion, proof boundary, correction,
erratum, and boundary case, and independently approve the mapping. They must select the scalar and
algebra structure, compactness scope, separation convention, topology, density formulation, and
credited alternate forms. Master acceptance of intake remains required before an accepted
statement transition.

A later statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, proof body, or proof
credit is claimed.
