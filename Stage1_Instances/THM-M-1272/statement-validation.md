# Statement validation record

Item: `S56-M-1272-STATEMENT`  
Base revision: `be286e95464895d6966301556151584a57536a1b`

## Frozen target

`Stage1Instances.THM_M_1272.FountainTheoremTarget` is the intake-selected classical Fountain
claim in a separable real Hilbert-space presentation. The sequence `e` is orthonormal and total;
`finiteCore e k` is the span below `k`, and `orthogonalTail e k` is its orthogonal complement.
The functional is even and `C1`, satisfies global Palais-Smale compactness, and obeys strict
two-radius Fountain geometry. The conclusion selects critical points whose values tend to infinity.

The two direct imports are the smallest checked pair among available pinned `.olean` artifacts. An
initial use of `Mathlib.Analysis.InnerProductSpace.Projection` failed because its `.olean` was
absent; no dependency build or `.lake` mutation was performed. The available `l2Space` import
supplies the orthogonal-submodule API.

## Commands and exact results

Commands ran in this worker clone on 2026-07-12; Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1272/Statement.lean` | 0 | target, components, four mutations, and unbounded-value consequence elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1272/check_statement.py` | 0 | expression SHA-256 `529bd5aeec0b1e9e58034f05dc03531a3fd9063547aeb54b68d5c0821d46cd31`; all mutations distinguished; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1272/Statement.lean lean-toolchain lake-manifest.json` | 0 | `da530b...1eec`, `651c8a...1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1272` | 0 | rank 165, planned, theorem incomplete |

## Boundary

The repository source says only "Fountain theorem" and "existence of multiple critical points".
Intake selected the classical Bartsch-Willem variant; this node formalizes that selection without
pretending the metadata supplies a source edition. The Hilbert presentation is a specialization of
the standard Banach/decomposition form, not a dual Fountain, Cerami, or PDE-corollary substitute.
Exact theorem/page and errata inspection remains an H-axis anchor-audit task.

The validator distinguishes removal of evenness, removal of Palais-Smale, weakening to one critical
point, and replacing divergent values with bounded ones. A total orthonormal family excludes zero
and finite-dimensional spaces; strict radius order is explicit. The checked
`tendsto_critical_values_unbounded` validates the advertised unboundedness reading without proving
the Fountain theorem.

This is statement-only evidence pending master acceptance. No theorem completion is claimed.
