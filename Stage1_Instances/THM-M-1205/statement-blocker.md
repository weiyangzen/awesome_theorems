# Exact-statement gate: blocked

Item: `S56-M-1205-STATEMENT`  
Base revision: `e0fbcaa7059e060c07df329438cbec38eba068d4`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. Its
entire mathematical claim is "a compactness method for conservation-law equations", attributed to
Tartar and Murat. Compensated compactness is a method family rather than one uniquely determined
proposition. The record does not choose among a div-curl lemma, weak continuity of a quadratic
form, Young-measure reduction, or a scalar conservation-law entropy compactness theorem.

Those choices have materially different domains, binders, hypotheses, and conclusions. Even after
choosing a family, the record does not fix the space dimension, domain, sequence and function
spaces, exponents, differential constraints and negative topology, flux and entropy regularity,
local versus global convergence, boundary conditions, or genuine-nonlinearity assumptions.
Selecting any values for these data would invent missing mathematics or substitute a convenient
theorem. The metadata label `已验证` is neither a source-statement identifier nor kernel evidence.

The intake therefore correctly remains at `[H4, M4, R4]`. This phase fails at the canonical human
claim identity gate, before minimal imports, an elaborated expression fingerprint, checked
transports, or meaningful removed-hypothesis/domain/binder/boundary mutations can be established.
No exact statement, statement acceptance, audit completion, or theorem completion is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_170.lean` is discovery input only. Its
`StatementShape` quantifies over `ConservationLawCompactnessData`, but that structure stores the
hard mathematical content in unconstrained proposition-valued fields named
`entropyProductionCompact`, `divCurlOrYoungMeasureReduction`, and `genuineNonlinearity`.
Consequently the module does not encode a source-selected compensated-compactness theorem. Its
successful elaboration establishes only that this historical abstract interface is type-correct in
the pinned environment; it supplies no rev-5.6 exact-statement credit and cannot determine minimal
imports for an unidentified target.

A scoped source search in pinned mathlib found no compensated-compactness, div-curl, Young-measure
compactness, or entropy-compactness declaration. The one textual match was an unrelated topological
entropy lemma whose name contains `isCompact`; it is not a candidate target. This observation is
discovery evidence only and does not replace the later anchor-audit phase.

## Required unblock

An accountable source reviewer must select one stable primary-source theorem and record its
edition, theorem/page, exact wording, referenced definitions, assumptions, and errata. The review
must freeze the theorem family, domain and dimension, function spaces and exponents, differential
constraints and topology, regularity and boundary hypotheses, ordered binders, conclusion, and
degenerate cases. A later statement worker can then encode that exact claim, minimize pinned
imports, serialize and hash its elaborated expression, check transports, and run the required
structural mutations.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 using only the existing pinned `.lake`
artifacts. No update, build, dependency fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1205` | 0 | rank 170, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_170.lean)` | 0 | legacy abstract interface elaborated and printed its declarations; no exact source target was established |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_170.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `eaf49b1a...0e7c` |
| `rg -n -i 'compensated compactness\|div.?curl\|young.measure.*compact\|entropy.*compact' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | one unrelated `coverEntropy...isCompact` substring match; no relevant declaration |

Known failures are the canonical source-statement identity, exact Lean target, minimal-import
determination, expression fingerprint, checked transports, and mutation tests. The assigned phase
is therefore not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted.
