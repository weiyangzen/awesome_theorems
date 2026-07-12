# Statement validation record

Item: `S56-M-0982-STATEMENT`  
Base revision: `32f565ebdf8b093386e287c150f0a2c7292903dc`

## Frozen target

`Stage1Instances.THM_M_0982.ProbabilityContinuityTarget` is the exact selected event formulation.
It is the conjunction of continuity from below for increasing measurable events and continuity from
above for decreasing measurable events, over an arbitrary measurable space and probability measure.
Both conclusions use `Tendsto` at `atTop` in the topology of `ENNReal`. Its sole direct import is
`Mathlib.MeasureTheory.Measure.Typeclasses.Probability`.

The canonical target requires ordinary `MeasurableSet` events in both branches. The checked
`probabilityContinuityTarget_implies_historicalShape` transport reaches the historical candidate's
`NullMeasurableSet` above branch. The reverse direction is not credited. Pinpoint primary-source
review remains open, so this does not assert `H0`.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned `.lake` environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0982/Statement.lean` | 0 | canonical conjunction, checked historical transport, four mutations, and constant/empty/universal boundary declarations elaborated; explicit canonical declaration printed |
| `python3 ../../Stage1_Instances/THM-M-0982/check_statement.py` | 0 | expression SHA-256 `7ff4b7b4d50897c445c48b9d307a22590726bbbef6b6f8b064a8179d5d6cd088`; all four mutated expressions differed from the canonical expression |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0982/Statement.lean lean-toolchain lake-manifest.json` | 0 | `3ffa7f...0f72`, `651c8a...1d2`, `321626...d81`; values match `statement.json` |

## Mutation and boundary policy

The validator serializes explicit elaborated expressions and rejects identity with mutations that
remove measurability, specialize the domain to `Nat`, relocate the measurability premise, or require
strict rather than weak monotonicity. The last mutation excludes constant sequences. Kernel-checked
declarations retain constant sequences and exercise the empty-union and universal-intersection
boundaries. These tests distinguish statement structure; they do not claim a proof of the root.

This is statement-only evidence pending master acceptance. Anchor audit, obligation-tree, proof,
validation, release, human-source review, and theorem completion remain open.
