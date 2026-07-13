# THM-M-0061 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0061`, Lagrange's theorem
for finite groups. The repository claim is narrow and mathematically stable: if `H` is a subgroup
of a finite group `G`, then the order of `H` divides the order of `G`. The catalog's `已验证`
label is untrusted metadata and supplies no source or proof credit.

The scope map preserves the finite ambient-group premise, arbitrary subgroup, and natural-number
divisibility conclusion. In particular, the intake does not silently replace the claim by the
stronger pinned mathlib declaration without a finiteness premise. That declaration uses
`Nat.card`, whose infinite-type convention broadens its domain beyond the catalog wording.

`Statement.lean` now freezes the exact finite-scope root as
`Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget`. Its sole direct import is the
statement-vocabulary module `Mathlib.Algebra.Group.Subgroup.Finite`, not the proof-bearing
coset-cardinality module. It checks an `Iff` transport to the corresponding `Fintype.card`
encoding, distinguishes all four required mutation classes, and exercises groups of order one plus
bottom and top subgroups. `check_statement.py` re-elaborates and fingerprints those expressions and
requires the sole import to be necessary.

Pinned mathlib also contains the close proof candidate `Subgroup.card_subgroup_dvd_card` in
`Mathlib.GroupTheory.Coset.Card`. `IntakeProbe.lean` remains discovery-only evidence; the statement
module deliberately does not import that theorem. The anchor-audit phase owns exact candidate
mapping, terminal-body provenance, transitive dependencies, placeholders, axioms, and trust.

The provisional root vector is `[H1, M3, R4]`. The theorem family and a textbook source lead are
known, but no primary edition/theorem/page/proof/errata crosswalk or independent review is
accepted; the exact root is elaborated but not master-accepted or proved; and no readable proof
reconstruction exists. The statement worker evidence is provisional, and all five later phases
remain open. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
