# Full proof study — S5-CLM-00003519

## [PU-01] Exact proposition and semantic boundary

Hypotheses: none. The frozen proposition asks for one element of
`Arxiv.«2605.12342».gammaSubgroup 2 2` whose singleton subgroup closure is top.
Inference: `type_of%` checks both directions between the provider type and the
claim-owned surface in the provider environment. Output: the exact existential
proposition, with no weakened conclusion. Formal anchor: `source_to_target` and
`target_to_source` in `Statement.lean`. Downstream use: fixes the type proved by
the machine root. Exceptional case: the provider proof body has `sorryAx` and
is excluded. Trust boundary: the frozen provider supplies statement bytes only;
Master must re-elaborate the type and semantic environment.

## [PU-02] Choose the diagonal transposition

Hypotheses: `Fin 2` has the distinct elements `0` and `1`. Inference: set
`τ = Equiv.swap 0 1` and take the pair `(τ, τ)`. Output: a concrete candidate
generator. Formal anchor: `LEAN-GENERATOR` in `Proof.lean`. Downstream use: this
pair becomes the witness `g`. Exceptional case: choosing only one transposition
would give a mixed-sign pair and would not lie in the kernel. Trust boundary:
`Equiv.swap` is imported from the pinned provider environment, not redefined.

## [PU-03] Verify membership in the kernel

Hypotheses: both coordinates of the candidate are the same permutation `τ`.
Inference: `signDiffHom` evaluates to `sign τ * (sign τ)⁻¹ = 1`. Output: the
subtype proof that `(τ, τ)` belongs to `gammaSubgroup 2 2`. Formal anchor: the
proof field of `g` in `LEAN-GENERATOR`. Downstream use: makes `g` a legal
singleton generator. Exceptional case: no assumption about the numerical sign
of `τ` is needed for this diagonal membership. Trust boundary: the definitions
`gammaSubgroup` and `signDiffHom` are the exact provider declarations.

## [PU-04] Exhaust the permutations of Fin 2

Hypotheses: `σ` is an arbitrary permutation of `Fin 2`. Inference: the closed,
kernel-reducible decision proof enumerates the finite equivalences and yields
`σ = 1 ∨ σ = τ`. Output: a two-case classification for each coordinate. Formal
anchor: `hperm` in `LEAN-CLASSIFICATION`. Downstream use: produces four cases
for an arbitrary kernel element. Exceptional case: this is special to a
two-element type and is not asserted for larger symmetric groups. Trust
boundary: `decide`, not `native_decide`, is used, so no native-code oracle is
introduced.

## [PU-05] Remove the two mixed-sign pairs

Hypotheses: `(a,b)` lies in the kernel, and each of `a,b` is either `1` or `τ`.
Inference: unfolding the routed kernel and sign-difference definitions makes
the mixed cases contradictory because identity and the nontrivial transposition
have opposite signs. Output: the only possible values are `(1,1)` and `(τ,τ)`.
Formal anchor: the two contradiction branches in `LEAN-CLASSIFICATION`.
Downstream use: yields `x = 1 ∨ x = g`. Exceptional case: both diagonal cases
survive. Trust boundary: simplification uses provider/mathlib theorems that
Master must audit transitively at trust zero.

## [PU-06] Put both surviving elements in the closure

Hypotheses: `x = 1 ∨ x = g`. Inference: every subgroup contains `1`, while
`Subgroup.subset_closure` puts the member of `{g}` in its closure. Output:
`x ∈ Subgroup.closure {g}`. Formal anchor: the final two branches of
`rank_2_2_machine`. Downstream use: establishes top is below the closure.
Exceptional case: no separate power calculation is needed because the kernel
classification is exhaustive. Trust boundary: only standard subgroup closure
rules from the pinned environment are used.

## [PU-07] Conclude equality with top

Hypotheses: every element of the ambient kernel subgroup lies in the closure of
`{g}`. Inference: `top_unique` turns the inclusion `⊤ ≤ closure {g}` into
equality. Output: `Subgroup.closure {g} = ⊤`, completing the existential root.
Formal anchor: the `top_unique` composition in `rank_2_2_machine`. Downstream
use: discharges the frozen provider proposition and its Stage6 alias.
Exceptional case: equality is of subgroups of the exact routed gamma subtype,
not a cardinality proxy. Trust boundary: canonical acceptance still requires
Master compilation, exact axiom reporting, replay, and adversarial mutations.

## Reverse coverage

Every mathematical paragraph above maps to one distinct proof-DAG node and one
content-addressed anchor in `readability-review.json`. Generated declaration
inventories live in JSON and are intentionally not duplicated here.
