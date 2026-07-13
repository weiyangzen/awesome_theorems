# THM-M-0234 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`儒歇定理`, attributed to Eugene Rouche in 1862 and glossed as "stability of the number of
zeros of functions." The catalog's `已验证` ("verified") field is untrusted metadata under
rev-5.6; it supplies neither human-source nor Lean proof credit.

The name, attribution, date, category, and zero-stability gloss point toward Rouche's theorem in
complex analysis. A modern candidate family says that a holomorphic function and a sufficiently
small boundary perturbation have the same number of interior zeros, counted with multiplicity.
The repository does not provide a formula or source, however, and does not choose the domain,
boundary, holomorphic-neighborhood, inequality, dominance, multiplicity, or zero-count conventions.
No canonical mathematical or Lean proposition is therefore frozen at intake.

There is also an unresolved identity collision. The adjacent target `THM-M-0232` is `鲁歇定理`,
has the same author and year, and is glossed as comparison of the numbers of zeros of holomorphic
functions. The two Chinese titles are alternate transliterations of Rouche. No repository record
explains whether the IDs are accidental duplicates or intentionally different variants. This
dossier does not inspect, modify, merge, or inherit evidence from the other target.

The provisional root vector is `[H1, M4, R4]`: the classical published theorem family and a
bibliographic primary-work lead are identifiable, but the exact source-to-target mapping and date
discrepancy remain unreviewed; no usable exact formal artifact is credited; and no source-faithful
proof reconstruction exists. `IntakeProbe.lean` elaborates adjacent pinned analytic-order,
isolated-zero, and divisor APIs only. All six downstream phases remain open. No canonical
statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
