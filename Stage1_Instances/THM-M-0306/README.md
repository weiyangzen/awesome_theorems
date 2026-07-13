# THM-M-0306 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`弗里德里希斯不等式` (Friedrichs inequality). The complete catalogue gloss is
`紧支集Sobolev函数的估计` ("an estimate for compactly supported Sobolev functions"), attributed
to Kurt Friedrichs and dated 1929. The catalogue gives no formula, primary citation, domain,
dimension, scalar field, Sobolev model, exponent range, derivative convention, norm, constant,
ordered binders, or boundary cases. Its `已验证` label is untrusted metadata and supplies no
source or machine-proof credit.

The gloss identifies a classical Sobolev inequality family, not one proposition. A compact-support
estimate on Euclidean space, a zero-trace inequality on a bounded domain, a boundary-term norm
equivalence, and a general Poincare-type estimate have materially different hypotheses and
conclusions. The catalogue separately retains the same attribution, date, and gloss as PDE target
`THM-M-1240`; no alias, distinction, deduplication, or proof-ownership decision is accepted.

This intake freezes the received family, proposition-changing choices, duplicate boundary, and
source-to-statement gaps. It leaves the canonical mathematical statement and Lean target null.
The provisional root vector is `[H1, M3, R4]`: secondary source discovery supports a classical
proved family but not an accepted exact source crosswalk; pinned mathlib exposes adjacent
compact-support derivative-norm inequalities but no source-matched root is selected; and no
readable proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the open decisions, while `task-dag.json` keeps all six
downstream phases open. `IntakeProbe.lean` checks only adjacent pinned APIs. No canonical
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, duplicate
reconciliation, or master acceptance is claimed.
