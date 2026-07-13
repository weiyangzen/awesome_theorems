# THM-M-0920 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0920`. The repository calls
the target `安德鲁斯分裂定理`, attributes it to George Andrews in 1974, and supplies only the gloss
`分拆函数的进一步推广` (a further generalization of the partition function). It labels the item
`已验证`, but rev-5.6 treats that label as untrusted metadata rather than source or proof evidence.

The received name and gloss do not identify one stable proposition. In this context Chinese
`分拆` means integer partition, while `分裂` ordinarily means splitting; the catalog may therefore
contain a title-level translation error. Even after interpreting the subject as integer partitions,
it does not choose a partition-cardinality identity, a generating-function identity, an analytic
multiple-series expansion, a congruence, or another theorem, and it supplies no parameters,
binders, definitions, hypotheses, formula, or conclusion.

George E. Andrews' 1974 PNAS paper *An Analytic Generalization of the Rogers-Ramanujan Identities
for Odd Moduli* is the strongest exact-year and subject lead inspected at intake. Its Theorem 1 is
a parameterized multiple-series/product identity. The paper itself says the classical
Rogers-Ramanujan identities are special cases. However, Andrews published several closely related
works in 1974, including *On the general Rogers-Ramanujan theorem*, and the catalog cites none of
them. The PNAS paper is therefore a candidate identity lead, not the adopted root or H0 evidence.

Pinned mathlib provides ordinary and restricted integer partitions, a generic partition generating
function, and congruence infrastructure. `IntakeProbe.lean` authenticates only those interfaces. A
bounded exact-topic search found no Andrews-Gordon or general Rogers-Ramanujan target in the pinned
Lean tree. No exact formal artifact is credited.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog record as not yet a
stable proposition; it does not refute Andrews' published identities. The canonical mathematical
statement and Lean target remain null, and all six downstream phases remain open. No H0, M0, R0,
accepted state, audit completion, theorem completion, or master acceptance is claimed.
