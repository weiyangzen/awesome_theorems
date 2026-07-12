# THM-M-0030 rev-5.6 statement

`THM-M-0030` is the repository's Krull intersection theorem item. The catalog describes it only
as an ideal-intersection property in a Noetherian local ring, attributes it to Wolfgang Krull in
1938, and labels it verified. That label is untrusted metadata, not human-source or kernel evidence.

## Planned scope

This intake selects the conventional ideal specialization, with historical source ratification
still open: if `R`
is a commutative Noetherian local ring and `I` is a proper ideal of `R`, then the intersection of
all natural powers `I ^ n` is the zero ideal. The more general finite-module theorem is an
authoritative source form and a pinned Lean candidate, but it is not silently substituted for the
catalog's ideal-only root.

Stacks Project Lemma 10.51.4 (tag `00IP`) was inspected at an immutable revision as an authoritative
modern source lead. It states the finite-module form and proves it using Artin-Rees and Nakayama.
This supports an `H1` lead only: historical source fidelity, corrections, complete premise mapping,
and independent review remain open.

## Formal boundary

Pinned mathlib module `Mathlib.RingTheory.Filtration` contains the close candidate
`Ideal.iInf_pow_eq_bot_of_isLocalRing` and the finite-module declaration
`Ideal.iInf_pow_smul_eq_bot_of_isLocalRing`. `IntakeProbe.lean` authenticates their types with the
pinned toolchain. The proof-body and transitive trust audit remains downstream.

`Statement.lean` freezes `Stage1Instances.THM_M_0030.KrullIntersectionTarget` with three minimal
definition/operation imports. A checked iff connects ideal equality to the elementwise membership
form. Four distinct mutations cover removed properness, a field-only domain, changed binder scope,
and exclusion of the bottom-ideal boundary. Kernel witnesses show that `I = top` is the excluded
counter-boundary and `I = bot` remains in scope. The proof-bearing `Filtration` module is not
imported by the statement.

The vector remains `[H1, M3, R3]`: the exact Lean expression and environment are self-tested, but
the receipt is provisional and pending master acceptance. Historical source fidelity, formal-
anchor and proof-body audit, all downstream phases, audit completion, and theorem completion remain
open. No H0, M0, R0, accepted execution state, proof, or master acceptance is claimed.
