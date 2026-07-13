# THM-M-0760 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Myhill-Nerode定理` (Myhill-Nerode theorem). The math catalog supplies only the gloss
`正则语言的特征` (a characterization of regular languages), the attribution John Myhill / Anil
Nerode, the year 1958, and an untrusted `已验证` label. A separate computer-science catalog row
describes "minimal DFA and distinguishable strings." Together these identify the classical theorem
family, but they do not decide whether this target includes only the regularity/finite-index
equivalence, the minimal-state result, or both.

Pinned mathlib contains a strong exact candidate:
`Language.isRegular_iff_finite_range_leftQuotient`. It says that an arbitrary language over an
arbitrary alphabet is regular exactly when its set of left quotients is finite. Equality of those
left quotients realizes the conventional Nerode equivalence of prefixes. `IntakeProbe.lean` checks
the candidate and its immediate definitions in the pinned environment. This is discovery evidence
for the later statement and anchor-audit phases, not an accepted target fingerprint or proof
receipt.

The intake freezes the family identity, candidate mapping, proposition-changing choices,
degenerate cases, historical-source gap, and six-step open task DAG. It deliberately does not add a
finite-alphabet hypothesis, append a minimum-DFA cardinality conclusion, or silently identify the
catalog wording with the mathlib declaration. The provisional catalog-target vector is
`[H5, M3, R4]`: the received wording is not yet one stable proposition, while a checked formal
candidate interface exists. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.

Validation commands and exact boundaries are recorded in `validation.md`. The root worker packet
and `intake-receipt.json` propose only `[_]` review of this self-tested intake node; the authoritative
checklist remains untouched until the integration lane decides acceptance.
