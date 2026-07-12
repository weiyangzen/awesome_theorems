# Exact-statement gate: blocked

Item: `S56-M-1295-STATEMENT`  
Base revision: `8f4c72eeb09c3eab9ea2ef5a83d0bf48d59fdce6`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording available for `THM-M-1295` is the name "bubble decomposition" and
the phrase "asymptotic decomposition of critical problems". The record gives no author, primary
publication, theorem number or page, equation, or theorem family. The untrusted metadata label
`已验证` is not a source identifier and provides neither statement identity nor kernel evidence.

This wording admits inequivalent theorems, including Struwe-type global compactness for critical
elliptic Palais-Smale sequences, harmonic-map bubble trees, and nonlinear profile decompositions.
It does not determine the domain or manifold, dimension, boundary conditions, critical exponent,
energy space, equation and sign convention, solution and approximation predicates, subsequence,
finite or countable bubble indexing, scale and center conventions, parameter separation, remainder
topology, or energy/norm splitting formula. Choosing any such data would broaden or substitute the
source record rather than elaborate its exact claim.

The accepted intake correctly leaves these choices open and assigns `[H3, M4, R4]`. Its Struwe and
Lions references are explicitly discovery candidates whose exact theorem/page and assumptions have
not been inspected. Therefore the phase fails at canonical human-claim identity, before a Lean
expression, minimal pinned imports, expression hash, checked alternate encodings, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutations can exist. No exact statement, statement
acceptance, audit completion, or theorem completion is claimed.

## Existing Lean boundary

The only nearby repository module, `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_174.lean`, is a
legacy artifact for the distinct global-compactness target `THM-M-1294`. It elaborates an abstract
`SelectedStatementShape` over structures whose fields package arbitrary topology, energy,
admissibility, PDE predicates, compactification, and limit-passage conclusions. It does not state
bubbles, scale/center separation, remainder convergence, or an energy splitting identity, and it
cannot be substituted for `THM-M-1295`. Successful elaboration of that module checks only its
abstract interfaces. A scoped source search found no named bubble/profile decomposition,
concentration-compactness, Palais-Smale, or Struwe terminal theorem in pinned mathlib; this is only
negative discovery evidence, not completion of the later anchor-audit phase.

## Required unblock

An accountable source reviewer must select a stable primary-source edition and identify the exact
theorem/page, referenced definitions, full wording, assumptions, and errata. The review must freeze
the PDE or geometric system, domain and dimension, boundary conditions, exponent, spaces, ordered
binders, sequence hypotheses, solution predicate, bubble equations and parameters, indexing,
subsequence, convergence and separation clauses, splitting identities, and zero-bubble/boundary
cases. Only then can a statement worker encode that proposition, minimize pinned imports, preserve
and hash the elaborated expression, check transports, and run the four required mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 using the existing pinned toolchain and canonical
`.lake` artifacts. No update, build, dependency fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1295` | 0 | rank 463, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_174.lean)` | 0 | distinct legacy global-compactness interfaces elaborated; no exact `THM-M-1295` target established |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'bubble decomposition\|profile decomposition\|concentration.compactness\|palais.?smale\|struwe' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matches in pinned mathlib source |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and structural mutation
tests. The assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is
emitted.
