# Source-statement crosswalk

## Primary-source candidates

- Charles A. Weibel, *An Introduction to Homological Algebra*, Cambridge Studies in Advanced
  Mathematics 38, Cambridge University Press, 1994, section 1.3, especially the long exact sequence
  associated to a short exact sequence of chain complexes. Edition-page, theorem number, definitions,
  and errata must be checked against a stable copy before H0.
- Saunders Mac Lane, *Homology*, Springer, 1963, the chapter on exact sequences and the connecting
  homomorphism. This is an independent classical source candidate; a pinpoint statement and edition
  check remain open.

These are discovery citations, not evidence receipts and not an H0 source audit.

## Statement crosswalk

| Repository/source phrase | Mathematical content to preserve | Lean-side consequence | Intake state |
|---|---|---|---|
| short exact sequence | degreewise exact `0 -> A -> B -> C -> 0` of complexes, with compatible chain maps | a short complex of homological complexes plus categorical short-exactness | included; exact encoding open |
| induces | connecting morphisms are constructed from the short exact sequence, not assumed | use or construct the boundary map and retain its provenance | required |
| homology | homology in each degree of the three complexes | explicit complex shape, adjacent indices, and homology functor/API | required |
| long sequence | the pattern continues across all applicable degrees | quantify over degrees or assemble an indexed exact sequence; one isolated window is insufficient | required |
| exact | every consecutive composable pair has image equal to kernel | categorical exactness obligation at all three repeating positions | required |

## Existing Lean discovery boundary

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_096.lean` imports mathlib homology
sequence modules and contains wrappers around connecting-morphism and exactness declarations. It is
useful discovery input for the later anchor audit. Its `StatementShape` packages a local adjacent
window, so statement identity with the full continuing source claim has not yet been established.
No declaration, proof body, axiom report, or build result from that file is accepted by this intake.

Before H0, a reviewer must pin a primary edition, record the exact theorem/page and invoked
definitions, check errata, and map every premise, grading convention, connecting-map direction,
exactness location, and naturality clause to the canonical claim.
