# THM-M-0709 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for the undecidability of Post's
correspondence problem (PCP). The repository's `已验证` label is untrusted discovery metadata and
provides neither human-source nor machine-proof credit.

The intended mathematical root is the uniform decision problem: finite PCP instances over a fixed
finite alphabet are effectively encoded, and no total computable Boolean predicate decides whether
an arbitrary encoded instance has a nonempty matching index sequence. A PCP match uses the same
index sequence on the upper and lower word lists. This excludes the decidability of one fixed
instance and the modified PCP variant unless a checked reduction is supplied.

The statement phase selects a structured finite input over the fixed binary alphabet: `PCPInstance`
is `List (List Bool × List Bool)`. Because this type is itself `Primcodable`, every input is well
formed and no external malformed-code policy is needed. `Statement.lean` freezes the exact target
as `¬ ComputablePred HasSolution`, checks its full definitional expansion, distinguishes four
scope-changing mutations, and proves the empty-instance boundary case.

Lifecycle remains `planned`; provisional root debt remains `[H1, M4, R3]`. The exact Lean statement
is self-tested but pending master acceptance. The primary source has not received a pinpoint
statement/assumption/errata review, no undecidability proof is supplied, and no reviewed
reconstruction exists. All accepted proof state remains empty. Intake evidence is in `validation.md`;
statement evidence and its status boundary are in `statement-validation.md`.
