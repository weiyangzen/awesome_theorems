# Exact-statement gate: blocked

Item: `S56-M-0297-STATEMENT`

Theorem: `THM-M-0297`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository's authoritative source
record. The record gives only the name "Marcinkiewicz interpolation theorem," the Marcinkiewicz
attribution, 1939, and the gloss "interpolation of weak-type operators." It gives no cited
proposition, source and target measure spaces, scalar and function codomains, operator domain or
algebraic law, weak-type normalization, endpoint exponents, interpolation formula, measurability
or density assumptions, conclusion, quantitative constant, extension semantics, or boundary
cases. Stage0 explicitly leaves the precise definitions and premises, proof route, dependencies,
equivalent forms, axiom profile, machine status, and artifacts open. The catalog's `verified` label
is untrusted metadata under rev-5.6.

The historical lead J. Marcinkiewicz, *Sur l'interpolation d'operations*, C. R. Acad. Sci. Paris
208 (1939), 1272-1273, identifies a plausible primary source. Its locator is corroborated by the
reference metadata for Antoni Zygmund's later treatment. No lawful complete source edition, exact
passage and incorporated definition chain, proof boundary, translation, correction or errata
audit, or independent source review is admitted. The source lead therefore remains `H1`; it does
not authorize selection of a familiar modern version.

Materially different results fit the gloss: diagonal versus off-diagonal exponent pairs; sublinear
versus quasilinear operators; two finite endpoints versus an endpoint at infinity; simple-function
domains versus completed `Lp` spaces; qualitative boundedness versus a quantitative estimate;
and restricted-weak-type, Lorentz-space, vector-valued, multilinear, or quasi-Banach variants.
Choosing any one without an approved source crosswalk would invent or substitute mathematics.
`THM-M-0296` separately owns Riesz-Thorin strong-endpoint interpolation, and `THM-M-0374` is the
generic interpolation-family entry; neither supplies statement or proof credit here.

Consequently the intake correctly leaves the canonical human statement, Lean module and
expression, expression hash, and canonical-target environment fingerprint null at
`[H1, M4, R4]`; its ordered binders and hypotheses are empty, and its conclusion remains an
explicit unresolved `Open:` record. Without a canonical expression, no import set can be certified
minimal, no alternate encoding can receive a checked transport, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
rather than passed. No `Statement.lean`, axiom, placeholder, assumed interpolation predicate,
weakened special case, or broadened theorem was introduced.

The direct dependency `S56-M-0297-INTAKE` has provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, is non-content-addressed, and has no accepted
receipt ID. This permits a dependency-ordered blocker inspection but cannot satisfy the acceptance
gate. The independent first substantive failure is exact source-statement identity.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.MeasureTheory.Function.LpSeminorm.ChebyshevMarkov`
- `Mathlib.MeasureTheory.Function.LpSpace.Basic`

It checks `MemLp`, `eLpNorm`, `Lp`, an integral representation of `eLpNorm`, and two
Chebyshev-Markov superlevel-measure inequalities. All six adjacent APIs elaborate. They neither
define a source-selected weak-type operator contract nor state weak-to-strong interpolation, so the
probe and its imports receive no canonical-statement, minimal-import, anchor, or proof credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no named
Marcinkiewicz or weak-type interpolation declaration. This is narrow statement-feasibility
evidence, not the downstream exhaustive anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0297` | 0 | rank 1301; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; base revision and tree are recorded above |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0297/{README.md,instance.json,intake-receipt.json,scope-map.md,source-statement-crosswalk.md,task-dag.json,IntakeProbe.lean,check_intake.py,validation.md} Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/{Defs.lean,ChebyshevMarkov.lean} Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean` | 0 | all printed hashes agree with `statement-blocker.json` |
| `git blame -L 2132,2137 -- Docs/researches/math_theorems.md`; `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at that commit; source blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | Lean and Lake identities recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0297/IntakeProbe.lean` | 0 | six adjacent pinned APIs elaborated; stdout SHA-256 `034c2dc33d13fb77d236e90236dedc00913b939a507622f35f6482e852f04258`; empty stderr; no canonical target or proof body |
| `rg -n -i --glob '*.lean' 'Marcinkiewicz\|weak[ _-]*type.{0,40}interpol\|interpol.{0,40}weak[ _-]*type' Formalizations/Lean/AwesomeTheorems Stage1_Instances/THM-M-0297`; same search under `Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 expected for each search | no matching exact-topic declaration; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0297/check_intake.py` | 1 | historical intake replay stops at its authoritative-state assertion because it freezes intake `[ ]` while the integrated DAG records `[_]`; it was not rewritten or credited as statement evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*\(axiom\|constant\|opaque\)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0297` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0297/statement-blocker.json`; `jq -e '<recorded phase-invariant expression>' Stage1_Instances/THM-M-0297/statement-blocker.json` | 0 | structured blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, two-file scope, and absent self-test agree; the full expression is recorded in the JSON command ledger |
| `git diff --check -- Stage1_Instances/THM-M-0297 .stage1-worker-selftest.json`; `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0297/statement-blocker.json`; same no-index check for `statement-blocker.md` | 0 for the scoped check; 1 expected for each new-file difference | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker and receipt freeze intake-time authority hashes, the original
authoritative state, and the nine-file intake inventory. Integration later promoted the intake
worker evidence to `[_]`; these two statement artifacts also extend the inventory. This run records
that historical boundary instead of rewriting intake evidence or any state authority to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake. Accountable reviewers must then
lawfully preserve and hash one complete primary or authoritative source edition, select and
independently approve one exact result, and transcribe every incorporated definition, ordered
binder, hypothesis, exponent restriction and interpolation relation, weak-type normalization,
conclusion, constant dependency, extension convention, proof boundary, translation, correction,
erratum, and degenerate case. The measure spaces, scalar and codomain types, operator class and
domain, endpoint policy, measurability, density, and representative semantics must all be fixed.

A later statement worker can then encode only that source claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a truthful statement-node blocker, not completion of the assigned deliverable. Lifecycle
remains `planned`; the root remains `[H1, M4, R4]`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
