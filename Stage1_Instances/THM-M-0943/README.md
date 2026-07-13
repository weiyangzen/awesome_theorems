# THM-M-0943 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Plunnecke-Ruzsa inequality. The
repository catalog supplies only the slogan "growth of sumsets," attributes the family to Helmut
Plunnecke and Imre Ruzsa in 1970, and labels it verified. Under rev-5.6 that label is untrusted
metadata and provides no exact-statement, source, or proof credit.

The slogan does not select a binder-complete proposition. It leaves open the ambient additive
group, the finite sets and nonemptiness assumptions, a ratio premise versus a free growth constant,
the general `mB - nB` form versus a one-index sumset form, and the treatment of zero indices and
empty sets. The combined attribution and year also span Plunnecke's original growth theorem and
Ruzsa's later sum-and-difference extension rather than identifying one historical theorem passage.

Pinned mathlib contains a strong exact-name candidate,
`Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add`, in
`Mathlib.Combinatorics.Additive.PluenneckeRuzsa`. `IntakeProbe.lean` authenticates that declaration,
three nearby variants, the Petridis bridge, and their reported axioms at the pinned revision. An
inspected Petridis source lead gives a close standard statement, but the catalog does not cite or
adopt it and no independent source review has accepted the transport.

The provisional vector is `[H1, M3, R4]`. A published proof/source lead is known but its exact
source-to-catalog mapping is open; a close pinned formal interface exists but is not an accepted
root or proof; and no source-faithful readable reconstruction is available. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open.

No canonical proposition, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
