# THM-M-0529 frozen obligation tree

The registry contains seven unique obligations. Proof edges point from a parent to its requirements;
each has a reciprocal child-to-parent composition edge. The proof denominator has four nodes, while
statement, source, and provenance nodes remain distinct assurance overlays.

## M0529-ROOT

For every `n : Nat`, `X Y : TopCat`, and `e : X ≃ₜ Y`, the exact degree-`n`, integral,
unreduced singular-homology functor maps `(TopCat.isoOfHomeo e).hom` to an `IsIso` morphism.
Requires `M0529-C-MAP`. Budget: 20 semantic steps.

## M0529-C-MAP

Instantiate generic functorial preservation of isomorphisms at the exact homology functor and the
exact source morphism. Requires `M0529-B-HOMEO` and `M0529-B-FUNCTOR`. The conditional composition
is checked in `ObligationTree.lean`; it supplies no unconditional root proof credit. Budget: 20.

## M0529-B-HOMEO

Establish the `IsIso` instance on the hom morphism of `TopCat.isoOfHomeo e`. This is a substantive
mathlib bridge whose later proof-phase wrapper and terminal provenance must be accepted. Budget: 20.

## M0529-B-FUNCTOR

Instantiate `CategoryTheory.Functor.map_isIso` for the degreewise integral singular-homology
functor. Its terminal declaration/body and transitive trust closure remain proof-phase work. Budget: 20.

## M0529-S-STATEMENT

Preserve the elaborated statement's domains, binder order, coefficient object, degree, and map-level
conclusion. This is a refinement node and is not counted again as a proof body. Budget: 20.

## M0529-X-SOURCE

Attach reviewed primary-source theorem/page, assumptions, conventions, and errata to all material
proof nodes. It is human-source eligible but not machine-proof eligible. Budget: 20.

## M0529-X-PROVENANCE

Resolve terminal declarations and bodies, imports, complete transitive dependency and axiom closure,
TCB, replay receipts, ownership, invalidation, and revocation. It is an informational overlay and
cannot contribute proof credit. Budget: 20.

## Frozen boundary

The root remains `M3`; `H0`, `R0`, proof acceptance, audit completion, and theorem completion are
not claimed. Any node correction, split, merge, eligibility change, or exclusion requires a new
registry version with an append-only ID delta.
