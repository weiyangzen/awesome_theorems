# THM-M-0200 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0200`, the catalog item
`塞瓦定理` (Ceva's theorem). The repository gives only the gloss `共点线的比例关系` (a ratio
relation for concurrent lines), attributes the item to Giovanni Ceva in 1678, and labels it
`已验证`. Those are untrusted catalog fields, not an exact source crosswalk or machine-proof
evidence.

An inspected, immutable modern source lead states the familiar necessary-and-sufficient result:
for a nondegenerate triangle and one point on each opposite side, the three cevians are concurrent
if and only if the cyclic product of side ratios is one, with signed lengths on extended sides.
This identifies the theorem family but does not decide that the catalog intended both directions,
unsigned distances, directed ratios, side segments, or full sidelines. It is not independently
reviewed or admitted as the catalog's authoritative source, so it supports `H1`, not `H0`.

Pinned mathlib has direct Ceva declarations in algebraic weight and metric distance forms.
`IntakeProbe.lean` authenticates six interfaces and reports the axioms of four representative
bodies. All four triangle-product declarations assume a common concurrency point and derive a
product identity. The two generalized declarations instead derive affine-weight proportionality;
none of the six supplies the converse. Selecting a forward-only root or crediting one branch of an
iff belongs to the statement and anchor-audit phases, not intake.

The provisional vector is `[H1, M3, R4]`: exact source admission and mapping remain open; direct
pinned proof interfaces exist but no canonical target or proof credit is frozen; and no accepted
source-faithful reconstruction exists. `instance.json` is the scope authority and `task-dag.json`
keeps all six downstream phases open. No canonical Lean statement, H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
