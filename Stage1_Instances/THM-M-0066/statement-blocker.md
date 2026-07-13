# Exact-statement gate: blocked

Item: `S56-M-0066-STATEMENT`

Theorem: `THM-M-0066`

Base revision: `9a1ce196889e32911beeeffa685084b48a969866` (tree
`00d5c1749015f44fb0c5694181253c3a08db5d47`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0066-INTAKE` has provisional state
`[_]`, not master-accepted state `[x]`, and its receipt is explicitly unaccepted. Independently of
that dependency boundary, the intake correctly leaves the canonical human statement, Lean module,
declaration or expression, expression hash, and canonical-target environment fingerprint null.

The repository's complete mathematical wording is only "a homomorphism between irreducible
representations is either zero or an isomorphism." It does not identify a source edition or exact
passage; choose the acting group, monoid, algebra, or category; fix the scalar field or division
ring; settle finite-dimensionality; or define representation, irreducibility, homomorphism, and
isomorphism. It also leaves binder order and boundary behavior for zero carriers, the zero map,
equal representations, and trivial acting objects open. These choices produce materially different
propositions. Selecting a familiar form would invent or substitute mathematics absent from the
received claim.

Rev-5.6 treats statement ambiguity and a missing elaborated-expression fingerprint as hard
blockers. There is consequently no truthful target whose imports can be certified minimal, no
credited alternate encoding for a checked transport, and no canonical expression against which
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can run. Those mutations are not runnable, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with imports
`Mathlib.RepresentationTheory.Irreducible` and
`Mathlib.CategoryTheory.Preadditive.Schur`. The most direct candidate,
`Representation.IsIrreducible.bijective_or_eq_zero`, quantifies over monoid representations over a
field and concludes `Function.Bijective f` or `f = 0`. The probe also checks packaging a bijective
intertwiner as `rho.Equiv sigma`, the simple-module version, and the categorical simple-object
version. All three printed axiom reports are `[propext, Classical.choice, Quot.sound]`.

These declarations confirm relevant pinned interfaces, but none selects the catalog's acting
object, scalar and dimensionality contract, or isomorphism encoding. The probe declares no
canonical target and supplies no checked source-to-target transport or proof credit. Its two
imports are probe facts, not a minimal-import result for the absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0066` | 0 | rank 1097; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 491,496 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0066/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]` and rejects the integration-updated `[_]`; it was not modified and is not statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| mathlib revision, tree, and worktree-status queries | 0 | pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0066/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; all three candidate axiom sets printed; stdout SHA-256 `81acf36edf36d4f014c228507eae90775debad9e71935c10fda2d7e88d92039c`; no canonical target or proof declared |
| bounded repository and pinned-mathlib search for Schur, `bijective_or_eq_zero`, and `isIso_iff_nonzero` | 0 | found the representation, simple-module, categorical, and stronger finite-dimensional forms already separated by intake; no source decision or exact catalog transport was found |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| `python3 -m json.tool Stage1_Instances/THM-M-0066/statement-blocker.json` and scoped blocker-invariant assertions | 0 | JSON parsed; identity, base, blocked state, null target/import/hash fields, unchanged vector, four unrunnable mutations, false completion fields, exact changed paths, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 wrapper result | no whitespace diagnostics; each raw no-index command returned only the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source and
independently approve one exact proposition with every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, translation, correction, erratum, and boundary case. They
must fix the acting object, scalar domain, dimensionality, representation and irreducibility
conventions, intertwiner type, zero branch, isomorphism witness, and degenerate cases. A later
statement run can then encode precisely that claim, minimize its pinned imports, serialize its
elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Master acceptance of refreshed intake evidence is also required before an
accepted statement transition.

This is the assigned phase's truthful blocker result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, proof body, or proof
credit is claimed.
