# THM-M-0305 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`庞加莱不等式` (Poincare inequality). The complete mathematical gloss supplied by the catalogue
is `Sobolev函数的L^p估计` ("an L^p estimate for Sobolev functions"), attributed to Henri
Poincare in 1890. The catalogue gives no bibliography, formula, domain, function space,
normalization, exponent range, derivative convention, constant, hypotheses, or boundary cases.
Its `已验证` label is untrusted metadata and gives no source or machine-proof credit.

The gloss identifies the analytic Poincare-inequality family, but not one proposition. A
mean-subtracted inequality on a bounded connected domain, a zero-trace inequality, and a
compact-support or whole-space Sobolev inequality have materially different hypotheses and
conclusions. The repository also retains the same attribution, year, and gloss as the separate
PDE target `THM-M-1239`; no alias, distinction, or proof-ownership decision has been accepted.
The probability/variance target `THM-M-0998` is explicitly different.

This intake freezes the received family, proposition-changing choices, duplicate boundary, and
source-to-statement gaps. It leaves the canonical mathematical statement and Lean target null.
The provisional root vector is `[H1, M3, R4]`: a classical proved theorem family is recognizable
but its exact primary-source statement is unaudited; pinned mathlib exposes adjacent
Gagliardo-Nirenberg-Sobolev interfaces but no source-matched root is selected; and no readable
proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the open decisions, while `task-dag.json` keeps all six
downstream phases open. `IntakeProbe.lean` checks only adjacent pinned APIs. No canonical
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, duplicate
reconciliation, or master acceptance is claimed.
