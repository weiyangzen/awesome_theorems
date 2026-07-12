# Statement validation record

Item: `S56-M-0981-STATEMENT`  
Base revision: `32f565ebdf8b093386e287c150f0a2c7292903dc`

## Frozen target

`Stage1Instances.THM_M_0981.KolmogorovAxiomsTarget` is the exact intake-selected modern
probability-measure packaging of the empty-event, unit-mass, and countable-additivity clauses. It
quantifies over an arbitrary measurable sample type, normalized measures, and `Nat`-indexed
pairwise-disjoint measurable event families. Its sole direct import is
`Mathlib.MeasureTheory.Measure.ProbabilityMeasure`.

`PinnedCandidateSourceShape` directly expands the historical `S1_M_261.StatementShape`, while
`ProbabilityMeasurePackaging` checks the equivalent mathlib subtype encoding. Both relationships
are kernel-checked iff theorems. This phase does not credit the historical wrapper proof.

## Commands and results

All commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake artifacts; no dependency operation ran.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0981/Statement.lean` | 0 | exact target, two transports, four mutations, and empty-family boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0981/check_statement.py` | 0 | expression SHA-256 `1170cf6dac37cd1a8b7dfbda1a3cc3d22ddb94a5c3846f16d90dd27541766c2a`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0981/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `408aad...4b3`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

The final repository-structure, target-manifest, JSON, placeholder, and whitespace checks are
recorded in the worker self-test manifest after they run.

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of measurable-event
hypotheses, replacement of countable families by two-event families, existential relocation of the
event-family binder, and removal of probability normalization. The constant-empty family remains
in scope. An empty sample type is not excluded by an added premise; rather, normalization controls
whether a probability measure can inhabit it.

This is statement-only evidence pending master acceptance. It does not prove the Kolmogorov clauses
or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
