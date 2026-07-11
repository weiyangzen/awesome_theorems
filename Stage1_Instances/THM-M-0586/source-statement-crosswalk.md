# Source-statement crosswalk

## Candidate primary source

Stephen Smale, "Generalized Poincare's Conjecture in Dimensions Greater Than Four," *Annals of
Mathematics*, Second Series 74(2) (1961), 391-406, DOI `10.2307/1970239`, is the primary proof
source candidate. The bibliographic identity is frozen for discovery, but the article's exact
theorem number/page, definitions, hypotheses, and any errata have not yet been inspected. It is
therefore not `H0` evidence.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `n >= 5` | stable high-dimensional range | natural dimension plus inequality | included; source wording open |
| closed smooth `n`-manifold | compact boundaryless differentiable manifold | concrete manifold and compactness/boundary predicates | included; conventions open |
| homotopy equivalent to `S^n` | sphere recognition hypothesis | concrete sphere and homotopy equivalence | included; encoding open |
| homeomorphic to `S^n` | topological classification conclusion | `Homeomorph M (Sphere n)` or checked equivalent | included; exact sphere model open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_117.lean` is discovery evidence only. Its audited
adjacent APIs and any abstract terminal package do not establish the source theorem and must be
rechecked against the pinned revision. No legacy source label, wrapper, or successful compilation
is accepted as rev-5.6 statement or proof credit.

Before `H0`, an independent reviewer must inspect the primary article and verify the exact theorem
anchor, category, dimension range, all assumptions, definitions, conclusion, and known corrections,
then approve a row-by-row source-to-Lean mapping. Any alternate simply-connected homology-sphere
formulation requires checked two-way transport and may not silently replace the canonical claim.
