# Statement validation record

Item: `S56-M-1061-STATEMENT`  
Base revision: `7ed5103bae419111bef3d397f525a727b98670d3`

## Frozen target

`Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget` is the intake-selected
bounded-continuous integral lemma. It quantifies over a nonempty Polish space,
probability measures satisfying explicit full LDP bounds at strictly positive
speeds tending to zero, a good `ENNReal`-valued rate function, and a bounded
continuous real test function. The logarithmic integral and variational value
live in `EReal`, preserving the zero/infinite boundary conventions.

`ExpandedTarget` unfolds the locally defined LDP, good-rate, and logarithmic
integral interfaces. The theorem
`varadhanIntegralLemmaTarget_iff_expandedTarget` checks this transport by
definitional equality. Removing each of the three imports separately failed,
while the initially included `Mathlib.Topology.MetricSpace.Polish` import was
successfully removed; the final imports are therefore minimal under this test.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1061/Statement.lean` | 0 | canonical target, expanded-target iff, and four mutations elaborated; explicit root expression printed |
| `python3 ../../Stage1_Instances/THM-M-1061/check_statement.py` | 0 | expression SHA-256 `681a5c8fcbefe363119923dd4424876a37b90d0418e715ff46daf781b5e32119`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1061/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `19f51d...0af1`, `651c8a...1d2`, and `321626...2d81` |
| remove each direct import and run `lake env lean /tmp/THM-M-1061-import-test.lean` | 1 for each retained import | `ENNReal.log`, lintegral syntax, or `IsProbabilityMeasure` became unavailable; the redundant Polish import was removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, planned, hard anchor/wrapper lane, theorem incomplete |

## Mutation and boundary policy

The validator compares fully explicit elaborated expressions and distinguishes
removal of the good-rate premise, specialization from an arbitrary Polish space
to `Real`, movement of the bound outside the test-function binder, and admission
of zero speed with the LDP bounds omitted. The nonempty instance and strictly
positive speed premises exclude the two intake boundary ambiguities. Extended
real codomains make zero/infinite logarithmic values explicit rather than hiding
them behind a partial real logarithm.

This is statement-only evidence pending master acceptance. It does not prove
Varadhan's lemma or advance anchor-audit, obligation-tree, proof, validation, or
release nodes.
