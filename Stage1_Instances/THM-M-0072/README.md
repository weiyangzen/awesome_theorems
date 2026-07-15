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

The version-1 obligation registry now freezes 28 root-relevant obligations before proof closure is
observed. It expands Thompson's page-411 route through the inside/outside membership split,
maximal-subgroup normality and index two, the quotient `S/M`, transfer, odd Sylow index, fixed-coset
parity, the transfer product, factor/conjugacy membership, and the no-index-two contradiction.
`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation, and workflow
relations separate. Twenty source-derived internal relations remain explicitly unverified
`logical_decomposition` edges.

`ObligationTree.lean` proves only the inside-`M` boundary and checks conditional composition from an
explicit outside-transfer premise to the exact printed root. It does not construct transfer or
inhabit the open premise. The vector remains `[H1, M3, R4]`; the minimal open machine cut is
`M0072-T-OUTSIDE`, accepted closure is empty, and source H0, readable R0, internal composition,
transitive provenance/trust, validation, release, audit completion, theorem completion, and master
acceptance remain open.
