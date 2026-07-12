# Exact-statement gate: blocked

Item: `S56-M-1374-STATEMENT`

Theorem: `THM-M-1374`

Base revision: `73c9cdb8a4086ef1fc18f25aa52185f4b68a0094` (tree
`96d5d58add62468ac9e9de9ce525ec7b4319bacd`)

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record supplies only the title `Noether定理`, Emmy Noether, 1918, and the gloss
`对称性与守恒量` ("symmetries and conserved quantities"). It gives no citation, truth-valued
proposition, incorporated definitions, ordered binders, hypotheses, conclusion, or boundary
cases. Stage0 explicitly leaves the formal system, exact definitions and premises, proof route,
dependencies, equivalent statements, axioms, machine status, and artifact links open. The catalog
label `已验证` is untrusted metadata under rev-5.6.

The historical source family contains materially different theorems. Noether's first theorem for
a finite continuous group yields divergence relations and, on shell, first integrals or
conservation laws. Her second theorem for transformations depending on arbitrary functions yields
differential identities among Euler-Lagrange expressions. Direct and converse clauses have
different qualifications. Modern mechanics, field-theory, Hamiltonian moment-map, exact-invariance,
quasi-invariance, current, charge, and converse formulations introduce still different binders and
premises. The repository selects none of them.

Selecting the finite-dimensional statement owned by the distinct target `THM-M-1515`, a
time-translation energy law, a zero-Lagrangian example, or another familiar specialization would
invent or substitute missing mathematics. Encoding the desired derivative, current, conservation,
or differential identity as a structure field or hypothesis would instead assume the result. Both
routes are prohibited.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression/environment fingerprints null. Without one canonical target there
is no meaningful alternate-form transport or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
weakened special case, or broadened interface was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated in the pinned environment. Its direct imports
expose derivative, Frechet-derivative, continuous-linear-map, flow, and invariant-set interfaces,
and all seven checked names elaborate. These are adjacent generic APIs only. The probe defines no
variational functional, Euler-Lagrange operator, symmetry action, current, or Noether implication.
Its imports cannot be certified minimal for an absent canonical target, and the successful check
receives no statement, anchor, or proof credit.

A bounded exact-topic search found no matching variational Noether declaration in pinned mathlib.
Repository-local matches are confined to discovery material owned by the separate `THM-M-1515`
target, including its legacy `S1_M_184` module. This is a scoped feasibility observation, not the
later immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No update,
build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1374` | 0 | rank 984, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree appear above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision and tree match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; the pinned package worktree is clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1374/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; complete output SHA-256 `26302cdb022fddbd7f92db37c081f09d95a45d18df0dc1b49f10b1af3390f4d3`; no target theorem was checked |
| bounded exact-topic `rg` search in pinned mathlib | 1 | expected no-match result; no variational Noether declaration was located under the recorded expression |
| the same bounded search in repository-local Lean and `THM-M-1515` | 0 | matches belong to the separate `THM-M-1515` discovery boundary; none transfers statement or proof credit |
| `python3 -B Stage1_Instances/THM-M-1374/check_intake.py` | 1 | historical intake replay detects a stale blueprint digest after integration; this statement phase does not rewrite prior intake evidence |
| prohibited declaration and proof-escape scan over owned Lean files | 1 | expected no-match result; the API-only probe contains no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1374/statement-blocker.json` | 0 | the finalized structured blocker is valid JSON |
| scoped statement-blocker invariant assertions | 0 | identity, rank, blocked state, null target/imports/fingerprints, unchanged debt vector, false completion flags, changed paths, and absent worker packet agree |
| `git diff --check -- Stage1_Instances/THM-M-1374` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

The intake prerequisite is only worker-provisional `[_]`; its receipt is unaccepted and its
historical replay is stale on the integrated base. That dependency/freshness issue independently
prevents statement-node acceptance.

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable source and
scope reviewers must then preserve and hash an immutable primary or authoritative edition, select
one exact Noether theorem and direction, transcribe every incorporated definition and premise with
pinpoint locators, audit translation corrections and errata, resolve ownership against
`THM-M-1515`, and independently approve the source crosswalk. The selection must fix the
variational setting, independent and dependent variables, scalar field, regularity and derivative
order, group or infinitesimal action, finite-parameter or arbitrary-function symmetry class,
exact or divergence invariance, boundary conditions, Euler-Lagrange and on-shell conventions,
rank/effectiveness assumptions, current equivalence, conclusion, converse qualifications, and all
degenerate cases.

A later statement worker can then encode that same claim, minimize its pinned imports, freeze its
ordered binders, universes, and typeclass context, serialize and hash its elaborated expression and
environment, compile every credited transport, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no
debt-vector change is proposed. The assigned phase is not genuinely self-tested to its completion
gate, so no `.stage1-worker-selftest.json` is emitted and no statement-node receipt or master
acceptance is claimed.
