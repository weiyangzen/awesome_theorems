# Statement validation record

Item: `S56-M-0324-STATEMENT`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`

## Frozen target

`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` says that there exists a separable,
infinite-dimensional real Banach space with no `Nat`-indexed `SchauderBasis`. The local
`RealBanachSpace` structure bundles all instances so the existential contains no unresolved
typeclass metavariables. Its checked iff with `SigmaPresentation` is the only alternate encoding
credited at this phase.

Separability and non-finite-dimensionality exclude the two obvious substitutions: choosing a
nonseparable space whose density obstructs a countable basis, or choosing a finite-dimensional
degenerate carrier. `zeroSpaceBoundary` kernel-checks that the zero space is finite-dimensional and
thus outside the target. The stronger reflexive counterexample without the approximation property
is deliberately not encoded or credited: the intake records that exact source text and the
approximation-property object model remain downstream source/anchor obligations.

## Commands and results

Commands ran inside this worker clone. Lean ran from `Formalizations/Lean` with the existing pinned
Lake environment and canonical read-only build artifacts. No update, build, fetch, or dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0324/Statement.lean` | 0 | bundled target, checked sigma iff, four mutations, and zero-space exclusion elaborated; explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0324/check_statement.py` | 0 | expression SHA-256 `d69d1e5ebb004524a214e2f22608448f7a1a4df0ac1d46c002a38c309c157570`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0324/Statement.lean lean-toolchain lake-manifest.json lakefile.lean` | 0 | hashes `7e6c4b...f770`, `651c8a...1d2`, `321626...2d81`, and `43259b...cda`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | rank 820, planned, L0/rework-required, theorem incomplete |

## Mutation boundary

The validator compares explicit elaborated kernel expressions and distinguishes the target from
four changes: removing infinite dimension, changing the scalar field from `Real` to `Rat`, changing
existence to a universal claim, and replacing absence of every Schauder basis with failure of a
single specified sequence. These mutations cover a removed condition, changed domain, changed
binder scope, and a materially weakened conclusion.

This is statement-only evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, or release nodes and does not claim theorem completion.
