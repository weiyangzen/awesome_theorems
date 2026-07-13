# Scope map

## Preserved theorem family

The canonical root is the finite-group transfer/conjugacy theorem identified as Thompson 1968,
Lemma 5.38(a)(i): in a finite even-order group with
no subgroup of index two, involutions in a Sylow 2-subgroup can be conjugated into each maximal
subgroup of that Sylow subgroup. This is the exact printed universal clause.

The source theorem relates local Sylow-subgroup structure to ambient-group conjugacy through the
transfer homomorphism. The repository's generic local/global gloss is too weak to determine that
claim on its own. Lynd's versioned eponym crosswalk resolves the theorem-name identity strongly
enough to freeze the statement while the catalog date conflict and independent `H0` review remain
explicit source debt.

## Statement-freeze decisions

1. Thompson 1968 Lemma 5.38(a)(i) is the root represented by the catalog title; the decision rests
   on the pinpoint primary clause and Lynd's explicit classical-Thompson-transfer-lemma crosswalk.
2. The exact printed universal statement is canonical. Lynd's restricted `u ∉ M` form is a credited
   alternate with a checked `iff` transport.
3. Finiteness is `[Finite G]`, even order is `Even (Nat.card G)`, and no index-two subgroup is the
   literal `forall H : Subgroup G, H.index != 2`; it is not replaced by `Group.IsPerfect`.
4. `S : Sylow 2 G`, `M : Subgroup S`, and `IsCoatom M` preserve the maximal-proper subgroup and
   nested carrier structure.
5. Involution means `orderOf u = 2`; the conclusion uses ambient `IsConj` with explicit `M` to `S`
   to `G` coercions.
6. Binders follow the source order: `G`, the two ambient premises, `S`, `M`, maximality, `u`, exact
   order, then the conjugate witness.
7. Lemma 5.38(a)(ii) and (b) are outside this root and receive no statement or proof credit here.
8. Foundation, TCB, computation, import, serialization, and mutation profiles are frozen in
   `statement.json`; source preservation, correction review, and `H0` approval remain downstream.

## Degenerate and boundary cases

Source and statement review must explicitly address the trivial group; odd-order groups; groups of
order two; the difference between absence of any index-two subgroup and perfectness; a trivial or
order-two Sylow subgroup; maximal subgroups including the bottom subgroup; an involution already in
the maximal subgroup; an element satisfying `u ^ 2 = 1` but equal to the identity; coercions between
the nested subgroup carriers; and whether conjugacy is written `g⁻¹ug`, `gug⁻¹`, or via `IsConj`.

The target excludes the trivial and all odd-order groups through the printed even-order premise. It
also excludes the identity from the involution binder through exact order two. It includes the
order-two and bottom-maximal cases whenever all ambient premises hold, and includes involutions
already in `M`; `insideMaximal_hasConjugate` checks the latter boundary. The changed-order
`orderOf u = 4` structural mutation is deliberately distinct from the involution binder.

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

`Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget` is the canonical Lean target.
`Statement.lean` elaborates it from the sole direct import `Mathlib.GroupTheory.Sylow`, preserves the
fully explicit printed expression, and checks the restricted-form transport. This statement freeze
is provisional pending master acceptance. The bounded search remains neither an exhaustive anchor
audit nor proof of absence, and no root proof body is credited.
