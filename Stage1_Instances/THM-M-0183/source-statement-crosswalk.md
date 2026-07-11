# Source-statement crosswalk

## Primary-source anchors

- S.-T. Yau, "On the Ricci curvature of a compact Kahler manifold and the complex
  Monge-Ampere equation, I", *Communications on Pure and Applied Mathematics* **31** (1978),
  339-411, DOI `10.1002/cpa.3160310304`. This is the primary proof source.
- E. Calabi, "On Kahler manifolds with vanishing canonical class", in *Algebraic Geometry and
  Topology: A Symposium in Honor of S. Lefschetz*, Princeton University Press (1957), 78-89.
  This is a primary formulation source for the conjectural Ricci prescription/uniqueness problem.

These are discovery anchors only. Stable copies, exact theorem/page labels, invoked definitions,
and errata have not yet been independently checked, so this intake does not claim `H0`.

## Crosswalk

| Root component | Source-side role | Lean-side obligation | Intake status |
|---|---|---|---|
| compact Kahler manifold | analytic domain of Yau's theorem | complex manifold, Kahler structure, compactness | frozen semantically; encoding open |
| `c1(X)=0` in real cohomology | specializes prescribed Ricci form to zero | define tangent-bundle first Chern class and coefficient map | frozen semantically; encoding open |
| every Kahler class `kappa` | fixes the cohomology class of the solution | positive closed `(1,1)` class and representative relation | included, not optional |
| Ricci-flat Kahler metric | zero prescribed Ricci form/tensor | construct metric and checked tensor/form equivalence | frozen semantically; encoding open |
| uniqueness in a fixed class | part of the stronger classical theorem | would require equality/modulo-potential formulation | contextual; excluded from root credit |

## Repository metadata boundary

`Docs/researches/math_theorems.md` supplies only the name, proposer, broad gloss "existence of a
Ricci-flat metric on a compact Kahler manifold", and an untrusted `已验证` label. It omits the
vanishing-`c1` hypothesis and prescribed Kahler class; it is discovery metadata, not proof or exact
source evidence. `Docs/Stage1_Blueprint.md` repeats that gloss and explicitly marks the target as not
completed. A later source audit must ensure the frozen corollary follows from the exact cited source
statement without importing modern extra hypotheses.

