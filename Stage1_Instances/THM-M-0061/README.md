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

Pinned mathlib also contains the exact proof candidate `Subgroup.card_subgroup_dvd_card` in
`Mathlib.GroupTheory.Coset.Card`. The bounded anchor audit checked its finite-scope adapter and
visible body chain, but candidate evidence remains pending master acceptance and proof-phase
installation.

The obligation-tree phase freezes 20 semantic obligations and seven separate typed graphs. It
expands the short candidate through the quotient-times-subgroup cardinal product and the underlying
fiber/coset equivalence construction. `ObligationTree.lean` checks conditional child-to-parent
composition without installing the candidate. The generated additive theorem, quotient-product
support statement, and Fintype encoding are explicitly deduplicated.

The provisional root vector remains `[H1, M3, R4]`. The theorem family and a textbook source lead are
known, but no primary edition/theorem/page/proof/errata crosswalk or independent review is
accepted; the exact root and candidate are not master-accepted; and no independently reviewed
readable proof reconstruction exists. No H0, accepted M0, R0, accepted proof state, audit
completion, theorem completion, release, or master acceptance is claimed.
