# THM-M-0072 rev-5.6 statement

This directory is the fail-closed `planned` intake dossier for `THM-M-0072`, catalogued as the
Thompson transfer lemma. The repository gives only the gloss "about the relation between local and
global properties of groups," attributes the item to John Thompson in 1964, and labels it verified.
It supplies no formula, citation, definition, binder, hypothesis, conclusion, or proof boundary.
Under rev-5.6 the label is untrusted inventory metadata and grants no source or machine credit.

A precise eponym crosswalk was located. Justin Lynd's versioned paper *The Thompson-Lyons transfer
lemma for fusion systems* identifies the classical Thompson transfer lemma as Lemma 5.38 in Thompson's
1968 paper *Nonsolvable finite groups all of whose local subgroups are solvable*. The original
Lemma 5.38(a)(i), printed page 411, says that if a finite group has even order and no subgroup of
index two, then, for a Sylow 2-subgroup and a maximal subgroup of it, every involution of the Sylow
subgroup has a conjugate in that maximal subgroup. The source also gives a short transfer proof.

The statement phase selects the exact printed clause as the canonical root. The catalog does not
cite the paper and says 1964 rather than 1968, so this selection remains `H1`, not an `H0` source
acceptance. Parts (a)(ii) and (b) are out of the root: they are further conclusions in the numbered
lemma, whereas both the printed clause and Lynd's eponym formulation identify the conjugacy result.
Lynd's common form assumes the involution lies outside the maximal subgroup.
`thompsonTransferLemmaTarget_iff_outsideMaximalTarget` kernel-checks that it is equivalent to the
printed universal form because an involution already in the maximal subgroup is conjugate to itself.
`thompsonTransferLemmaTarget_iff_ambientOrderTarget` also checks that measuring involution order in
the Sylow carrier or after coercion to `G` is equivalent.

`Statement.lean` uses only the direct import `Mathlib.GroupTheory.Sylow`. It freezes a finite group
`G`, even `Nat.card G`, the literal absence of every subgroup of index two, `S : Sylow 2 G`,
`M : Subgroup S` with `IsCoatom M`, and every `u : S` of exact order two. The conclusion is an
`m : M` ambient-conjugate to `u`, with both nested coercions explicit. Removing the only import
fails. Four structural mutations and the inside-`M` boundary are checked before any proof evidence.

The vector remains `[H1, M3, R4]`: a primary proof passage, exact statement, and eponym crosswalk are
known, but source preservation, errata review, and independent source approval remain open; no proof
of the root has been credited; and no reviewed readable proof reconstruction exists. The statement
node is provisional pending master acceptance, and all later phases remain open. No H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
