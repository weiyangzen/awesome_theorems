# Exact-statement gate: blocked

Item: `S56-M-1294-STATEMENT`  
Base revision: `68e663d8ce85727d9e1baf107d3b32eb7a434ba8`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. Its
entire mathematical wording is "global compactness" and "compactification of noncompact
problems". The record names no author, publication, theorem, equation, or theorem family. Although
the neighboring queue entries and the intake make a Struwe/Lions-style critical-PDE bubble or
profile decomposition a plausible discovery hypothesis, they do not identify one proposition.

Even within that family, the record does not fix the elliptic or variational problem, domain or
manifold, dimension, boundary condition, critical exponent, function and dual spaces, solution or
Palais-Smale predicate, boundedness assumptions, profile equations, translation/dilation
parameters, finite or countable profile indexing, convergence topologies, separation conclusion,
or norm/energy splitting formula. Different choices produce inequivalent global compactness
theorems. Selecting Struwe's critical elliptic theorem, a Lions concentration result, or a profile
decomposition would therefore invent missing mathematics rather than elaborate the exact target.
The metadata label `已验证` is neither a source identifier nor kernel evidence.

The intake explicitly leaves the primary theorem, equation, domain, hypotheses, and decomposition
formula open and assigns `[H3, M4, R4]`. Consequently this phase fails at the canonical human-claim
identity gate, before minimal imports, an elaborated expression fingerprint, checked transports,
or meaningful hypothesis/domain/binder/boundary mutations can be established. No exact statement,
statement acceptance, audit completion, or theorem completion is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_174.lean` is discovery input only. Its
`SelectedStatementShape` universally quantifies over an arbitrary `ProfileCompactnessMechanism`
and `GlobalCompactnessProblem`. Those structures package the compact profile space, energy bound,
coercivity, regularity, weak/classical bridge, limit candidate, and limit-solution conclusion as
fields or unconstrained propositions. The resulting implication neither states a concrete PDE nor
exposes bubbles, their parameters, separation, remainder convergence, or energy splitting. It
cannot be substituted for a source-selected global compactness theorem.

The legacy module elaborates successfully in the pinned environment, proving only that its abstract
interfaces and adjacent compactness wrappers are type-correct. Its ten broad imports cannot be
called minimal imports for an unidentified exact target. A scoped search of pinned mathlib found no
declaration or source text for global compactness, Struwe compactness, Palais-Smale bubble
decomposition, or profile decomposition; this is discovery evidence, not the assigned later anchor
audit.

## Required unblock

An accountable source reviewer must identify a stable primary source by edition, theorem/page,
exact wording, referenced definitions, assumptions, and errata. The review must freeze the PDE and
sign convention, domain and dimension, boundary conditions, critical exponent, spaces, ordered
binders, sequence hypotheses, solution predicate, profile equations and parameters, indexing,
convergence and separation clauses, energy/norm identities, and zero-profile and boundary cases. A
later statement worker can then encode that exact claim, minimize pinned imports, print and hash the
elaborated expression, check transports, and run structural mutations.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 using only the existing canonical pinned `.lake`
artifacts. No update, build, dependency fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1294` | 0 | rank 174, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_174.lean)` | 0 | legacy abstract interfaces elaborated; printed `SelectedStatementShape : Prop`; no exact source target established |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_174.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `9d5ce578...a88` |
| `rg -n -i 'global compactness\|struwe\|palais.?smale\|bubble decomposition\|profile decomposition' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matches in pinned mathlib source |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is therefore not self-tested or complete, so no `.stage1-worker-selftest.json` is
emitted.
