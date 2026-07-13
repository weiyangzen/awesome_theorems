# THM-M-0635 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-0635`,
`极值定理` (extreme value theorem). The repository says that a continuous function on a compact
set attains maximum and minimum values, attributes the result to Karl Weierstrass in 1860, and
labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not a human-source audit or a
kernel-proof claim.

The gloss identifies the compact-domain extreme-value family, but not one binder-complete
proposition. It does not state that the compact set is nonempty, name the function's domain or
ordered codomain, distinguish global continuity from continuity on the set, or say whether the
maximum and minimum witnesses may differ. Those choices affect truth and formal type. In
particular, the literal existence claim is false for an empty compact set.

`IntakeProbe.lean` checks the pinned definitions and the exact mathlib minimum and maximum
interfaces adjacent to this family. Mathlib itself documents `IsCompact.exists_isMinOn` and
`IsCompact.exists_isMaxOn` as the extreme value theorem. This is a strong formal lead, but intake
does not select it as the canonical root, combine its two conclusions, audit terminal provenance,
or claim proof credit.

The provisional vector is `[H1, M3, R4]`: the classical theorem family and a direct pinned formal
interface are known, while exact source fidelity, canonical statement identity, formal-root
integration, and readable proof reconstruction remain open. `instance.json` is the structured
scope authority, the scope map and crosswalk freeze all proposition-changing choices, and the six
downstream phases remain open in `task-dag.json`. No H0, M0, R0, accepted state, audit completion,
theorem completion, or master acceptance is claimed.
