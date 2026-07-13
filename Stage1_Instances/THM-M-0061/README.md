# THM-M-0061 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0061`, Lagrange's theorem
for finite groups. The repository claim is narrow and mathematically stable: if `H` is a subgroup
of a finite group `G`, then the order of `H` divides the order of `G`. The catalog's `已验证`
label is untrusted metadata and supplies no source or proof credit.

The scope map preserves the finite ambient-group premise, arbitrary subgroup, and natural-number
divisibility conclusion. In particular, the intake does not silently replace the claim by the
stronger pinned mathlib declaration without a finiteness premise. That declaration uses
`Nat.card`, whose infinite-type convention broadens its domain beyond the catalog wording.

Pinned mathlib contains the close candidate `Subgroup.card_subgroup_dvd_card` in
`Mathlib.GroupTheory.Coset.Card`. `IntakeProbe.lean` checks the declaration and elaborates a
representative use under `[Finite G]`, including the trivial, bottom-subgroup, and top-subgroup
boundaries. This is real feasibility evidence only. The downstream statement phase still owns the
canonical declaration, expression fingerprint, alternate transports, and mutation suite; the
anchor-audit phase owns terminal-body, provenance, dependency, placeholder, and trust analysis.

The provisional root vector is `[H1, M3, R4]`. The theorem family and a textbook source lead are
known, but no primary edition/theorem/page/proof/errata crosswalk or independent review is
accepted; a formal candidate elaborates but no exact root is accepted; and no readable proof
reconstruction exists. All six downstream tasks remain open. No H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
