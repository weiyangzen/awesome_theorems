# THM-M-0646 rev-5.6 intake

This directory is the `planned` intake for the Loewenheim-Skolem theorem. The repository's source
wording is specifically the upward claim: an infinite first-order structure has arbitrarily large
elementarily equivalent models. At intake, "arbitrarily large" is conservatively scoped as a
cardinal-controlled elementary extension, not merely an unrelated model of the same theory.

The historical name is ambiguous. Loewenheim's 1915 result and Skolem's later refinements are
normally associated with downward countable-model results, whereas the repository sentence is the
modern upward theorem. This mismatch must be resolved against a pinpoint source before `H0` or an
exact canonical Lean statement is accepted.

Pinned mathlib contains plausible upward and downward declarations. They were only declaration-
checked during intake and receive no statement or proof credit. The provisional root vector is
`[H2, M4, R4]`; no elaborated canonical target, accepted proof state, audit completion, or theorem
completion is claimed.

The scope map, source-statement crosswalk, and open task DAG define the downstream work. Exact
intake checks and results are recorded in `validation.md`.
