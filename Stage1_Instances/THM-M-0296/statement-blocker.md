# Exact-statement gate: blocked

Item: `S56-M-0296-STATEMENT`

Theorem: `THM-M-0296`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository's authoritative source
record. That record gives only the name "Riesz-Thorin interpolation theorem," the Riesz/Thorin
attribution, 1939, and the gloss "interpolation theory for operators." It contains no cited
proposition, source and target measure spaces, scalar field, operator domain and identity, endpoint
exponents, strong-type hypotheses and constants, interpolation parameter, reciprocal-exponent
relations, exact conclusion, extension semantics, ordered binders, or boundary cases. Stage0
explicitly leaves the precise definitions and premises, proof route, dependencies, alternate
forms, axiom profile, machine status, and artifacts open. The catalog's `verified` label is
untrusted metadata under rev-5.6.

The intake correctly preserves only the named theorem family and leaves its canonical statement,
Lean module and expression, expression hash, and canonical-target environment fingerprint null at
`[H1, M4, R4]`. Its Riesz 1926 and Thorin 1939 citations are bibliographic leads, not admitted
source propositions. In particular, the historical convexity and bilinear-form formulations do
not by themselves select one modern theorem about an operator between two pairs of measure-space
`Lp` spaces.

Materially different propositions fit the catalog gloss: an operator on simple functions followed
by density versus compatible endpoint maps on completed `Lp` spaces; real versus complex scalars;
finite versus infinite endpoint exponents; open versus closed interpolation parameter range;
sigma-finite versus unrestricted measures; a pointwise-on-domain estimate versus existence and
uniqueness of a bounded extension; and differing conventions for zero endpoint constants. Choosing
one from mathematical familiarity would invent or substitute proposition-changing mathematics.

Consequently there is no canonical expression whose imports can be certified minimal, no approved
alternate encoding for a checked transport, and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutation results are undefined, not passed. No `Statement.lean`, axiom, placeholder,
assumed interpolation predicate, special case, or broadened theorem was introduced.

The direct dependency `S56-M-0296-INTAKE` has provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt is non-content-addressed, has `accepted: false`, and has no accepted receipt
ID. This permits a dependency-ordered blocker inspection but cannot satisfy the acceptance gate.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.Analysis.Complex.Hadamard`
- `Mathlib.MeasureTheory.Function.LpSpace.Basic`

It checks `MeasureTheory.Lp`, `MeasureTheory.MemLp`, `ContinuousLinearMap.compLp`,
`ContinuousLinearMap.compLpL`, and three Hadamard three-lines norm estimates. All seven adjacent
interfaces elaborate. `compLp` applies a codomain map pointwise at one fixed exponent; it is not
operator interpolation. Hadamard three-lines is a potential proof engine, not a source-selected
Riesz-Thorin statement. The probe therefore receives no canonical-statement, minimal-import,
anchor, or proof credit.

Bounded case-insensitive searches of repository-local Lean and pinned mathlib found no named
Riesz-Thorin declaration. This is narrow statement-feasibility evidence, not the downstream
exhaustive anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root
unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0296` | 0 | rank 1300; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; base revision and tree are recorded above |
| `sha256sum` over the authority, intake, toolchain, manifest, and two relevant pinned mathlib source files | 0 | all hashes agree with `statement-blocker.json` |
| `git blame -L 2125,2130 -- Docs/researches/math_theorems.md`; source blob lookup | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0296/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; stdout SHA-256 `438e7f6975d99b873d569ed44a04e52828bdb29f6e21d4a8080bc03032d63aff`; empty stderr; no canonical target or proof body |
| exact-topic `rg` over repository-local Lean; same search under pinned mathlib | 1 expected for each | no named Riesz-Thorin declaration; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0296/check_intake.py` | 1 | historical intake replay stops at line 147 because it freezes intake state `[ ]` while the integrated authoritative DAG records `[_]`; it was not rewritten or credited |
| prohibited-declaration `rg` over `Stage1_Instances/THM-M-0296/*.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped `jq -e` invariant check of `statement-blocker.json` | 0 | item identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped `git diff --check`; per-new-file `git diff --no-index --check` | 0 / 1 expected difference | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes intake-time authority hashes, the original authoritative
state, and the original nine-file inventory. Integration later promoted the intake worker evidence
to `[_]`; these statement artifacts also extend the inventory. This run records that historical
boundary instead of rewriting intake evidence or a state authority to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake. Accountable reviewers must then
lawfully preserve and hash one complete primary or approved authoritative source edition, select
and independently approve one exact result, and transcribe every incorporated definition, ordered
binder, hypothesis, measure-space and scalar convention, operator domain and identity, endpoint
restriction and bound, interpolation relation, conclusion, extension convention, proof boundary,
translation, correction, erratum, and degenerate case.

A later statement worker can then encode only that source claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This is a truthful statement-node blocker, not completion of the assigned deliverable. Lifecycle
remains `planned`; the root remains `[H1, M4, R4]`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
