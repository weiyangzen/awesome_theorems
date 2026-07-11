# Source-statement crosswalk

| Claim component | Repository source anchor | Lean target | Intake assessment |
|---|---|---|---|
| The named topic | `Docs/Stage0_Blueprint.md`, `THM-M-0607`: `光滑结构存在性` | none frozen | A topic label, not a proposition |
| Human wording | Same entry: `拓扑流形的光滑结构` | none frozen | Does not say which topological manifolds, in which dimensions, carry which compatible structure |
| Legacy Stage1 gloss | `Docs/Stage1_Blueprint.md`, `S1-M-254`: `拓扑流形的光滑结构` | a future namespace statement was requested generically | Discovery metadata only; the rev-5.6 manifest explicitly rejects inherited acceptance |
| Candidate low-dimensional theorem family | Moise's three-dimensional triangulation/smoothing results | unknown | Possible intended family, but restricting dimension would be substitution without a source pinpoint |
| Candidate high-dimensional theorem family | Kirby-Siebenmann obstruction theory for topological manifolds | unknown | Shows that hypotheses and dimension matter; no theorem/page/edition has yet been selected |
| Compatibility predicate | A smooth atlas inducing the given topology, with boundary/corners convention fixed | unknown | Must be defined before a Lean proposition can be elaborated |

## Fidelity boundary

The unrestricted sentence "every topological manifold admits a smooth structure" must not be
adopted: smoothability has genuine dimension-dependent obstructions. Conversely, this intake does
not choose a corrected theorem, because the repository source gives no authority for selecting a
dimension bound, PL hypothesis, or vanishing obstruction. The exact statement gate therefore fails
closed rather than manufacturing mathematics.

Candidate bibliography for later source discovery, not accepted evidence:

- E. E. Moise, *Geometric Topology in Dimensions 2 and 3*, Springer, 1977.
- R. C. Kirby and L. C. Siebenmann, *Foundational Essays on Topological Manifolds, Smoothings, and Triangulations*, Princeton University Press, 1977.

These citations identify relevant source families only. Later source audit must pin an edition,
theorem and page, assumptions, corrections/errata, and a node-specific premise crosswalk. Until
then the human status is `H4`; no source fidelity or machine theorem is claimed.
