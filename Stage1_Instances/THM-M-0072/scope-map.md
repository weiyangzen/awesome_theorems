# Scope map

## Preserved theorem family

The intake preserves the finite-group transfer/conjugacy theorem family named by the catalog. The
leading source identification is Thompson 1968, Lemma 5.38(a)(i): in a finite even-order group with
no subgroup of index two, involutions in a Sylow 2-subgroup can be conjugated into each maximal
subgroup of that Sylow subgroup. This is the proposed source scope, not yet the accepted canonical
proposition.

The source theorem relates local Sylow-subgroup structure to ambient-group conjugacy through the
transfer homomorphism. The repository's generic local/global gloss is too weak to determine that
claim on its own; the title-to-source crosswalk and the catalog date conflict require review.

## Decisions required at statement freeze

1. Approve Thompson 1968 Lemma 5.38(a)(i) as the root represented by the catalog title, or record a
   different pinpoint primary source rather than choosing from memory.
2. Decide whether the canonical root is the exact printed universal statement, Lynd's restricted
   `u ∉ M` form, or a package with an explicit checked relationship between them.
3. Fix finite-group and even-order encodings, the subgroup-index convention, and whether
   "2-perfect" is a defined abbreviation or the literal no-index-two premise.
4. Represent a Sylow 2-subgroup and a maximal proper subgroup without losing the nested coercions
   from `M` to `S` to `G`.
5. Fix involution as order exactly two, rather than merely `u ^ 2 = 1`, and state ambient `G`
   conjugacy with an explicit witness or `IsConj`.
6. Decide the quantifier order over the Sylow subgroup, maximal subgroup, involution, and conjugacy
   witness, including every typeclass and finiteness dependency.
7. Decide whether Lemma 5.38(a)(ii) and (b) are out of scope, alternate consequences, or separate
   obligations, and map any incorporated Definition 2.8 notation.
8. Freeze the foundation, TCB, computation, source preservation, and correction profiles, then add
   checked transports for every credited alternate encoding.

## Degenerate and boundary cases

Source and statement review must explicitly address the trivial group; odd-order groups; groups of
order two; the difference between absence of any index-two subgroup and perfectness; a trivial or
order-two Sylow subgroup; maximal subgroups including the bottom subgroup; an involution already in
the maximal subgroup; an element satisfying `u ^ 2 = 1` but equal to the identity; coercions between
the nested subgroup carriers; and whether conjugacy is written `g⁻¹ug`, `gug⁻¹`, or via `IsConj`.

No case is excluded at intake. Thompson's even-order premise and universal quantification must not
be deleted merely because a restricted formulation makes some cases vacuous or immediate.

## Explicit substitutions excluded

- Burnside's normal `p`-complement theorem assumes a normalizer-centralizer condition and concludes
  existence of a normal complement; it is not Thompson's conjugacy-into-a-maximal-subgroup lemma.
- The focal subgroup theorem identifies an intersection with a focal subgroup; it is related
  transfer infrastructure, not the requested conjugacy conclusion.
- `Group.IsPerfect` is stronger than the no-index-two or 2-perfect premise and cannot replace it.
- A theorem about odd-order solvability, all local subgroups being solvable, control of fusion,
  strongly closed subgroups, or a fusion-system generalization is not the classical group lemma.
- Lemma 5.38(a)(ii) or (b) alone, a single maximal subgroup, a special finite group, or only
  involutions already in the maximal subgroup does not close the printed universal clause.
- A structure that stores the desired conjugacy witness, an assumed transfer formula, an unchecked
  theorem name, or the catalog's `已验证` label supplies no proof credit.

## Neighbor and formal boundary

`THM-M-0069` (Burnside theorem), `THM-M-0070` (Feit-Thompson theorem), and other local finite-group
targets retain separate scope and status. Their artifacts grant no credit here. Lynd's
Thompson-Lyons theorem is a generalization lead, not a replacement target.

No canonical Lean expression is frozen at intake. `IntakeProbe.lean` checks the pinned types and
transfer/focal declarations needed for a future exact encoding. The bounded search result is not an
exhaustive external anchor audit or a proof of global absence. The statement phase remains blocked
on source identity approval, exact root and alternate-form selection, binder and coercion freeze,
and expression/environment fingerprints.
