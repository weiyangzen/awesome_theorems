# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Historical Shimura lift | G. Shimura, *On modular forms of half integral weight*, Annals of Mathematics (2) 97 (1973), 440-481, DOI `10.2307/1970836` | `StatementShape` | Likely primary paper identified, but the repository has no immutable scan or exact theorem/page transcription; the identifier must be independently verified against the source |
| Half-integral source form | Same paper, definitions and hypotheses preceding the relevant correspondence theorem | `HalfIntegralWeightCuspFormData` | Legacy structure merely stores a function, coefficients, and propositions; it does not encode the metaplectic transformation law |
| Integral-weight target | Same paper's lift construction | `ShimuraLiftTarget.targetForm : CuspForm ...` | Ordinary mathlib target type is a useful candidate, but weight, group, character, and level are unconstrained in the legacy wrapper |
| Coefficient/series identity | Formula defining the lift in the selected primary theorem | proposition field `coefficientFormula` | No formula is represented; exact indices and normalization are open |
| Hecke compatibility | Corollary/eigenform portion of the selected source result | proposition field `heckeCompatibilityAwayFromLevel` | No operator or eigenform predicate is represented |
| Kohnen plus-space correspondence | W. Kohnen's later plus-space refinement (exact paper/theorem audit pending) | proposition field `kohnenPlusCondition` | Must not be folded into the 1973 root without an explicit source choice and checked transport |

The repository source record `Docs/researches/math_theorems.md` says only "lifting of modular forms",
attributes it to Shimura in 1973, and labels it verified. That label is untrusted metadata, not a
statement or proof receipt. The similarly named `THM-M-0129` is a distinct target and supplies no
scope or proof credit.

The likely paper citation above is a discovery lead, not H0 evidence. Before statement acceptance,
an auditor must obtain an immutable copy, verify its bibliographic identifier, select the exact
theorem/corollary, transcribe every parameter and convention, map assumptions and conclusions to
Lean binders, search corrections/errata, and obtain independent review. Until then the canonical
claim deliberately remains provisional and the human status is `H3`.
