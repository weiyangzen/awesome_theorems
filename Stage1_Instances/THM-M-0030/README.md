# THM-M-0030 rev-5.6 obligation tree

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

Pinned mathlib module `Mathlib.RingTheory.Filtration` contains the exact-strength declaration
`Ideal.iInf_pow_eq_bot_of_isLocalRing` and its finite-module and Jacobson supporting bridges.
`AnchorAudit.lean` introduces the frozen binders in their canonical order and closes the copied
target directly with that theorem. Lean prints its transparent body, reports it and both supporting
bridges sorry-free, and reports only `propext`, `Classical.choice`, and `Quot.sound` for the terminal
declaration and local adapter.

The selected proof body is at immutable mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It specializes the finite-module result to `M = R`;
that result reduces properness in a local ring to the Jacobson-radical theorem, whose body uses the
finite-generation/Nakayama route. A bounded public search found only downstream uses in Atlas and
FLT, not an independent external Lean 4 proof declaration. Atlas shares this repository's Lean and
mathlib pins; FLT does not. Search access limitations and the no-saturation boundary are recorded
in `anchor-audit.json`.

`Statement.lean` freezes `Stage1Instances.THM_M_0030.KrullIntersectionTarget` with three minimal
definition/operation imports. A checked iff connects ideal equality to the elementwise membership
form. Four distinct mutations cover removed properness, a field-only domain, changed binder scope,
and exclusion of the bottom-ideal boundary. Kernel witnesses show that `I = top` is the excluded
counter-boundary and `I = bot` remains in scope. The proof-bearing `Filtration` module is not
imported by the statement.

The exact mathlib route is a self-tested pinned `E2` candidate; `M0-W` remains conditional on
later `E1` admission. The accepted vector remains
`[H1, M3, R3]` because the receipts are provisional and pending master acceptance.

## Frozen architecture

`obligation-registry.json` freezes 28 semantic obligations before accepted closure is observed. The
root route exposes the exact mathlib body, its finite-module specialization, the proper-local-ideal
to Jacobson reduction, the fixed-point characterization, stable intersection submodule,
finite-generation/Nakayama witness, and both directions of the power-membership iff. The audit
wrapper and future proof wrapper are deduplicated from the one terminal body.

`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation, and
workflow edges separate. `ObligationTree.lean` checks seven conditional compositions while leaving
the pinned terminal theorem and the central fixed-point and Jacobson-unit facts as explicit
premises. These checks validate interfaces only; they neither install the proof nor close a root.

Historical source fidelity, complete transitive trust, proof-phase integration, validation,
release, audit completion, and theorem completion remain open. No H0, accepted M0/E1, R0, accepted
execution state, `AUDIT-Z`, theorem completion, or master acceptance is claimed.
