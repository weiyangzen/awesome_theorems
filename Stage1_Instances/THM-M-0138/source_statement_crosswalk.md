# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Abelian localization for regular integral infinitesimal character | A. Beilinson and J. Bernstein, “Localisation de g-modules,” *C. R. Acad. Sci. Paris Sér. I Math.* 292 (1981), no. 1, 15-18 | future exact root; legacy `AbelianRegularIntegralStatementShape` | Primary announcement located, but theorem/page transcription, edition hash, assumptions, and errata review are not accepted: `H1` |
| Representation category | Same paper: modules governed by `U(g)` and a fixed central character | `UniversalEnvelopingAlgebra`; legacy `RepresentationSidePackage` | Only generic algebra/API scaffolding; it does not define the required central reduction or block |
| Geometric category | Same paper: modules over twisted differential operators on the flag variety | legacy `GeometrySidePackage` and mathlib scheme/sheaf APIs | Abstract package only; flag variety and twisted differential-operator sheaf are absent from the credited target |
| Localization/global sections equivalence | Same paper’s localization theorem and compatible dominance/regularity hypotheses | legacy `LocalizationBridge`, functor `IsEquivalence` conjunction | The categorical conclusion shape is plausible, but abstract functors plus proposition fields broaden the assumptions and are not the theorem |
| Derived or singular variants | Later localization literature; exact primary genealogy not audited here | none | Explicit non-target; cannot be used as a replacement closure |

The source uses conventions for the Harish-Chandra parameter and dot action that can move a
`rho`-shift between the weight, central character, and twisting parameter. “Dominant,” “regular,”
and the handedness of modules therefore require a literal source transcription and a convention
table before the statement is frozen. The theorem may also be presented as exactness plus unit and
counit isomorphisms rather than a single equivalence object; that packaging requires checked Lean
transports.

Discovery locator (not immutable evidence): bibliographic record for the 1981 note, volume 292,
pages 15-18. Follow-up must obtain a stable scan/hash, map every premise and conclusion to exact
page/formula locations, inspect corrections and later full expositions, and receive independent
review. No `H0`, exact-statement, or proof claim is made.
