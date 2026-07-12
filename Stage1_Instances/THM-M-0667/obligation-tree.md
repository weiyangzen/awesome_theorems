# THM-M-0667 frozen obligation architecture

Item: `S56-M-0667-OBLIGATION_TREE`. Registry version: 1. Freeze date: 2026-07-12.

The denominator contains 16 canonical obligations frozen from the exact statement and immutable
anchor audit before proof-phase credit. Fourteen are machine-required, twelve require source
mapping, and all sixteen require readable reconstruction.

## Root and statement boundary

<a id="m0667-root"></a> `M0667-ROOT` is exactly `Not (Primrec2 Nat.ack)`.
<a id="m0667-s-normalization"></a> `M0667-S-NORMALIZATION` owns the two-variable recursion and all
zero/successor equations. <a id="m0667-s-encoding"></a> `M0667-S-ENCODING` owns the checked
uncurried and unpaired transports. Neither a unary diagonal-only claim nor general computability
can substitute for the root.

## Proof decomposition

<a id="m0667-n-diagonal"></a> `M0667-N-DIAGONAL` composes a hypothetical binary primitive-recursive
function with two identities. <a id="m0667-t-nat-bridge"></a> `M0667-T-NAT-BRIDGE` moves that
diagonal through `Primrec.nat_iff`. <a id="m0667-n-domination"></a> `M0667-N-DOMINATION` states the
substantive theorem: every unary `Nat.Primrec f` has one Ackermann level strictly dominating it at
every input.

<a id="m0667-b-constructors"></a> `M0667-B-CONSTRUCTORS` expands domination over every inductive
constructor. <a id="m0667-l-base"></a> `M0667-L-BASE` owns zero, successor, and projection cases.
<a id="m0667-l-pair-comp"></a> `M0667-L-PAIR-COMP` owns pair and composition. <a id="m0667-l-prec"></a>
`M0667-L-PREC` owns the nested induction for primitive recursion and remains split-required.
<a id="m0667-l-growth"></a> `M0667-L-GROWTH` owns the monotonicity, pairing, square, nested-call,
and level-shift inequalities and also remains split-required.

<a id="m0667-t-contradiction"></a> `M0667-T-CONTRADICTION` specializes the diagonal domination bound
at its own witnessing level. <a id="m0667-t-assemble"></a> `M0667-T-ASSEMBLE` is kernel-checked in
`ObligationTree.lean`: it composes the exact root from an explicit `DominationPackage` hypothesis.
It therefore validates child-to-parent composition without claiming the domination proof.

## Assurance overlays

<a id="m0667-x-source"></a> `M0667-X-SOURCE` keeps the primary-edition theorem/page/normalization
crosswalk open. <a id="m0667-x-foundation"></a> `M0667-X-FOUNDATION` keeps the transitive axiom and
TCB audit open. <a id="m0667-x-provenance"></a> `M0667-X-PROVENANCE` traces the unique pinned
mathlib terminal body and cannot earn separate proof credit.

## Closure boundary

The root cut set is `M0667-N-DOMINATION`, `M0667-X-FOUNDATION`, and `M0667-X-SOURCE`. The seven
typed graph families and reciprocal proof edges are frozen and self-tested. Root debt remains
`M3`; proof acceptance, `H0`, validation, release, and theorem completion remain open.
