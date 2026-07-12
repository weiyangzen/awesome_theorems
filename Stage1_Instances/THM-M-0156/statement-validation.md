# Statement validation record

Item: `S56-M-0156-STATEMENT`  
Base revision: `fa0980e32546eb9fdf401bc5ddad470ac23e506e`

## Frozen target

`Stage1Instances.THM_M_0156.DivergenceTheoremTarget` freezes the positive-dimensional rectangular
box form of the divergence theorem documented by the pinned mathlib module. For a vector field
continuous on `[a,b]`, Frechet differentiable throughout its open interior, and with integrable
coordinate divergence, the restricted volume integral of the derivative trace equals the signed
sum of upper-face minus lower-face integrals. This is exactly the volume-divergence/outward-flux
claim within the selected box scope; it is not advertised as an arbitrary regular-domain theorem.

The sole direct import is `Mathlib.MeasureTheory.Integral.DivergenceTheorem`. The canonical target
is a `def : Prop`, not a theorem containing proof evidence. `target_iff_expanded` kernel-checks its
binder-explicit form. Four separately elaborated mutations expose removal of continuity,
specialization to three-space, existential rebinding of the box, and exclusion of degenerate boxes.

## Commands and results

Commands ran inside this worker clone. Lean ran from `Formalizations/Lean` against the existing
pinned Lake environment; no update, fetch, build, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0156` | 0 | rank 655, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/Statement.lean` | 0 | canonical target, checked expansion, four mutations, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0156/check_statement.py` | 0 | expression SHA-256 `1107b156...bd790`; all four structural mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0156/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `b622de...9596`, `651c8a...b1d2`, and `321626...2d81` |

## Status boundary

This is statement-only evidence pending master acceptance. The exact historical or modern human
source pinpoint, anchor provenance and trust audit, proof-obligation graph, proof credit, hermetic
validation, and independent review remain open. No `H0`, `M0`, audit completion, or theorem
completion is claimed.
