# THM-M-0923 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `贝尔数`
(`Bell numbers`). The catalog supplies only the gloss `集合划分的计数` (counting set partitions),
an attribution to Eric Bell, the year 1934, and an untrusted `已验证` label. Those fields identify a
standard enumerative concept, but they do not state one binder-complete truth-valued proposition.

A strong modern scope reference was inspected. NIST DLMF 26.7 defines `B(n)` as the number of
partitions of `{1, ..., n}` and separately records the zero case, the sum over Stirling numbers,
Dobinski's formula, an exponential generating function, and a recurrence. The repository does not
choose among the cardinality characterization, any of those identities, or a bundled recursive
specification. The likely 1934 bibliographic lead, E. T. Bell's *Exponential Numbers*, was confirmed
by metadata, but its article body was not accessible and is not credited as a proof source.

Pinned mathlib contains `Nat.bell`, `Nat.bell_succ`, `Multiset.bell`, and adjacent Stirling-number
interfaces. Its Bell module explicitly leaves proving that these definitions actually count the
indicated set partitions as future work. `IntakeProbe.lean` therefore authenticates exact-topic
definitions and recurrence candidates only. It does not establish the literal catalog claim or
select a canonical theorem.

The provisional root vector is `[H5, M3, R4]`. `H5` classifies the received concept/definition
heading as not yet a stable proposition; it does not say that Bell-number mathematics is false or
open. `M3` records pinned definitions, statement shapes, and recurrence interfaces without a
source-selected exact target. `R4` records that no source-faithful proof reconstruction can attach
before that selection.

`scope-map.md` freezes proposition-changing choices and exclusions,
`source-statement-crosswalk.md` records the source and Lean boundaries, and `task-dag.json` leaves
all six downstream phases open. No canonical statement, accepted proof state, H0, M0, R0, audit
completion, theorem completion, or master acceptance is claimed.
