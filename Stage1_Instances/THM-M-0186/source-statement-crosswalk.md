# Source-statement crosswalk

## Source anchors

- Fernando C. Marques and Andre Neves, "Min-max theory and the Willmore conjecture",
  *Annals of Mathematics* (2), volume 179 (2014), number 2, pages 683-782. This is the published
  proof source and a candidate for the principal theorem anchor. Pinpoint theorem wording,
  assumptions, and errata have not yet received independent dossier review.
- Thomas J. Willmore, "Note on embedded surfaces", *Analele Stiintifice ale Universitatii
  \"Al. I. Cuza\" din Iasi*, Sectiunea I a, Matematica (N.S.) 11B (1965), pages 493-496. This is a
  historical formulation anchor; its exact normalization and scope still require inspection.

These bibliographic records support `H1`, not `H0`. Neither is Lean evidence.

## Claim crosswalk

| Repository/intake component | Mathematical role | Required Lean object | Intake status |
|---|---|---|---|
| "torus Willmore-functional lower bound" | `W(f) >= 2*pi^2` | ordered inequality in `Real` | root claim frozen |
| smooth immersed two-torus | quantification domain | smooth compact torus and immersion into Euclidean `R^3` | human scope frozen; API open |
| `H = (k1+k2)/2` | fixes the constant's convention | scalar mean curvature derived from the immersion | frozen convention; API open |
| `integral H^2 dA` | Willmore functional | induced area measure and integrable curvature function | formula frozen; elaboration open |
| Marques-Neves spherical result | main published proof route | round `S^3`, embedded surface, genus and area theorem | source pinpoint/Lean bridge open |
| conformal invariance | relates Euclidean and spherical formulations | checked stereographic/conformal energy transport | open |
| non-embedded immersion case | prevents weakening to embeddings | exact reduction, commonly via multiplicity estimates | source anchor and formal bridge open |

## Fidelity boundary

The modern proof is often stated for embedded closed surfaces of positive genus in the round
three-sphere, while the classical conjecture is phrased for immersed tori in Euclidean space. Those
are not definitionally the same statement. The statement and obligation phases must identify every
hypothesis and prove the transports rather than using shared theorem names as equivalence evidence.

Before `H0`, an independent reviewer must verify the selected editions, pinpoint theorem numbers or
pages, definitions of mean curvature and energy, embedded/immersed hypotheses, equality statement,
errata, and the row-by-row route to the canonical claim.

## Repo-local formal-artifact boundary

A scoped search of repository Lean sources for `Willmore` and `Clifford torus` found no target
declaration. Hits for `mean curvature` concern other theorems and do not establish a usable Willmore
interface. This is preliminary intake discovery only; the pinned mathlib/external audit belongs to
`S56-M-0186-ANCHOR_AUDIT`.
