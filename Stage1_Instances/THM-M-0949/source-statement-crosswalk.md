# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6931-6936` supplies exactly the title
`密度Hales-Jewett定理`, attribution Hales/Jewett/Furstenberg/Katznelson, the year 1991, the gloss
`组合线的存在性` ("existence of a combinatorial line"), importance "high," and status
`已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record omits the alphabet, dimension, subset,
density threshold, all binders and hypotheses, the exact conclusion, a bibliography, a proof
boundary, corrections, and formal artifacts.

`Docs/Stage0_Blueprint.md:25876-25901` repeats the gloss and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only
as untrusted source metadata and resets the target to `L0 / rework_required`.

## Inspected proof source

D. H. J. Polymath, *A new proof of the density Hales-Jewett theorem*, Annals of Mathematics
175 (2012), 1283-1327, DOI `10.4007/annals.2012.175.3.6`, is an accessible primary proof source.
Theorem 1.4 on page 1285 gives the finite word-cube statement recorded in `scope-map.md`.
The text on pages 1283-1285 defines `[k] = {1, ..., k}`, subsets of `[k]^n`, density
`|A| / k^n`, and a
combinatorial line via a nonempty wildcard coordinate set. The paper says that Furstenberg and
Katznelson first proved the theorem in 1991 and supplies a new complete elementary proof.

The inspected publisher PDF is hashed in the provisional receipt. No `H0` claim follows: the
repository did not select this edition, the original Furstenberg-Katznelson article (*Journal
d'Analyse Mathematique* 57 (1991), 64-119, DOI `10.1007/BF03041066`) was identified but not fully
inspected, the source genealogy and errata have not been audited, and no independent reviewer has
accepted a definition-by-definition and premise-by-premise crosswalk.

## Component crosswalk

| Catalog/source component | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| positive integer `k` | nonempty alphabet `[k]` | `Fin k` with `0 < k`, or checked equivalent finite type | encoding and transport open |
| positive real `delta` | lower density threshold | `delta : Real`, `0 < delta` | exact density codomain/casts open |
| positive threshold `dhj(k, delta)` | uniform dimension cutoff | `N : Nat`, possibly `0 < N` | positivity convention open |
| every `n >= N` | word-cube dimension | `Fin n -> Fin k` | exact binder order open |
| subset `A` | selected words | `Finset (Fin n -> Fin k)` or finite `Set` | representation open |
| density at least `delta` | `|A| / k^n >= delta` | real cast of cardinal quotient or `Finset.dens` with checked cast | exact normalization open |
| combinatorial line | fixed coordinates plus nonempty wildcard set, all points in `A` | `l : Combinatorics.Line (Fin k) (Fin n)` and `forall x, l x in A` | containment predicate must be frozen |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.HalesJewett` defines `Combinatorics.Line`, whose `proper` field requires at
least one wildcard coordinate, and proves `Combinatorics.Line.exists_mono_in_high_dimension`, the
ordinary coloring Hales-Jewett theorem. `Mathlib.Data.Finset.Density` supplies `Finset.dens` as a
nonnegative-rational finite-set density. A bounded search over pinned mathlib and repo-local Lean
found no `density Hales-Jewett` or `DHJ` declaration. This is intake discovery, not an exhaustive
immutable external anchor audit and not a global absence claim.

`IntakeProbe.lean` checks the adjacent declarations and elaborates the candidate binder shape with
`Finset.dens` converted to `Real`. It declares no theorem and proves no instance of the candidate
shape. Ordinary Hales-Jewett cannot receive density-root credit by name similarity.

Before leaving `H1`, accountable reviewers must preserve an immutable complete source edition,
inspect the original-proof and correction history, adopt the exact proposition, map every
incorporated definition, binder, hypothesis, conclusion, and degenerate case, and independently
approve the crosswalk. Only the later statement phase may freeze minimal imports, a canonical Lean
expression and environment fingerprint, checked transports, and the required statement mutations.
