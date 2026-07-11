# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Every smooth manifold embeds smoothly in finite-dimensional Euclidean space | H. Whitney, "Differentiable Manifolds," *Annals of Mathematics* 37 (1936), 645-680, DOI `10.2307/1968482` | Intended future root expression | Primary historical source identified, but theorem/page wording, conventions, and errata have not received independent premise-level review: `H1` |
| Weak dimension bound `R^(2m+1)` | Whitney's embedding construction, to be pinpointed in the 1936 paper during source audit | Future alternate encoding | Stronger than the canonical existence-only claim; not frozen or credited at intake |
| Strong dimension bound `R^(2m)` | Later strong Whitney embedding formulation; exact primary publication must be pinned by source audit | Future alternate encoding | Source genealogy deliberately left open rather than attributed from memory |
| Smooth embedding means topological embedding plus injective differential | Standard modern differential-topology formulation; convention-level source mapping remains open | Candidate predicate assembled from `ContMDiff`, closed/topological embedding, and pointwise injective `mfderiv` | Semantic correspondence requires exact Lean inspection and checked bridges |
| Compact specialization | Modern compact-manifold specialization | `Mathlib.Geometry.Manifold.WhitneyEmbedding.exists_embedding_euclidean_of_compact` (name taken from a legacy discovery artifact) | Candidate anchor only. Exact declaration type and pinned revision are deferred; compactness cannot be added to close the general root |
| General noncompact branch | Historical unrestricted theorem | No accepted declaration identified at intake | Open machine boundary; absence is not proved by this intake |

The repository's source slogan, "a smooth manifold can be embedded in Euclidean
space," omits separation, countability, boundary, and dimension conventions.
This dossier makes the conventional Hausdorff, second-countable,
finite-dimensional reading explicit while keeping the dimension bound
existential. The statement phase must either validate that reading against a
pinpoint source or record a scope correction through the governed intake
process; it must not quietly substitute the compact mathlib theorem.

Discovery links, not immutable evidence receipts:

- Whitney 1936 DOI: <https://doi.org/10.2307/1968482>
- Candidate Lean module: `Mathlib.Geometry.Manifold.WhitneyEmbedding`
- Legacy discovery file: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_255.lean`

No `H0` or machine-closure claim is made. Follow-up requires a scan/hash of the
primary source, pinpoint theorem and premise mapping, errata search, exact
mathlib revision and declaration inspection, and independent review.
