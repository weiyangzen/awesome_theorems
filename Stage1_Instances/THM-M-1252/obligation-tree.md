# Frozen obligation architecture

Item: `S56-M-1252-OBLIGATION_TREE`  
Registry: `THM-M-1252-OBLIGATIONS-v1`

The registry freezes eleven semantic obligations. Wrappers and transports are interfaces, not
additional proof bodies. The only central imported body is the pinned
`Distribution.dsupport_compl_eq`; the later proof phase must install its specialization as the
repo-local target and the validation phase must close provenance and trust.

## Proof spine

`M1252-ROOT` requires `M1252-T-COMPOSE`, which requires `M1252-N-SPECIALIZE`. Specialization
requires both the generic `M1252-L-UPSTREAM` body and the exact `M1252-S-DOMAIN` instantiation.
Every proof edge has a reciprocal `composes` edge in `typed-graphs.json`.

## M1252-ROOT

Exact canonical statement. Open at `M3`; architecture freeze is not proof installation.

## M1252-S-DEFINITIONS

Checked unfolding of `Distribution.IsVanishingOn` into evaluation on supported test functions.

## M1252-S-DOMAIN

Exact universe, space, scalar, open-domain, distribution, and order specialization.

## M1252-S-BOUNDARY

Zero distributions, empty domains, and zero-dimensional spaces remain quantified. There is no
mathematical branch split; this node prevents later proofs from silently adding hypotheses.

## M1252-S-TRANSPORT

Checked one-way transport from the canonical root to `ExpandedTarget`. It shares semantic credit
with the root and definition interface.

## M1252-S-FOUNDATION

Release-facing axiom, TCB, placeholder, and oracle audit. It is open in this phase.

## M1252-N-SPECIALIZE

Central open integration obligation: instantiate the generic `FunLike` theorem at mathlib's
distribution test-function structure and bind it to the canonical target.

## M1252-L-UPSTREAM

Pinned bridge body at mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Anchor audit
found the body `by simp [dsupport, Set.compl_sInter, Set.compl_image_set_of]`; this registry does
not count the audit harness as the final target proof.

## M1252-T-COMPOSE

`root_of_specializedAnchor` is a kernel-checked conditional composition certificate. It consumes
the exact specialized conclusion and adds no undeclared premise.

## M1252-X-SOURCE

Human-source crosswalk boundary. Primary-source edition, pinpoint, wording, and independent review
remain open, so this node supplies no machine proof credit.

## M1252-X-PROVENANCE

Informational release overlay for body identity, imports, transitive constants, foundations,
license, and replay receipts. It supplies no independent proof credit.

## Inapplicable layers

Construction is inapplicable because this is a definitional set identity and constructs no object.
A mathematical case split is inapplicable because the upstream proof is uniform. Computation is
inapplicable because no solver, reflection, finite calculation, numerical result, or oracle is
used. These exclusions remain pending independent integration-lane approval.

Each node has a substantive budget of at most 60 steps. The central imported invocation is not
treated as a primitive leaf: it owns `M1252-L-UPSTREAM` and its own provenance boundary.
