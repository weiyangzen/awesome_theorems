# THM-M-0959 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Croot-Lev-Pach方法` (Croot-Lev-Pach method). The catalog gloss, `多项式方法在cap集问题中的应用`
("application of the polynomial method to the cap-set problem"), describes a method and an
application rather than one truth-valued proposition with fixed binders, hypotheses, conclusion,
and proof-provenance boundary. Its `已验证` value is untrusted metadata and supplies no source or
proof credit.

The exact author/year/topic match is Croot, Lev, and Pach, *Progression-free sets in Z_4^n are
exponentially small*, Annals of Mathematics 185 (2017), 331-337. Its Theorem 1 bounds a
progression-free subset of `Z_4^n` by `4^(gamma*n)`, while Lemma 1 is the polynomial-method
diagonal/linear-independence engine and Proposition 1 is the dense-coset estimate. The paper calls
this a cap-set-type problem, but the classical cap-set problem itself is over `F_3^n` and the next
catalog target, `THM-M-0960`, separately owns the Ellenberg-Gijswijt `F_q^n` upper bound.

The catalog does not select CLP Theorem 1, Corollary 1, Lemma 1, Proposition 1, the reusable proof
method, or a provenance-sensitive package combining them. This intake freezes that ambiguity
rather than replacing the method label with the most convenient theorem. The provisional vector is
`[H5, M4, R4]`: `H5` classifies the received method/application wording as not yet a stable
proposition, not the published CLP results as false; `M4` records that no source-selected formal
artifact is credited; and `R4` records that no readable reconstruction can attach to an
unidentified root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the result choices, source locators, neighbor boundaries,
and excluded substitutions. All six downstream phases remain open in `task-dag.json`.
`IntakeProbe.lean` checks only adjacent pinned APIs for three-term-progression-free sets, finite
product cardinality, `ZMod`, and binary entropy. Exact validation evidence is in `validation.md`
and the provisional `intake-receipt.json`.

No stable canonical proposition, H0, M0, R0, accepted execution state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
