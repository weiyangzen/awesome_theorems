# Source-statement crosswalk

| Claim component | Repository source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| The title "Gromov embedding theorem" | Stage0 metadata, attributed to Mikhail Gromov and dated 1986 | No unique declaration | Insufficient bibliographic identity: `H5` |
| "Necessary-and-sufficient condition for metric-space embedding" | Generated Stage0 and legacy Stage1 wording; no definitions of embedding or target class | `IsometricallyEmbedsIn X E` in legacy `S1_M_132.lean` | The wording does not fix isometric/topological/smooth embedding, the target, or metric-space class |
| Separable metric space embeds isometrically into `l-infinity(N, R)` | No primary-source crosswalk in target metadata | `KuratowskiEmbedding.exists_isometric_embedding` and legacy wrapper `exists_isometric_embedding_linfty` | Genuine candidate discovered locally, but it is a sufficient existence theorem and is commonly Kuratowski's construction; it cannot be substituted for an unidentified Gromov iff theorem |
| Equality in compact Gromov-Hausdorff space characterizes isometry | No matching source claim identified | `GromovHausdorff.toGHSpace_eq_toGHSpace_iff_isometryEquiv` | Adjacent theorem, not accepted as the root |
| Negative-type criterion for Hilbert embedding | Possible reading of "necessary-and-sufficient condition" | No candidate accepted | Usually associated with Schoenberg; source identity and intended codomain are missing |
| Differential-geometric/h-principle embedding | Category says differential geometry and date says 1986 | Legacy file lists nonselected variants | Plausible title context, but metadata lacks manifold relation, regularity, dimension, codimension, and topology hypotheses |

No primary mathematical source is accepted at intake. The apparent combination of a Gromov
attribution, a 1986 date, a differential-geometry category, and generic metric-space iff wording is
not enough to reconstruct a unique claim. Later work must locate the originating catalogue/source
record or an identifiable Gromov publication with a pinpoint statement and then map every premise
and conclusion component. It must also audit edition, page/theorem number, corrections, and errata.

The legacy Lean module is useful negative evidence: it explicitly says that it selected the
Kuratowski branch by disambiguation and did not claim a terminal proof of every theorem bearing the
name. It remains unaccepted discovery material under the uniform L0/rework baseline.
