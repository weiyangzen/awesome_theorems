# Source-statement crosswalk

| Claim component | Repository source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Subject label | `Docs/researches/math_theorems.md`: "tau function", attributed to multiple authors, twentieth century | namespace `AwesomeTheorems.Stage1.S1_M_211` | Bibliographic metadata only; no author, paper, theorem, page, or assumptions |
| Stated content | "tau functions of integrable systems" | legacy `StatementShape` | Not a proposition: it does not select a hierarchy or say whether the claim is existence, representation, or characterization |
| Universal existence | No source supplied | `StatementShape`: every abstract model satisfying three proposition fields has a witness | Not accepted as a translation; the abstract fields do not provide a construction and may encode assumptions unrelated to a concrete integrable system |
| Hirota characterization | No equation, convention, or source supplied | `HirotaBilinearDatum.bilinearIdentity` | Predicate parameter only, not a formal Hirota identity |
| Reconstruction | No dependent-variable transform or nonvanishing domain supplied | `solutionReconstruction` | Arbitrary relation parameter only; no source correspondence |
| Finite determinant branch | Mentioned only as a legacy branch choice | finite matrix determinant APIs in mathlib | Plausible future restricted target, but no primary theorem or exact formula is frozen |

The source-statement map is therefore intentionally non-total. "Tau function" has incompatible
standard meanings across KP/Toda hierarchies, soliton determinant formulae, Fredholm determinants,
isomonodromic deformation, and algebraic-geometric constructions. Choosing one from general
knowledge would broaden or substitute the source entry rather than formalize it.

The statement phase requires a primary-source edition with theorem/equation/page, assumptions and
normalization, plus an errata search and independent review. Only then can it bind ordered Lean
quantifiers and test boundary mutations. The repository's `已验证` label is untrusted metadata and
provides neither `H0` nor machine-proof credit.
