# Source-statement crosswalk

## Repository source record

The target is generated from `Docs/researches/math_theorems.md`, whose complete mathematical wording
is `向量场散度在体积上的积分` (the integral of a vector field's divergence over a volume). The same
record attributes the theorem to Mikhail Ostrogradsky and dates it to 1826. `Docs/Stage0_Blueprint.md`
repeats that wording but explicitly leaves the precise definitions and hypotheses open. Its
`已验证` label is untrusted metadata under rev-5.6 and supplies neither `H0` nor machine credit.

## Human-source candidates

- Mikhail Ostrogradsky's 1826-era work is the historical-source lead carried by the repository.
  The exact memoir title, publication edition, page, formulation, and assumptions have not been
  verified and must not be invented from the attribution.
- A modern analysis or differential-geometry source stating the Euclidean divergence theorem may
  be selected as the authoritative statement source. The statement phase must record an exact
  edition, theorem/page, definitions, hypotheses, and errata before it can improve `H1`.

These are source-audit tasks, not citations sufficient for `H0`.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| `散度定理` | divergence/Gauss--Ostrogradsky theorem | `DivergenceTheoremTarget` | exact box-scoped type selected |
| vector field | map from the ambient domain into its Euclidean tangent space | `f : (Fin (n+1) -> Real) -> (Fin (n+1) -> Real)` | included |
| divergence | trace of the derivative/Jacobian | sum of `f' x (Pi.single i 1) i` | included |
| volume integral | integral of divergence over `Omega` | restricted product-Lebesgue integral on `Icc a b` | included |
| boundary flux | outward normal component integrated over `boundary Omega` | upper-face component integral minus lower-face component integral | included for boxes |
| equality | volume divergence equals outward boundary flux | exact Lean equality with signed orientation | included and elaborated |

## Lean discovery crosswalk

The pinned local file
`Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DivergenceTheorem.lean`
documents and proves a box theorem. Its public declaration
`MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable` assumes `a <= b`, continuity on the
closed box, a Frechet derivative away from a countable exceptional set in the interior, and
integrability of the coordinate divergence; its conclusion is a signed sum of face integrals.
Related declarations include
`MeasureTheory.integral_divergence_prod_Icc_of_hasFDerivAt_of_le` and
`MeasureTheory.integral2_divergence_prod_of_hasFDerivAt`.

This is real pinned discovery evidence and likely closes a rectangular formulation once exact-type,
axiom, provenance, and source-scope checks are run. It is not yet an accepted anchor audit and does
not by itself establish that the repository's intended theorem is restricted to boxes.

Before `H0`, an independent reviewer must verify the selected human source and the mapping of every
domain, regularity, orientation, measure, boundary, and degeneracy assumption. Before any `M0`
claim, the statement and anchor phases must elaborate the exact target and inspect the terminal
declaration and its transitive trust/provenance closure.
