# Statement validation record

Item: `S56-M-0353-STATEMENT`  
Base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`

## Frozen target

`Stage1Instances.THM_M_0353.HermiteCompletenessTarget` fixes the complex-valued Hermite
functions on the real line with Lebesgue measure. It uses mathlib's probabilists' polynomial
`He_n = Polynomial.hermite n` and the equivalent normalized function

`pi^(-1/4) / sqrt(n!) * He_n(sqrt(2) x) * exp(-x^2/2)`.

The target first requires every literal function to be in complex `L^2`, then requires a
`HilbertBasis Nat Complex` whose vectors agree almost everywhere with those functions. Thus the
orthonormality and completeness are supplied by the basis structure without assuming either as a
hypothesis. Index zero, every natural index, almost-everywhere quotient equality, and the entire
unweighted Lebesgue `L^2` space are included. Finite truncations, Gaussian-weighted measure,
abstract unidentified bases, and merely one matching index are excluded.

The three direct mathlib imports expose respectively the polynomial convention, complex `Lp`, and
`HilbertBasis`; `Mathlib.MeasureTheory.Measure.Lebesgue.Basic` is additionally necessary to install
the canonical Lebesgue `MeasureSpace Real` instance used by `volume`.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` artifacts.
No update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0353/Statement.lean` | 0 | exact target and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0353/check_statement.py` | 0 | source SHA-256 recorded; canonical components and four mutations present |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-0353/Statement.lean lean-toolchain lake-manifest.json` | 0 | `58416b...2d99`, `651c8a...b1d2`, `321626...5cb2` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets valid |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | rank 846, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0353` | 0 | no whitespace errors |

## Gate boundary

The removed-integrability, changed-measure, changed-binder-scope, and finite-truncation forms are
separate elaborated propositions and the checker ensures they cannot silently replace the frozen
source text. They are structural mutation fixtures, not claims that Lean has proved mathematical
non-equivalence.

This is self-tested statement-only evidence pending master acceptance. It proves neither
integrability nor the basis theorem and does not advance anchor-audit, obligation-tree, proof,
validation, or release nodes. Human-source review and checked transports to other normalizations
remain downstream work; no H0, M0, R0, audit completion, or theorem completion is claimed.
