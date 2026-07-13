# THM-M-0070 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0070`, the
Feit-Thompson odd order theorem. The catalog gloss `奇数阶群可解` is resolved by the
primary paper's opening theorem: all finite groups of odd order are solvable. The catalog's
`已验证` field remains untrusted metadata and supplies no source or proof credit.

The primary paper was inspected at its title page and page 775 theorem statement. That establishes
the historical statement and candidate source boundary, but a page-one inspection is not a complete
proof, assumptions, corrections, errata, or node crosswalk. The independent source review required
for H0 also remains open.

Pinned mathlib supplies the vocabulary `IsSolvable`, `isSolvable_def`, `derivedSeries`, `Odd`, and
`Nat.card`. `IntakeProbe.lean` checks those interfaces, elaborates the candidate proposition shape,
and checks the order-one boundary. A bounded exact-topic search found no Lean Feit-Thompson root;
the upstream machine-checked result described in the repository is Coq/MathComp, not part of this
Lean dependency closure.

The provisional vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` leaves all six downstream phases open. No canonical Lean expression, H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
