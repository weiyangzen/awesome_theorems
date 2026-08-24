# Proof outline and exact readable fragments

## Fragment N01 — exact root

The target is the exact pinned proposition: there exists g in gammaSubgroup 2 2 whose singleton closure is top.

Input and hypothesis: the frozen declaration in the exact provider module.
Inference: elaborate the qualified proposition without aliases or substituted
imports. Output: the target existential. Formal anchor:
`Statement.lean:source_to_target_statement`. Downstream use: N07 and the
statement crosswalk. Exceptional case: the provider theorem has `sorryAx`, so
only its statement bytes are trusted. Trust boundary: the new local proof must
close the root independently.

## Fragment N02 — two permutations

Let tau be the transposition of 0 and 1. Exhaustive finite computation proves every permutation of Fin 2 is either identity or tau.

Input: an arbitrary permutation of `Fin 2`. Inference: kernel-checked finite
exhaustion. Output: the two-case classification. Formal anchor:
`Proof.lean:permutation_cases`. Downstream use: witness construction and both
coordinate splits. Exceptional case: no claim about permutations of any larger
type is made. Trust boundary: Lean checks the reflected decision certificate.

## Fragment N03 — diagonal witness

The diagonal pair (tau,tau) lies in gammaSubgroup 2 2 because signDiffHom evaluates to sign(tau) times its inverse, hence one.

Input: the transposition. Inference: unfold the exact pinned kernel definition
and cancel equal coordinate signs. Output: a subtype witness `g`. Formal
anchor: `Proof.lean:g`. Downstream use: N06 and N07. Exceptional case: mixed
pairs are not witnesses. Trust boundary: provider definitions are exact source
bytes, while their unrelated theorem bodies carry no credit.

## Fragment N04 — four cases

For an arbitrary subgroup element x, classify both permutation coordinates independently as identity or tau.

Input: `x : gammaSubgroup 2 2`. Inference: apply N02 to each projection.
Output: `(1,1)`, `(1,tau)`, `(tau,1)`, or `(tau,tau)`. Formal anchor:
`Proof.lean:coordinate-rcases`. Downstream use: N05 and N06. Exceptional case:
both orientations of a mixed pair remain separate. Trust boundary: exhaustion
is formal, not a cardinality assertion in prose.

## Fragment N05 — mixed cases

The mixed coordinate cases contradict x membership in the kernel: their sign difference is negative one rather than one.

Inputs: one mixed coordinate equality and `x.2`, the kernel equation.
Inference: substitute the coordinates, unfold `signDiffHom`, and simplify.
Output: contradiction for both mixed orientations. Formal anchor:
`Proof.lean:mixed-kernel-branches`. Downstream use: N06. Exceptional cases:
identity/tau and tau/identity are discharged independently. Trust boundary:
Lean derives each contradiction from the pinned definition.

## Fragment N06 — closure

Thus x is either the identity, already in every subgroup, or the chosen diagonal generator, which belongs to its singleton closure.

Inputs: N03–N05. Inference: subtype extensionality identifies the surviving
pairs, then `Subgroup.one_mem` or `Subgroup.subset_closure` establishes closure
membership. Output: every subgroup element is in `closure {g}`. Formal anchor:
`Proof.lean:identity-and-generator-branches`. Downstream use: N07. Exceptional
case: the two survivors use different closure facts. Trust boundary: only the
foundation subgroup API is used.

## Fragment N07 — root

Every x belongs to the singleton closure, so top_unique gives closure {g} = top and the existential target follows.

Inputs: the valid witness and N06. Inference: apply `Subgroup.top_unique`, then
package the witness. Output: the exact unconditional root. Formal anchor:
`Proof.lean:rank_2_2`. Downstream use: provisional release and the frozen Stage6
alias. Exceptional case: this proves the formal cyclic-generation conclusion;
it does not separately formalize minimal-rank terminology. Trust boundary:
trust-zero kernel elaboration checks the complete composition.
